"""Figures and evidence exports for the four AI articles; no model or Actor calls."""
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

import ai_examples as ai


def build_ai_assets(root, frame, save):
    load = lambda name: json.loads((root / "data" / name).read_text(encoding="utf-8"))
    export = lambda name, value: (root / "data" / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    ink, muted, green, orange, grid = "#16352f", "#64756e", "#087f6f", "#bd4b2b", "#dedfd4"
    history = load("tennis-match-history.json")
    evidence = ai.scout_evidence(history[0], history)
    chosen = {"fact_ids": ["player1-elo", "player2-elo", "player1-available-form"]}
    export("ai-scout-evidence.json", evidence)
    export("ai-scout-editorial-selection.json", {"kind": "editorial-preview-not-model-output", **chosen})
    (root/"ai-scout-preview.md").write_text("*Historical reconstruction; editorial evidence selection, not live model output.*\n\n"+ai.render_scout(evidence,chosen),encoding="utf-8")

    fig, ax = frame("An AI scout with a paper trail", "Sinner vs Zverev  ·  historical reconstruction of the 2026 Wimbledon final", 9)
    ax.set_axis_off()
    for i,(name,overall,surface) in enumerate(((history[0]["player1Name"], history[0]["player1Elo"], history[0]["elo"]["player1Surface"]),(history[0]["player2Name"], history[0]["player2Elo"], history[0]["elo"]["player2Surface"]))):
        x=.03+i*.51
        ax.add_patch(FancyBboxPatch((x,.51),.44,.43,boxstyle="round,pad=0.02",facecolor="#edf0e7",edgecolor=grid,transform=ax.transAxes))
        ax.text(x+.025,.87,name,fontsize=13,weight="bold",color=green,transform=ax.transAxes)
        ax.text(x+.025,.70,str(overall),fontsize=36,weight="bold",transform=ax.transAxes)
        ax.text(x+.25,.70,"overall Elo\nbefore match",fontsize=10,color=muted,transform=ax.transAxes)
        ax.text(x+.025,.56,f"Surface Elo  {surface}",fontsize=12,transform=ax.transAxes)
    selected = [f for f in evidence["facts"] if f["id"] in chosen["fact_ids"]]
    form = next(f for f in selected if f["id"] == "player1-available-form")
    ax.text(.035,.40,"PRIOR MATCH EVIDENCE",fontsize=11,color=green,weight="bold",transform=ax.transAxes)
    ax.text(.035,.30,form["text"],fontsize=12,weight="bold",transform=ax.transAxes)
    ax.text(.035,.20,evidence["limitations"][0],fontsize=10,color=muted,transform=ax.transAxes)
    ax.text(.035,.10,"SOURCES · target " + evidence["matchId"],fontsize=10,color=green,transform=ax.transAxes)
    for j, source in enumerate(form["sources"]):
        ax.text(.035 + j*.24,.025,source["matchId"],fontsize=10,url=source["url"],transform=ax.transAxes)
    save(fig,"07-ai-scout-card","Cutoff: 12 Jul 2026, 15:10 UTC. Ratings reconstructed from saved source records retrieved after the event.\nLimited history sample; not last-ten coverage. Editorial preview, not an archived forecast or paid model output.")

    fig, ax = frame("Let AI edit. Keep the evidence attached.", "Flashscore Tennis + Match History → validated selection → cited scout", 8.5)
    ax.set_axis_off()
    steps=[("01","SOURCE ACTORS","Target context + completed prior matches","Stable player IDs · match IDs"),
           ("02","PYTHON EVIDENCE LEDGER","Exclude target outcomes; enforce the cutoff","Facts · field paths · source links"),
           ("03","AI EDITOR","Select existing evidence IDs","No invented numerical fields"),
           ("04","DETERMINISTIC SCOUT CARD","Render facts, sources and missing coverage","Human review before publication")]
    for i,(number,title,desc,detail) in enumerate(steps):
        y=.94-i*.25
        ax.text(.015,y,number,fontsize=25,weight="bold",color=green,transform=ax.transAxes)
        ax.text(.12,y+.02,title,fontsize=11,weight="bold",transform=ax.transAxes)
        ax.text(.12,y-.045,desc,fontsize=15,transform=ax.transAxes)
        ax.text(.12,y-.105,detail,fontsize=10,color=muted,transform=ax.transAxes)
        if i<3: ax.annotate("",xy=(.045,y-.18),xytext=(.045,y-.045),xycoords=ax.transAxes,arrowprops={"arrowstyle":"->","color":grid,"lw":2})
    save(fig,"08-ai-evidence-flow","Optional drilldown: point-by-point of a prior completed match. Target-match points are post-match information.\nSource strings are data, not tool instructions. Enum validation checks structure, not source correctness.")

    matches = load("tennis-match-dataset.json")
    plan = {"tour":"wta","surface":"Hard","minimum_matches":2}
    ranking = ai.execute_query_plan(matches,plan)
    export("ai-query-result.json", {"plan":plan,"plan_kind":"editorial-example-not-model-output","rows":ranking})
    top=ranking[:8]
    fig,ax=frame("Ask a question. Show the denominator.","WTA hard court  ·  wins / eligible appearances as the lower-ranked player",8.3)
    fig.subplots_adjust(left=.28,right=.91)
    for i,row in enumerate(top):
        ax.barh(i,100,color=grid,height=.55)
        ax.barh(i,row["rate"]*100,color=green,height=.55)
        ax.text(row["rate"]*100-2,i,f"{row['upsets']}/{row['eligible']}",ha="right",va="center",color="white",fontsize=11,weight="bold")
    ax.set(yticks=range(len(top)),yticklabels=[r["player"] for r in top],xlim=(0,100),xlabel="Observed upset win rate in the selected export (%)")
    ax.invert_yaxis()
    save(fig,"09-ai-query-upsets","Source: saved 233-match export, 22 Oct 2026. WTA / Hard / at least 2 eligible underdog appearances.\nSmall samples. Missing/tied ranks and RET / W/O / DEF excluded. This is not a full-season ranking.")

    match=load("wimbledon-2024-points.json")
    ledger=ai.recap_evidence(match)
    export("ai-recap-evidence.json",ledger)
    stats=[]
    for side in ("player1","player2"):
        pressure=[g for g in match["pointByPoint"] if not g.get("tiebreak") and g.get("server")==side and g.get("breakPoints",0)>0]
        stats.append({"name":match[f"{side}Name"],"opportunities":sum(g["breakPoints"] for g in pressure),"games":len(pressure),"held":sum(g["winner"]==side for g in pressure)})
    fig,ax=frame("The pressure has two denominators", "Wimbledon 2024 final  ·  break-point opportunities and ordinary service games",7.7)
    ax.set_axis_off()
    cols=[("BREAK POINTS FACED","opportunities"),("PRESSURE GAMES","games"),("OF THOSE, HELD","held")]
    for i,item in enumerate(stats):
        y=.82-i*.50
        ax.text(.01,y,item["name"],fontsize=16,weight="bold",color=green if i==0 else orange,transform=ax.transAxes)
        for j,(label,key) in enumerate(cols):
            x=.31+j*.24
            ax.text(x,y+.03,label,fontsize=8.5,color=muted,transform=ax.transAxes)
            ax.text(x,y-.15,str(item[key]),fontsize=36,weight="bold",color=green if i==0 else orange,transform=ax.transAxes)
    save(fig,"10-ai-recap-pressure","Recorded point feed Sf0bExdB, parsed with the production parser: 28 ordinary games, 9 pressure games, 1 tiebreak.\nA pressure game can contain several break-point opportunities. Tiebreaks excluded from these service-game counts.")

    result=ai.fit_temporal_baseline(matches)
    export("ai-model-evaluation.json",result)
    data=ai.model_rows(matches)
    weeks=sorted({r["week"] for r in data})
    counts=Counter(r["week"] for r in data)
    fig,ax=frame("Train earlier weeks. Hold later weeks out.","Illustrative tournament-week split  ·  exact match-time validation is still required")
    ax.bar(range(len(weeks)),[counts[w] for w in weeks],color=[green if w<result["cutoff_week"] else orange for w in weeks],width=.5)
    for i,w in enumerate(weeks): ax.text(i,counts[w]+3,str(counts[w]),ha="center",weight="bold")
    ax.set(xticks=range(len(weeks)),xticklabels=[f"{str(w)[4:6]}/{str(w)[6:]}\n{'TRAIN' if w<result['cutoff_week'] else 'TEST'}" for w in weeks],ylim=(0,max(counts.values())+22),ylabel="Eligible match rows",xlabel="Tournament-week labels in October 2026")
    save(fig,"11-ml-week-split",f"Saved export: {result['train_count']} train rows, {result['test_count']} test rows. Completed-score filter; ATP and WTA pooled.\nA tournament-week label is not a match finish timestamp. Small pipeline demonstration, not a strict historical backtest.")

    fig,ax=frame("The fitted model loses to overall Elo", "Test subset  ·  Brier score  ·  lower is better")
    names=list(result["scores"])
    values=[result["scores"][n]["brier"] for n in names]
    ax.barh(range(3),values,color=[grid,green,orange],height=.5)
    for i,v in enumerate(values): ax.text(v+.004,i,f"{v:.4f}",va="center",weight="bold")
    ax.set(yticks=range(3),yticklabels=names,xlim=(0,.31),xlabel="Mean squared probability error (Brier score)")
    ax.invert_yaxis()
    fig.subplots_adjust(left=.21)
    save(fig,"12-ml-baselines",f"Same {result['test_count']} held-out later-week rows for all three methods. Logistic model fitted on {result['train_count']} earlier-week rows.\nOverall Elo formula, not the Actor's blended probability. No uncertainty interval, deployment or profit claim.")
    return 6
