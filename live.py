"""Shared live transport. Importing it never starts a paid run."""
import csv
import hashlib
import json
import math
import os
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from apify_client import ApifyClient
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
DEFAULTS = dict(PLAYER='Jannik Sinner', OPPONENT='Alcaraz',
                MATCH_PLAYER='Alcaraz', MATCH_OPPONENT='Djokovic', MATCH_DATE='2024-07-14', MATCH_TOURNAMENT='Wimbledon',
                SCOUT_PLAYER='Muchova', SCOUT_OPPONENT='Shnaider', SCOUT_DATE='2026-10-15', SCOUT_TOURNAMENT='Wuhan',
                DOMAIN='apify.com', YOUR_DOMAIN='scrapy.org', COMPETITOR='zyte.com',
                QUERY='milk', POSTCODE='2000', ALDI_POSTCODE='2010', ADVERTISER='nike.com',
                DATE_FROM='yesterday', DATE_TO='yesterday')


def configure():
    load_dotenv(ROOT / '.env', override=False)


def resolve(value):
    if isinstance(value, dict):
        return {k: resolve(v) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(v) for v in value]
    if not isinstance(value, str):
        return value
    match = re.fullmatch(r'\$\{([A-Z_]+)\}', value)
    if match:
        key = match[1]
        value = os.getenv(key) or DEFAULTS[key]
        if key in ('DATE_FROM', 'DATE_TO') and value in ('today', 'yesterday'):
            day = datetime.now(timezone.utc).date() - timedelta(days=value == 'yesterday')
            value = day.isoformat()
    return value


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def export_rows(folder, rows):
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'data.json', rows)
    with (folder / 'data.jsonl').open('w', encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    fields = sorted({key for row in rows for key in row})
    with (folder / 'data.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        if fields:
            writer.writeheader()
        for row in rows:
            safe = {}
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                # CSV viewers may execute formulas from untrusted source text.
                if isinstance(value, str) and value.lstrip().startswith(('=', '+', '-', '@')):
                    value = "'" + value
                safe[key] = value
            writer.writerow(safe)
    with closing(sqlite3.connect(folder / 'data.sqlite')) as db, db:
        db.execute('CREATE TABLE IF NOT EXISTS records (row_number INTEGER PRIMARY KEY, data TEXT NOT NULL)')
        db.execute('DELETE FROM records')
        db.executemany('INSERT INTO records VALUES (?, ?)',
                       [(i, json.dumps(row, ensure_ascii=False)) for i, row in enumerate(rows, 1)])


def run_actor(slug, run_input, folder, *, reuse=False, client=None):
    token = os.getenv('APIFY_TOKEN', '').strip()
    if not token and client is None:
        raise ValueError('Set APIFY_TOKEN in the repository .env file.')
    charge = Decimal(os.getenv('APIFY_MAX_CHARGE_USD', '0.50'))
    timeout = int(os.getenv('APIFY_TIMEOUT_SECONDS', '180'))
    if not charge.is_finite() or charge <= 0 or timeout < 1:
        raise ValueError('Charge limit and timeout must be positive finite values.')
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        raise ValueError('Invalid Actor slug')
    folder = Path(folder)
    identity = {'actor': 'crawlplant/' + slug, 'input': run_input}
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    metadata = folder / 'run.json'
    if reuse and metadata.exists() and (folder / 'data.json').exists():
        saved = json.loads(metadata.read_text(encoding='utf-8'))
        if saved.get('fingerprint') == fingerprint and saved.get('status') == 'SUCCEEDED':
            return json.loads((folder / 'data.json').read_text(encoding='utf-8'))
    client = client or ApifyClient(token)
    # No application-level retry: an uncertain start must not create a second paid run.
    run = client.actor(identity['actor']).call(run_input=run_input,
        max_total_charge_usd=charge, timeout_secs=timeout)
    if not run:
        raise RuntimeError('No run returned. Inspect Apify Console before trying again.')
    info = {**identity, 'fingerprint': fingerprint, 'run_id': run['id'],
            'dataset_id': run.get('defaultDatasetId'), 'status': run['status'],
            'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'requested_max_charge_usd': str(charge), 'usage_total_usd': run.get('usageTotalUsd')}
    write_json(metadata, info)
    if run['status'] != 'SUCCEEDED':
        raise RuntimeError(f"Run {run['id']} ended as {run['status']}; see run.json and Apify Console.")
    rows = list(client.dataset(run['defaultDatasetId']).iterate_items())
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError('Expected an array of dataset objects')
    info['row_count'] = len(rows)
    info['at_item_cap'] = len(rows) >= run_input.get('maxItems', math.inf)
    info['coverage_note'] = 'Bounded sample; item/charge limits and source coverage may truncate results.'
    export_rows(folder, rows)
    write_json(metadata, info)
    print(f"{identity['actor']}: {len(rows)} rows -> {folder}")
    if info['at_item_cap']:
        print('Item cap reached: this is a sample, not a complete export.')
    return rows


def select_named_match(rows, selection):
    """Name filters are OR on Apify; validate the pair before using the result."""
    def contains(value, part):
        return bool(part.strip()) and part.casefold() in str(value or '').casefold()
    found = []
    for row in rows:
        names = [row.get('player1Name', row.get('server1')), row.get('player2Name', row.get('server2'))]
        left, right = selection['players']
        pair = ((contains(names[0], left) and contains(names[1], right)) or
                (contains(names[1], left) and contains(names[0], right)))
        date = str(row.get('date', '')).replace('-', '')
        if row.get('pbp_id') and not date.isdigit():
            try:
                date = datetime.strptime(date, '%d %b %y').strftime('%Y%m%d')
            except ValueError:
                continue
        tournament = row.get('tournament', row.get('tny_name'))
        if pair and date == selection['date'].replace('-', '') and contains(tournament, selection['tournament']):
            found.append(row)
    if len(found) != 1:
        raise ValueError('Expected one match for the named pair, date and tournament; inspect candidates, refine names/date or raise the candidate cap. Do not guess an ID.')
    return found[0]
