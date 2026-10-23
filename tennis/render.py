"""Render original figures and an offline reading edition. No network or Actor calls."""
import html
import inspect
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import examples
import ai_examples

ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
load = lambda name: json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
snapshot = load("public-snapshot.json")
matches = load("tennis-match-dataset.json")
points = load("tennis-point-by-point.json")
market = examples.market_comparison(load("flashscore-tennis.json"))
joined = examples.join_points(matches, points)
INK, MUTED, GREEN, ORANGE, PAPER, GRID = "#16352f", "#64756e", "#087f6f", "#bd4b2b", "#faf8f2", "#dedfd4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "axes.spines.bottom": False, "figure.facecolor": PAPER, "axes.facecolor": PAPER})


def frame(title, subtitle, height=6.7):
    fig, ax = plt.subplots(figsize=(12, height))
    fig.subplots_adjust(left=.12, right=.95, top=.74, bottom=.20)
    fig.text(.07, .94, "CRAWLPLANT  /  TENNIS DATA LAB", fontsize=10, color=GREEN, weight="bold")
    fig.text(.07, .865, title, fontsize=23, weight="bold")
    fig.text(.07, .805, subtitle, fontsize=11, color=MUTED)
    return fig, ax


def save(fig, name, note):
    fig.text(.07, .07, note, fontsize=9, color=MUTED)
    fig.savefig(ASSETS / f"{name}.png", dpi=170)
    fig.savefig(ASSETS / f"{name}.svg")
    plt.close(fig)


ranked = [r for r in matches if r.get("winner_rank") is not None and r.get("loser_rank") is not None
          and r["winner_rank"] != r["loser_rank"] and not any(c in (r.get("score") or "") for c in ("RET", "W/O", "DEF"))]
fig, ax = frame("The lower-ranked player still wins", "Ranking upsets in one saved batch. Each bar includes its own denominator.")
for i, tour in enumerate(("atp", "wta")):
    group = [r for r in ranked if r["tour"] == tour]
    wins = sum(r["winner_rank"] > r["loser_rank"] for r in group)
    rate = 100 * wins / len(group)
    ax.barh(i, 100, color=GRID, height=.5)
    ax.barh(i, rate, color=GREEN if i == 0 else ORANGE, height=.5)
    ax.text(rate + 2, i, f"{rate:.1f}%   ·   {wins}/{len(group)} matches", va="center", weight="bold", fontsize=13)
ax.set(yticks=[0, 1], yticklabels=["ATP", "WTA"], xlim=(0, 100), xlabel="Share of eligible matches (%)")
ax.invert_yaxis()
save(fig, "01-rank-upsets", "Source: saved 233-row Actor export, run 22 Oct 2026. Not a full season; qualifying included.\nMissing/tied ranks and RET / W/O / DEF excluded. Ranking upset ≠ market upset.")

followups = load("worked-followups.json")
rivalry = [r for r in followups["rivalry"][0]["matches"]
           if r["tour"] in ("atp", "challenger-men", "itf-men") and r["status"] == "finished"]
totals = examples.rivalry_by_surface(rivalry, "6HdC3z4H")
surfaces = [{"surface": s, "player1Wins": r["wins"], "player2Wins": r["losses"]}
            for s, r in totals.items()]
fig, ax = frame("One rivalry. Three surfaces.", "Sinner vs Alcaraz  ·  recorded head-to-head split by surface")
for i, row in enumerate(surfaces):
    a, b = row["player1Wins"], row["player2Wins"]
    ax.barh(i, a, color=GREEN, height=.55)
    ax.barh(i, b, left=a, color=ORANGE, height=.55)
    if a: ax.text(a/2, i, str(a), color="white", ha="center", va="center", weight="bold")
    if b: ax.text(a+b/2, i, str(b), color="white", ha="center", va="center", weight="bold")
    ax.text(a+b+.22, i, f"n={a+b}", va="center", color=MUTED)
ax.set(yticks=range(len(surfaces)), yticklabels=[r["surface"].title() for r in surfaces], xlim=(0, 11.7), xlabel="Recorded wins")
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.invert_yaxis()
ax.legend(handles=[Line2D([0], [0], color=GREEN, lw=8, label="Jannik Sinner"), Line2D([0], [0], color=ORANGE, lw=8, label="Carlos Alcaraz")], frameon=False, loc="lower left", bbox_to_anchor=(0,1.01), ncol=2, fontsize=10)
save(fig, "02-rivalry-surfaces", "Source: saved match records from the CrawlPlant database, 23 Oct 2026. 17 completed meetings; retirements and exhibitions excluded.\nSource coverage, not an independently audited official record. Two grass matches are a small sample.")

match = load("wimbledon-2024-points.json")
games = match["pointByPoint"]
fig, ax = frame("The scoreline leaves out the pressure", "Wimbledon 2024 final  ·  Alcaraz vs Djokovic  ·  6–2  6–2  7–6(4)", 7.3)
for i, g in enumerate(games, 1):
    if g.get("tiebreak"):
        ax.axvspan(i-.45, i+.45, color="#e9dfb7")
        ax.text(i, 3.3, "TB", ha="center", fontsize=10, weight="bold")
        continue
    held = g["winner"] == g["server"]
    colour = GREEN if held else ORANGE
    ax.bar(i, g["breakPoints"], color=colour, width=.6)
    ax.scatter(i, -.3, c=colour, marker="o" if held else "X", s=42, clip_on=False)
    ax.text(i, -.75, "A" if g["server"] == "player1" else "D", ha="center", fontsize=8, color=MUTED)
    if g["breakPoints"]: ax.text(i, g["breakPoints"]+.14, str(g["breakPoints"]), ha="center", fontsize=10)
