"""Finish the saved-data examples with source-linked reports; no network calls."""
import json
import textwrap
from datetime import datetime

import examples
import ai_examples


def prior_matches(rows, target):
    cutoff = datetime.fromisoformat(target['startTime'].replace('Z', '+00:00'))
    if cutoff.tzinfo is None:
        raise ValueError('Target needs a timezone')
    eligible = {}
    for row in rows:
        if row['matchId'] == target['matchId'] or row.get('status') != 'finished' or not row.get('endTime'):
            continue
        ended = datetime.fromisoformat(row['endTime'].replace('Z', '+00:00'))
        if ended.tzinfo and ended < cutoff:
            eligible[row['matchId']] = row
    return sorted(eligible.values(), key=lambda r: r['endTime'], reverse=True)


def workflow_report(matches, streams, target, history):
    joined = examples.join_points(matches, streams)
    selected = next((r for r in joined if r['match_id'] == target['matchId'] and r['has_points']), None)
    if selected is None:
        raise ValueError('Target must join to both the cohort and a point stream')
    ids = {target[s]['playerId'] for s in ('player1', 'player2')}
    if ids != {selected['winner_id'], selected['loser_id']}:
        raise ValueError('Participant identities disagree')
    games = target.get('pointByPoint')
    if not games:
        raise ValueError('Game-level points are unavailable')
    prior = prior_matches(history, target)
    pressure = examples.pressure_games(target)
    first = pressure[0] if pressure else None
    return {'matchId': target['matchId'], 'url': target['url'], 'score': target['score'],
            'player1': target['player1']['name'], 'player2': target['player2']['name'],
            'startTime': target['startTime'], 'cohort': len(joined),
            'joined': sum(r['has_points'] for r in joined), 'recorded_points': selected['recorded_points'],
            'game_entries': len(games), 'pressure_games': len(pressure),
            'break_point_opportunities': sum(g['opportunities'] for g in pressure),
            'first_pressure_game': first,
            'prior': {pid: [r['matchId'] for r in prior if any(r[s]['playerId'] == pid for s in ('player1','player2'))] for pid in ids},
            'limitations': ['Limited history exports; not a complete last-ten record.',
                            'Missing end times excluded; historical reconstruction, not an archived forecast.']}


