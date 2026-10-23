"""Small building blocks used in the articles. Importing this file makes no API calls."""
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def call_actor(slug, run_input):
    from apify_client import ApifyClient

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(f"crawlplant/{slug}").call(run_input=run_input)
    if not run or run["status"] != "SUCCEEDED":
        raise RuntimeError(f"Actor did not succeed: {run and run['status']}")
    rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    if len(rows) >= run_input["maxItems"]:
        raise RuntimeError("Result reached maxItems; narrow the range or increase the cap before claiming completeness.")
    return rows


def update_dataset(old_rows, new_rows):
    # Refresh an overlap window: corrected rows replace the same match id.
    by_id = {}
    for row in [*old_rows, *new_rows]:
        key = row.get("match_id")
        if not key:
            raise ValueError("A match_id is required for an update")
        by_id[key] = row
    return list(by_id.values())


def rivalry_by_surface(rows, player_id):
    totals = {}
    seen = set()
    for row in rows:
        if row.get("status") != "finished" or row.get("winner") not in ("player1", "player2"):
            continue
        if row["matchId"] in seen:
            continue
        seen.add(row["matchId"])
        side = next((s for s in ("player1", "player2") if (row.get(s) or {}).get("playerId") == player_id), None)
        if side is None:
            raise ValueError("The chosen player is absent from a returned match")
        surface = row.get("surface") or "unknown"
        total = totals.setdefault(surface, {"wins": 0, "losses": 0})
        total["wins" if row["winner"] == side else "losses"] += 1
    return totals


def pressure_games(match):
    games = match.get("pointByPoint")
    if not games:
        raise ValueError("No game-level points; select pointByPointFormat='games' and check coverage")
    result = []
    for game in games:
        if game.get("tiebreak") or game.get("server") not in ("player1", "player2"):
            continue
        if game.get("winner") not in ("player1", "player2"):
            continue
        faced = game.get("breakPoints")
        if faced is None or faced < 1:
            continue
        result.append({"set": game["set"], "game": game["game"], "server": game["server"],
                       "opportunities": faced, "held": game["winner"] == game["server"]})
    return result


def market_comparison(rows):
    out = []
    for row in rows:
        elo = row.get("player1EloWinProbability")
        market = (row.get("odds") or {}).get("player1Probability")
        if elo is None or market is None:
            continue
        if not all(isinstance(p, (int, float)) and math.isfinite(p) and 0 <= p <= 1 for p in (elo, market)):
            raise ValueError("Probabilities must be finite numbers between zero and one")
        out.append({"matchId": row["matchId"], "player1": row["player1Name"], "player2": row["player2Name"],
                    "elo": elo, "market": market, "gap_pp": 100 * (elo - market), "status": row.get("status")})
    return sorted(out, key=lambda x: abs(x["gap_pp"]), reverse=True)


def join_points(matches, points):
    by_id = {}
    for row in points:
        key = row.get("pbp_id")
        if not key or key in by_id:
            raise ValueError("Point streams need unique pbp_id values")
        stream = row.get("pbp")
        if not isinstance(stream, str):
            raise ValueError("Expected a Sackmann point stream")
        unexpected = set(stream) - set("SRAD;./")
        if unexpected:
            raise ValueError(f"Unknown point symbols: {unexpected}")
        by_id[key] = row
    result = []
    for row in matches:
        point_row = by_id.get(row["match_id"])
        result.append({**row, "has_points": point_row is not None,
                       "recorded_points": sum(c in "SRAD" for c in point_row["pbp"]) if point_row else None})
    return result


def write_snapshot(path, rows):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


if __name__ == "__main__":
    load = lambda name: json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
    matches = load("tennis-match-dataset.json")
    joined = join_points(matches, load("tennis-point-by-point.json"))
    report = {"matches": len(matches), "matches_with_points": sum(r["has_points"] for r in joined),
              "elo_market_rows": len(market_comparison(load("flashscore-tennis.json"))),
              "wimbledon_pressure_games": len(pressure_games(load("wimbledon-2024-points.json")))}
    print(json.dumps(report, indent=2))
