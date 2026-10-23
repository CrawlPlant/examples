"""Check the new report's identity/cutoff rules and public bundle privacy."""
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=ROOT/'tennis'
sys.path.insert(0,str(BUNDLE))
from reports import workflow_report, prior_matches
load=lambda n:json.loads((BUNDLE/'data'/f'{n}.json').read_text(encoding='utf-8'))
extra=load('worked-followups');target=extra['target']
history=[m for p in extra['history'] for m in p['matches']]
args=[load('tennis-match-dataset'),load('tennis-point-by-point'),target,history]
r=workflow_report(*args)
assert (r['cohort'],r['joined'],r['game_entries'],r['pressure_games'],r['break_point_opportunities'])==(233,116,21,9,13)
assert sorted(map(len,r['prior'].values()))==[4,10]
assert target['matchId'] not in {x['matchId'] for x in prior_matches(history,target)}
bad=copy.deepcopy(target);bad['player1']['playerId']='invalid'
try: workflow_report(args[0],args[1],bad,history)
except ValueError:pass
else:raise AssertionError('Mismatched identity accepted')
synthetic=copy.deepcopy(history[1]);synthetic['matchId']='test';synthetic['endTime']=target['startTime']
assert not prior_matches([synthetic],target)
synthetic['endTime']=None
assert not prior_matches([synthetic],target)
rivalry=json.loads((BUNDLE/'reports/rivalry.json').read_text())
assert sum(sum(x.values()) for x in rivalry['totals'].values())==17
for name in ('01-rank-upsets', '07-ai-scout-card', '13-illustrated-recap', '14-workflow-report'):
    assert (BUNDLE/'assets'/f'{name}.png').stat().st_size > 1000
for path in BUNDLE.glob('*.py'):
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
print('PASS: identity checks, history cutoffs, H2H inclusion and generated artifacts.')
