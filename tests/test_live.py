import copy
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch

from jsonschema import Draft7Validator
from live import ROOT, configure, export_rows, resolve, run_actor
from workflows import one_match, process, select_ids


class FakeClient:
    def __init__(self, status='SUCCEEDED'):
        self.status = status
        self.calls = []
    def actor(self, actor):
        self.actor_name = actor
        return self
    def call(self, **kwargs):
        self.calls.append(kwargs)
        return {'id':'test-run', 'status':self.status, 'defaultDatasetId':'test-dataset'}
    def dataset(self, dataset_id):
        return self
    def iterate_items(self):
        yield {'name':'=UNTRUSTED()', 'nested':{'value':1}}
        yield {'name':'second page', 'nested':{'value':2}}


class LiveTests(unittest.TestCase):
    def test_all_inputs_match_published_schemas(self):
        recipes=list((ROOT/'recipes').glob('*.json'))
        self.assertEqual(len(recipes),48)
        for path in recipes:
            recipe=resolve(json.loads(path.read_text(encoding='utf-8')))
            for step in recipe['steps']:
                schema=json.loads((ROOT/'tests/schemas'/f"{step['actor']}.json").read_text(encoding='utf-8'))
                schema['additionalProperties']=False
                with self.subTest(recipe=path.stem, actor=step['actor']):
                    Draft7Validator(schema).validate(step['input'])

    def test_transport_limits_export_and_cache(self):
        client=FakeClient()
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'APIFY_MAX_CHARGE_USD':'0.02','APIFY_TIMEOUT_SECONDS':'60'}):
            folder=Path(tmp)
            rows=run_actor('flashscore-tennis', {'maxItems':2}, folder, client=client)
            self.assertEqual(len(rows),2)
            self.assertEqual(str(client.calls[0]['max_total_charge_usd']),'0.02')
            self.assertEqual(client.calls[0]['timeout_secs'],60)
            self.assertIn("'=UNTRUSTED()",(folder/'data.csv').read_text())
            with closing(sqlite3.connect(folder/'data.sqlite')) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM records').fetchone()[0],2)
            self.assertTrue(json.loads((folder/'run.json').read_text())['at_item_cap'])
            run_actor('flashscore-tennis', {'maxItems':2}, folder, reuse=True, client=client)
            self.assertEqual(len(client.calls),1)
            run_actor('flashscore-tennis', {'maxItems':3}, folder, reuse=True, client=client)
            self.assertEqual(len(client.calls),2)

    def test_failed_run_is_not_cached_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError,'TIMED-OUT'):
                run_actor('flashscore-tennis', {}, Path(tmp), client=FakeClient('TIMED-OUT'))
            self.assertFalse((Path(tmp)/'data.json').exists())
            self.assertEqual(json.loads((Path(tmp)/'run.json').read_text())['status'],'TIMED-OUT')

    def test_invalid_budget_rejected_before_call(self):
        for value in ('NaN','Infinity','0','-1'):
            with self.subTest(value=value), patch.dict(os.environ, {'APIFY_MAX_CHARGE_USD':value}):
                with self.assertRaises(ValueError):
                    run_actor('flashscore-tennis', {}, Path('unused'), client=FakeClient())

    def test_empty_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            export_rows(Path(tmp),[])
            self.assertEqual(json.loads((Path(tmp)/'data.json').read_text()),[])

    def test_model_unknown_duplicate_and_oversized_selections(self):
        evidence={'facts':[{'id':'known'}]}
        for ids in ([], ['missing'], ['known','known'], [{}]):
            with patch('workflows.ai_json', return_value={'fact_ids':ids}):
                with self.assertRaises(ValueError):select_ids(evidence,'task')

    def test_wrong_match_identity(self):
        with self.assertRaises(ValueError):one_match([{'matchId':'wrong'}],'expected')

    def test_dotenv_does_not_override_existing_environment(self):
        with tempfile.TemporaryDirectory() as tmp, patch('live.ROOT',Path(tmp)), patch.dict(os.environ,{'APIFY_TOKEN':'shell-token'}):
            (Path(tmp)/'.env').write_text('APIFY_TOKEN=file-token\n',encoding='utf-8')
            configure()
            self.assertEqual(os.environ['APIFY_TOKEN'],'shell-token')

    def test_scout_fetches_both_players_and_excludes_target_result(self):
        history=json.loads((ROOT/'tennis/data/tennis-match-history.json').read_text())
        target=history[0]
        recipe={'process':'scout','goal':'Scout','steps':[{'input':{'matchIds':[target['matchId']]}}]}
        with tempfile.TemporaryDirectory() as tmp, patch('workflows.run_actor',return_value=history) as actor:
            process(recipe,{'match':[target]},Path(tmp))
            self.assertEqual(actor.call_count,2)
            evidence=json.loads((Path(tmp)/'evidence.json').read_text())
            self.assertNotIn('winner',evidence)
            self.assertNotIn('score',evidence)
            self.assertTrue((Path(tmp)/'report.md').exists())

    def test_offline_analysis_processors(self):
        load=lambda n:json.loads((ROOT/'tennis/data'/n).read_text(encoding='utf-8'))
        matches=load('tennis-match-dataset.json')
        cases=[('cohort',{'matches':matches}),('update',{'matches':matches}),
               ('join',{'matches':matches,'points':load('tennis-point-by-point.json')}),
               ('pressure',{'points':[load('wimbledon-2024-points.json')]}),
               ('market',{'matches':load('flashscore-tennis.json')}),
               ('evidence',{'matches':matches}),('query',{'matches':matches})]
        for kind,batches in cases:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                process({'process':kind,'goal':'Test evidence'},batches,Path(tmp))
                self.assertTrue(list(Path(tmp).glob('*.json')))

    def test_recap_counts_and_prompt(self):
        match=json.loads((ROOT/'tennis/data/wimbledon-2024-points.json').read_text())
        recipe={'process':'recap','goal':'Recap with citations','steps':[{'input':{'matchIds':[match['matchId']]}}]}
        with tempfile.TemporaryDirectory() as tmp:
            process(recipe,{'points':[match]},Path(tmp))
            evidence=json.loads((Path(tmp)/'evidence.json').read_text())
            self.assertEqual(evidence['break_point_opportunities'],17)
            self.assertTrue((Path(tmp)/'prompt.md').exists())

if __name__ == '__main__':unittest.main()
