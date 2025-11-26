from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    return json.loads(text)


def build_account_row(steam_id: str) -> Dict[str, Any]:
    """
    For a single steam_id, read the raw JSON files and build
    one flat dict of account-level fields.
    """
    summaries_path = RAW_DIR / f"{steam_id}_player_summaries.json"
    games_path = RAW_DIR / f"{steam_id}_owned_games.json"
    stats_path = RAW_DIR / f"{steam_id}_cs2_stats.json"

    summaries = load_json(summaries_path)
    games = load_json(games_path)
    stats = load_json(stats_path)

    # --- player summary ---
    player = None
    try:
        player = summaries["response"]["players"][0]
    except (KeyError, IndexError):
        player = {}

    # --- owned games: find CS2 (appid 730) ---
    cs2_info = {}
    try:
        for g in games["response"].get("games", []):
            if g.get("appid") == 730:
                cs2_info = g
                break
    except KeyError:
        cs2_info = {}

    # --- CS2 stats (optional, may be empty) ---
    cs2_stats = {}
    try:
        cs2_stats = stats["playerstats"]
    except KeyError:
        cs2_stats = {}

    row: Dict[str, Any] = {
        "steam_id": steam_id,
        # from player summary
        "personaname": player.get("personaname"),
        "communityvisibilitystate": player.get("communityvisibilitystate"),
        "profilestate": player.get("profilestate"),
        "timecreated": player.get("timecreated"),
        "lastlogoff": player.get("lastlogoff"),
        "personastate": player.get("personastate"),
        "realname": player.get("realname"),
        "country": player.get("loccountrycode"),
        # from CS2 owned game record
        "cs2_playtime_forever": cs2_info.get("playtime_forever"),
        "cs2_playtime_2weeks": cs2_info.get("playtime_2weeks"),
        "cs2_last_played": cs2_info.get("rtime_last_played"),
        # simple stats container flag
        "has_cs2_stats": bool(cs2_stats),
    }

    return row


def main() -> None:
    # Find all *_player_summaries.json files and extract steam_ids from filenames
    steam_ids = []
    for path in RAW_DIR.glob("*_player_summaries.json"):
        sid = path.name.split("_")[0]
        steam_ids.append(sid)

    if not steam_ids:
        print("No player_summaries files found in data/raw/")
        return

    rows = [build_account_row(sid) for sid in steam_ids]
    df = pd.DataFrame(rows)

    out_path = PROCESSED_DIR / "accounts.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} for {len(df)} accounts")


if __name__ == "__main__":
    main()

