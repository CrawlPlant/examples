"""Render the Wimbledon recap card from source records and validated evidence IDs."""
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


def render_recap_card(match, ledger, edit, output_prefix="wimbledon-recap", selection_kind="editorial"):
    # shortcut: canvas targets this final; add automatic layout before accepting other matches.
    if match.get("matchId") != "Sf0bExdB" or match.get("score") != "6-2 6-2 7-6(4)":
        raise ValueError("This card layout is for the recorded 2024 Wimbledon men's final")
    if (match.get("player1Name"), match.get("player2Name")) != ("Alcaraz C.", "Djokovic N."):
        raise ValueError("Player orientation does not match this card")
    if selection_kind not in ("editorial", "model"):
        raise ValueError("Unknown selection kind")
    by_id = {fact["id"]: fact for fact in ledger["facts"]}
    chosen = edit.get("fact_ids")
    if (not isinstance(chosen, list) or len(chosen) != 4 or not all(isinstance(key, str) for key in chosen)
            or "result" not in chosen or len(set(chosen)) != 4 or any(key not in by_id for key in chosen)):
        raise ValueError("Select result and exactly three distinct known event IDs")
    event_ids = [key for key in chosen if key != "result"]
    if any(len(textwrap.wrap(by_id[key]["text"], width=36)) > 4 for key in event_ids):
        raise ValueError("Selected event text exceeds this card's layout")
    games = match["pointByPoint"]
    ordinary = [g for g in games if not g.get("tiebreak")]
    if (ledger["matchId"] != match["matchId"] or len(games) != 29
            or ledger["ordinary_games"] != len(ordinary)
            or ledger["pressure_games"] != sum(g.get("breakPoints", 0) > 0 for g in ordinary)
            or ledger["break_point_opportunities"] != sum(g.get("breakPoints", 0) for g in ordinary)
            or ledger["tiebreaks"] != sum(bool(g.get("tiebreak")) for g in games)):
        raise ValueError("Source records and evidence counts do not match")

    INK, GREEN, MINT = "#16352f", "#087f6f", "#85d3bd"
    ORANGE, PAPER, MUTED, GRID = "#bd4b2b", "#faf8f2", "#64756e", "#dce2d9"
    fig = plt.figure(figsize=(16, 18), dpi=100, facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1600), ylim=(1800, 0))
    ax.axis("off")
    texts = []

    def text(x, y, value, size=16, colour=INK, weight="normal", **kwargs):
        obj = ax.text(x, y, value, fontsize=size, color=colour, weight=weight,
                      family="DejaVu Sans", va="top", linespacing=1.35, **kwargs)
        texts.append(obj)
        return obj

    def card(x, y, w, h, colour="white", edge="none", radius=18):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                                  facecolor=colour, edgecolor=edge, linewidth=1))

    ax.add_patch(Rectangle((0, 0), 1600, 477, facecolor=INK))
    text(80, 48, "CRAWLPLANT  /  TENNIS DATA LAB", 15, MINT, "bold")
    text(80, 97, "WIMBLEDON 2024  ·  MEN'S FINAL  ·  14 JULY", 13, "#c5dbd1")
    text(80, 150, "Alcaraz finishes in straight sets.", 39, PAPER, "bold")
    text(80, 236, "CARLOS ALCARAZ", 23, PAPER, "bold")
    text(80, 315, "NOVAK DJOKOVIC", 23, "#c5dbd1", "bold")
    for i, token in enumerate(match["score"].split()):
        x, label = (960, 1165, 1370)[i], f"SET {i+1}"
        a, d = token.split("(")[0].split("-")
        text(x, 213, label, 11, MINT, "bold", ha="center")
        text(x, 240, a, 35, PAPER, "bold", ha="center")
        text(x, 319, d, 35, "#c5dbd1", ha="center")
    text(1450, 338, "("+match["score"].split("(")[-1], 16, MINT)
    text(80, 412, "An opening break. A late reply. A 7–4 tiebreak to finish.", 19, "#d9e5dd")

    for x, value, label in ((80, f"{ledger['pressure_games']} / {ledger['ordinary_games']}", "Service games with break points"),
                            (570, str(ledger["break_point_opportunities"]), "Break-point opportunities"),
                            (1060, str(ledger["tiebreaks"]), "Separate tiebreak")):
        card(x, 518, 460, 124, edge=GRID)
        text(x+25, 534, value, 33, GREEN, "bold")
        text(x+25, 596, label, 13, MUTED)

    text(80, 692, "Pressure, game by game", 25, INK, "bold")
    text(80, 745, "Break-point opportunities faced by the server", 14, MUTED)
    text(1140, 745, "A  Alcaraz     D  Djokovic", 13, MUTED)
    start, step, baseline, scale = 145, 46, 1000, 30
    for count in (0, 1, 3, 5):
        y = baseline - count * scale
        ax.plot([115, 1490], [y, y], color=GRID, lw=.8, zorder=0)
        text(95, y-9, str(count), 11, MUTED, ha="right")
    for index, g in enumerate(games):
        x = start + index * step
        if g.get("tiebreak"):
            card(x-20, 837, 40, 206, "#eee6c9", radius=8)
            text(x, 903, "TB", 12, INK, "bold", ha="center")
            text(x, 933, g["points"][-1].replace(":", "–"), 11, MUTED, ha="center")
            continue
        colour = GREEN if g["server"] == "player1" else ORANGE
        n = g["breakPoints"]
        if n:
            ax.add_patch(Rectangle((x-12, baseline-n*scale), 24, n*scale, facecolor=colour))
            text(x, baseline-n*scale-27, str(n), 13, colour, "bold", ha="center")
        else:
            ax.plot(x, baseline, marker="o", markersize=3, color=GRID)
        text(x, 1020, "A" if g["server"] == "player1" else "D", 10, colour, "bold", ha="center")
        if g["server"] != g["winner"]:
            text(x, 1050, "×", 14, INK, "bold", ha="center")
        text(x, 1080, str(g["game"]), 8, MUTED, ha="center")
    for left, right, label in ((0, 7, "SET 1"), (8, 15, "SET 2"), (16, 28, "SET 3")):
        text(start+(left+right)*step/2, 796, label, 12, GREEN, "bold", ha="center")
    for cut in (7.5, 15.5):
        ax.plot([start+cut*step]*2, [826, 1083], color=GRID, lw=1.3)
    text(80, 1120, "Bars = opportunities  ·  A / D = server  ·  × = server broken  ·  Bottom numbers = game within each set", 12, MUTED)

    text(80, 1172, "Three moments, with receipts", 25, INK, "bold")
    titles = {"set-1-game-1": "Opening pressure", "set-3-game-10": "The late reply", "set-3-game-13": "The finish"}
    events = [(f"{i+1:02}", titles.get(key, "Selected event"), by_id[key]["text"], key)
              for i, key in enumerate(event_ids)]
    source = f"https://www.flashscore.com/match/{match['matchId']}/"
    for index, (number, title, paragraph, event_id) in enumerate(events):
        x = 80+index*490
        card(x, 1232, 460, 235, edge=GRID)
        text(x+25, 1252, number, 12, GREEN, "bold")
        text(x+25, 1286, title, 19, INK, "bold")
        text(x+25, 1332, textwrap.fill(paragraph, width=36), 13, MUTED)
        text(x+25, 1440, event_id, 10, GREEN, url=source)

    text(80, 1512, "THE WORKFLOW SHOWN IN THE ARTICLE", 12, GREEN, "bold")
    for index, (title, detail) in enumerate((("Flashscore Tennis", "Match context"), ("Point-by-Point", "Recorded games"),
                                           ("Python ledger", "Counts + event IDs"), ("Recap card", "Selected, cited events"))):
        x = 80+index*372
        card(x, 1553, 330, 94, "#eaf0e7")
        text(x+18, 1568, title, 15, INK, "bold")
        text(x+18, 1604, detail, 12, MUTED)
        if index < 3:
            text(x+344, 1578, "→", 19, GREEN)

    text(80, 1688, f"SOURCE  {match['matchId']} · game-format records supplied to the renderer; see article for provenance.", 11, MUTED, url=source)
    selection_note = ("EDITORIAL EXAMPLE  Explicit event selection; the optional model API was not called." if selection_kind == "editorial"
                      else "MODEL-SELECTED EVENTS  Validated IDs; numerical statements are rendered from the evidence ledger.")
    text(80, 1723, selection_note, 11, MUTED)
    text(80, 1752, "Counts describe recorded events. They do not establish emotions or causes. Review selected events before sharing.", 11, MUTED)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for obj in texts:
        box = obj.get_window_extent(renderer)
        assert box.x0 >= 60 and box.x1 <= 1540 and box.y0 >= 15 and box.y1 <= 1770, obj.get_text()

    prefix = Path(output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    png = prefix.with_suffix(".png")
    svg = prefix.with_suffix(".svg")
    fig.savefig(png, dpi=100, facecolor=PAPER)
    fig.savefig(svg, facecolor=PAPER)
    plt.close(fig)
    return {"png": str(png), "svg": str(svg), "event_ids": event_ids}


if __name__ == "__main__":
    import sys
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    from ai_examples import recap_evidence
    match = json.loads((root / "data/wimbledon-2024-points.json").read_text(encoding="utf-8"))
    ledger = recap_evidence(match)
    edit = {"fact_ids": ["result", "set-1-game-1", "set-3-game-10", "set-3-game-13"]}
    artifacts = render_recap_card(match, ledger, edit, root / "assets/13-illustrated-recap")
    print(json.dumps({"ordinary_games": ledger["ordinary_games"], "pressure_games": ledger["pressure_games"],
        "break_point_opportunities": ledger["break_point_opportunities"], "tiebreaks": ledger["tiebreaks"], **artifacts}, indent=2))
