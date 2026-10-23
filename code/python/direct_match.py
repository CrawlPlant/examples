"""A minimal SDK example using the same .env and bounded transport as the catalog.

Run from the repository root: python code/python/direct_match.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from live import ROOT, configure, run_actor

configure()
rows = run_actor('flashscore-tennis', {
    'mode': 'matchIds',
    'matchIds': [os.getenv('MATCH_ID') or 'Sf0bExdB'],
    'includeOdds': False,
    'includeH2H': False,
    'maxItems': 2,
}, ROOT / 'output/direct-python-match')

for match in rows:
    print(match.get('matchId'), match.get('player1Name'), match.get('player2Name'), match.get('score'))
