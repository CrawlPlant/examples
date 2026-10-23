# Use the data from code

## Python

After the [shared setup](../docs/LIVE-QUICKSTART.md):

```sh
python code/python/direct_match.py
```

The example imports `run_actor` from `live.py`, which reads the token from `.env`,
enforces the requested per-run charge limit and exports all dataset pages.
Copy its small input dictionary to adapt the example. The 48 [recipes](../docs/CATALOG.md)
provide working input dictionaries for all 15 Actors.

## JavaScript / native REST

Node 22 or newer, from the repository root:

```sh
node --env-file=.env code/javascript/match.mjs --dry-run
node --env-file=.env code/javascript/match.mjs
```

No npm install is required. Node loads `.env`; the script uses the token in an
Authorization header, starts one capped run, waits for completion and paginates
the dataset. Outputs are in `output/direct-javascript-match/`.

## Read the exports in your own Python code

```python
import json
import sqlite3
from contextlib import closing
from pathlib import Path

folder = Path('output/tennis-dataset/matches')
rows = json.loads((folder / 'data.json').read_text(encoding='utf-8'))
print('Saved sample:', len(rows))

with closing(sqlite3.connect(folder / 'data.sqlite')) as db:
    for (raw,) in db.execute('SELECT data FROM records LIMIT 5'):
        match = json.loads(raw)
        print(match.get('winner_name'), match.get('loser_name'))
```

The live Python runner exports JSON, JSONL, CSV and SQLite for every Actor.
Use the raw JSON for nested structures; CSV serializes nested arrays and objects as JSON strings.