for cut in (8.5, 16.5): ax.axvline(cut, color=GRID, lw=1.4)
for xpos, label in ((4.5, "SET 1"), (12.5, "SET 2"), (23, "SET 3")): ax.text(xpos, 5.95, label, ha="center", fontsize=10, color=MUTED, weight="bold")
ax.set(xlim=(.3, 29.7), ylim=(-1.1, 6.3), ylabel="Break-point opportunities", xlabel="Match game number · A / D below each game identifies the server", xticks=[1,4,8,9,12,16,17,20,24,28,29])
ax.set_yticks(range(0, 6))
ax.legend(handles=[Line2D([0],[0],marker="o",color=GREEN,lw=0,label="Server held"),Line2D([0],[0],marker="X",color=ORANGE,lw=0,label="Server broken")],frameon=False, loc="upper right")
save(fig, "03-wimbledon-pressure", "Source: recorded Flashscore point feed Sf0bExdB, parsed with the production parser. A = Alcaraz; D = Djokovic.\n29 entries: 28 service games + a tiebreak. Bars count opportunities, not a win-probability model.")

fig, ax = frame("Where Elo and the market disagree", "Eight largest absolute gaps  ·  both probabilities refer to the first named player", 8)
for i, row in enumerate(market[:8]):
    a, b = row["elo"]*100, row["market"]*100
    ax.plot([a,b],[i,i],color=GRID,lw=5,zorder=1)
    ax.scatter(a,i,c=GREEN,s=70,zorder=2)
    ax.scatter(b,i,c=ORANGE,s=70,zorder=2)
    ax.text(101,i,f"{row['gap_pp']:+.1f} pp",va="center",ha="left",fontsize=10,weight="bold")
ax.set(yticks=range(8),yticklabels=[f"{r['player1']}  /  {r['player2']}" for r in market[:8]],xlim=(0,100),xlabel="First named player's win probability (%)")
ax.invert_yaxis()
ax.grid(axis="x",color=GRID,lw=.6)
fig.subplots_adjust(left=.31,right=.87)
ax.legend(handles=[Line2D([0],[0],marker="o",color=GREEN,lw=0,label="Pre-match Elo"),Line2D([0],[0],marker="o",color=ORANGE,lw=0,label="Retrieved closing market")],frameon=False, loc="lower left",bbox_to_anchor=(0,1.01),ncol=2,fontsize=10)
save(fig, "04-elo-market", "Source: existing Actor run, 22 Oct 2026; 18/20 rows have both probabilities. GB bookmakers.\nFinished-match retrospective. Prices were retrieved after play; this is not a pre-match signal or a backtest.")

fig, ax = frame("The join is part of the result", "Match-table rows with a matching point stream in the two saved exports")
for i,tour in enumerate(("atp","wta")):
    group=[r for r in joined if r["tour"]==tour]
    yes=sum(r["has_points"] for r in group)
    ax.barh(i,len(group),color=GRID,height=.5)
    ax.barh(i,yes,color=GREEN,height=.5)
    ax.text(len(group)+3,i,f"{yes}/{len(group)}  ·  {yes/len(group):.1%}",va="center",fontsize=12,weight="bold")
ax.set(yticks=[0,1],yticklabels=["ATP","WTA"],xlim=(0,180),xlabel="Matches in the saved cohort")
ax.invert_yaxis()
ax.legend(handles=[Line2D([0],[0],color=GREEN,lw=8,label="Point stream joined"),Line2D([0],[0],color=GRID,lw=8,label="No point row in this export")],frameon=False,loc="lower left",bbox_to_anchor=(0,1.01),ncol=2,fontsize=10)
save(fig,"05-point-coverage","233 match rows + 116 matching point streams = 49.8% overlap. Saved runs: 22 Oct 2026.\nDifferent run filters: unmatched rows do not prove that point data is unavailable at the source.")

fig, ax = frame("Start wide. End at a single point.", "Four Actors, one research question  ·  follow stable IDs between levels", 8)
ax.set_axis_off()
steps=[("01","MATCH DATASET","Define a cohort","match_id · winner_id · loser_id"),
       ("02","MATCH HISTORY","Add prior player context","playerId · matchId · startTime"),
       ("03","FLASHSCORE TENNIS","Inspect the selected match","matchId · Elo · form · odds"),
       ("04","POINT-BY-POINT","Replay the pressure","matchId / pbp_id · games / stream")]
for i,(number,title,desc,keys) in enumerate(steps):
    y=.91-i*.25
    ax.text(.01,y,number,fontsize=25,color=GREEN,weight="bold",transform=ax.transAxes)
    ax.text(.12,y+.025,title,fontsize=12,weight="bold",transform=ax.transAxes)
    ax.text(.12,y-.04,desc,fontsize=17,transform=ax.transAxes)
    ax.text(.59,y-.02,keys,fontsize=10,color=MUTED,transform=ax.transAxes)
    if i<3: ax.annotate("",xy=(.035,y-.16),xytext=(.035,y-.04),xycoords=ax.transAxes,arrowprops={"arrowstyle":"->","color":GRID,"lw":2})
save(fig,"06-workflow","Use only the levels your question needs. Keep timestamps, sample sizes and missing coverage attached.\nCrawlPlant tennis family · independent tools · no affiliation with Flashscore, ATP, WTA or Jeff Sackmann.")

from ai_assets import build_ai_assets
build_ai_assets(ROOT, frame, save)


from reports import build_reports
build_reports(ROOT, frame, save)
print("Created PNG/SVG figures and Markdown/JSON reports in assets/ and reports/.")