def build_reports(root, frame, save):
    load = lambda n: json.loads((root/'data'/f'{n}.json').read_text(encoding='utf-8'))
    output = root/'reports'
    output.mkdir(exist_ok=True)
    def export(name, data):
        (output/f'{name}.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    def document(name, title, paragraphs):
        (output/f'{name}.md').write_text('# '+title+'\n\n'+'\n\n'.join(paragraphs)+'\n',encoding='utf-8')
    def card(name, title, subtitle, sections, note):
        fig, ax = frame(title, subtitle, 10)
        ax.set_axis_off()
        y = .98
        for heading, text in sections:
            ax.text(.02,y,heading,fontsize=11,color='#087f6f',weight='bold',transform=ax.transAxes)
            lines=textwrap.wrap(text, width=87)
            ax.text(.02,y-.055,'\n'.join(lines),fontsize=12,va='top',linespacing=1.5,transform=ax.transAxes)
            y -= .09 + .052*len(lines)
        if y < -.05:
            raise ValueError('Report card exceeds its layout')
        save(fig,name,note)

    matches, streams, extra = load('tennis-match-dataset'), load('tennis-point-by-point'), load('worked-followups')
    target=extra['target']
    history=[m for p in extra['history'] for m in p['matches']]
    report=workflow_report(matches,streams,target,history)
    export('workflow',report)
    fig, ax = frame('The drilldown reaches the same match',
                    'Muchova vs Shnaider · Wuhan · Q3fQfAg2', 7.3)
    games = target['pointByPoint']
    for i, game in enumerate(games, 1):
        if game.get('tiebreak'):
            ax.axvspan(i-.4, i+.4, color='#e9dfb7')
            continue
        held = game['winner'] == game['server']
        colour = '#087f6f' if held else '#bd4b2b'
        ax.bar(i, game['breakPoints'], color=colour, width=.6)
        ax.scatter(i, -.25, c=colour, marker='o' if held else 'X', s=42)
        if i > 1 and game['set'] != games[i-2]['set']:
            ax.axvline(i-.5, color='#dedfd4')
    ax.set(xlim=(.3,len(games)+.7), ylim=(-.6,4),
           xlabel='Match game number · dot = hold; cross = break',
           ylabel='Break-point opportunities', xticks=[1,5,9,12,13,17,21])
    ax.set_yticks([0,1,2,3])
    save(fig,'15-wuhan-pressure','Same match ID as the cohort, context and history report. 21 games; 9 pressure games; 13 opportunities.\nCached game records retrieved 23 Oct 2026; post-match reconstruction, not a prediction.')
    first=report['first_pressure_game']
    sections=[('01 / MATCH DATASET + POINT STREAM',f"{report['joined']} / {report['cohort']} matches joined. Selected {report['matchId']}: {report['player1']} vs {report['player2']}."),
              ('02 / MATCH HISTORY', '; '.join(f"{target[s]['name']}: {len(report['prior'][target[s]['playerId']])} eligible prior records" for s in ('player1','player2'))+'. Only completed matches ending before the target start qualify.'),
              ('03 / MATCH CONTEXT',f"Start: {report['startTime']}. Score in player-one order: {report['score']}. Winner-first dataset orientation is checked by player ID."),
              ('04 / GAME-LEVEL POINTS',f"{report['game_entries']} games; {report['pressure_games']} pressure games; {report['break_point_opportunities']} break-point opportunities. First: set {first['set']}, game {first['game']}, {first['opportunities']} opportunities; server {'held' if first['held'] else 'was broken'}."),
              ('AUDIT TRAIL',f"Match {report['matchId']}; prior match IDs and source links are preserved in reports/workflow.json and workflow.md.")]
    card('14-workflow-report','One match, four levels of evidence','Muchova vs Shnaider · Wuhan · 15 October 2026',sections,
         'Saved exports plus cached database follow-up, retrieved 23 Oct 2026. No new Actor or model run.\nLimited history; rows without end times excluded. Export overlap is not overall source coverage.')
    document('workflow','Four-Actor research report',[text for _,text in sections]+[
        f"Source: [{target['matchId']}]({target['url']})", *[f"Prior [{r['matchId']}]({r['url']}) — ended {r['endTime']}" for r in prior_matches(history,target)], *report['limitations']])
    eligible=[r for r in extra['rivalry'][0]['matches'] if r['tour'] in ('atp','challenger-men','itf-men') and r['status']=='finished']
    totals=examples.rivalry_by_surface(eligible,'6HdC3z4H')
    export('rivalry',{'totals':totals,'last':eligible[:3],'scheduled_context':None})
    document('rivalry','Sinner–Alcaraz: surface card',[
        *[f"{surface}: Sinner {r['wins']}–{r['losses']}; n={r['wins']+r['losses']}" for surface,r in totals.items()],
        *[f"[{r['matchId']}]({r['url']}) — {r['startTime'][:10]}, {r['tournament']}, {r['score']} (source player order)" for r in eligible[:3]],
        'Scheduled-match context: not fetched in this offline example. Historical results are not current form.',
        '17 completed meetings. Retirements and exhibitions excluded; source coverage is not an official audited H2H.'])
    market=examples.market_comparison(load('flashscore-tennis'))
    focus=next(r for r in market if r['matchId']=='bJT29aAL')
    recent=[r for r in extra['machac'][0]['matches'] if r['status']=='finished' and r.get('endTime') and r['endTime']<'2026-10-22T00:00:00.000Z']
    export('market-followup',{'comparison':focus,'history':recent,'cutoff':'2026-10-22T00:00:00Z'})
    document('market-followup','Machac–Khachanov: inspect the gap',[
        f"Machac: Elo {focus['elo']:.2%}; market {focus['market']:.2%}; gap {focus['gap_pp']:+.2f} pp.",
        *[f"[{r['matchId']}]({r['url']}) — {r['startTime'][:10]}, {r['tournament']}: {r['score']} (source player order)." for r in recent[:3]],
        'History provides context, not a causal explanation for the market gap. Prices were retrieved after play.'])
    plan={'tour':'wta','surface':'Hard','minimum_matches':2}
    ranking=ai_examples.execute_query_plan(matches,plan)
    answer=[f"{r['player']}: {r['upsets']}/{r['eligible']} eligible appearances ({r['rate']:.0%}). Sources: "+', '.join(f'[{mid}](https://www.flashscore.com/match/{mid}/)' for mid in r['match_ids']) for r in ranking[:8]]
    document('query-answer','Which WTA players beat higher-ranked opponents on hard court?',
             [json.dumps(plan),*answer,'Small saved cohort; minimum two eligible appearances. Not a full-season leaderboard.'])
    export('query-answer',{'plan':plan,'ranking':ranking})
    evaluation=load('ai-model-evaluation')
    export('model-evaluation',evaluation)
    import csv
    with (output/'model-predictions.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle);writer.writerow(['match_id','a_won',*evaluation['predictions']])
        for i,row in enumerate(evaluation['test']):
            writer.writerow([row['match_id'],row['a_won'],*[p[i] for p in evaluation['predictions'].values()]])
    # A deliberately modified local copy demonstrates correction semantics, not a source correction.
    stale={**matches[0], 'score':'DEMO OLD VALUE'}
    refreshed=examples.update_dataset([stale],[matches[0]])
    assert len(refreshed)==1 and refreshed[0]['score']==matches[0]['score']
    export('update-demo',{'kind':'synthetic stale value on a real match identity', 'before':[stale], 'after':refreshed})
    scout=load('ai-scout-evidence')
    document('scout','Saved scout output',[ai_examples.render_scout(scout,{'fact_ids':['player1-elo','player2-elo','player1-available-form']}),
             'The image also displays the two source surface ratings as fixed context; the three fact IDs select the textual brief. Editorial selection; no model call.'])
