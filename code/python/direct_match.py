"""A minimal SDK example using the same .env and bounded transport as the catalog.

Run from the repository root: python code/python/direct_match.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from live import ROOT, configure, run_actor, resolve, select_named_match

configure()
rows = run_actor('flashscore-tennis', {
    'mode': 'matches',
    'dateFrom': resolve('${MATCH_DATE}'), 'dateTo': resolve('${MATCH_DATE}'),
    'players': [resolve('${MATCH_PLAYER}')],
    'tournaments': [resolve('${MATCH_TOURNAMENT}')], 'tours': ['atp'],
    'includeOdds': False,
    'includeH2H': False,
    'maxItems': 20,
}, ROOT / 'output/direct-python-match')

selected = select_named_match(rows, resolve({'players':['${MATCH_PLAYER}', '${MATCH_OPPONENT}'],
    'date':'${MATCH_DATE}', 'tournament':'${MATCH_TOURNAMENT}'}))
for match in [selected]:
    print(match.get('player1Name'), 'vs', match.get('player2Name'), match.get('date'), match.get('score'))
    print('Source:', match.get('url') or match.get('matchId'))
