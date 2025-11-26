import time
import json
from pathlib import Path
from typing import List, Set

from .download_matches import (
    fetch_player_summaries,
    fetch_owned_games,
    fetch_friend_list,
    fetch_cs2_stats,
)

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_seed_ids() -> List[str]:
    seed_path = Path("seed_ids.txt")
    if not seed_path.exists():
        print("seed_ids.txt not found.")
        return []
    ids = [line.strip() for line in seed_path.read_text().splitlines() if line.strip()]
    return ids


def save_json(obj, path: Path):
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def crawl(seed_ids: List[str], max_accounts: int = 50, delay: float = 1.0):
    """
    BFS-like expansion:
    - Start with seed IDs
    - For each ID, fetch data and save to raw/
    - Expand with their friend lists (when available)
    - Stop at max_accounts
    """
    visited: Set[str] = set()
    queue: List[str] = list(seed_ids)

    while queue and len(visited) < max_accounts:
        sid = queue.pop(0)

        if sid in visited:
            continue

        print(f"\nCollecting: {sid}")
        visited.add(sid)

        # fetch and save player summary
        try:
            summaries = fetch_player_summaries([sid])
            save_json(summaries, RAW_DIR / f"{sid}_player_summaries.json")
        except Exception as e:
            print(f"Error fetching summaries: {e}")

        # owned games
        try:
            owned = fetch_owned_games(sid)
            save_json(owned, RAW_DIR / f"{sid}_owned_games.json")
        except Exception as e:
            print(f"Error fetching owned games: {e}")

        # cs2 stats
        try:
            stats = fetch_cs2_stats(sid)
            save_json(stats, RAW_DIR / f"{sid}_cs2_stats.json")
        except Exception as e:
            print(f"Error fetching CS2 stats: {e}")

        # friends -> queue expansion
        try:
            friends = fetch_friend_list(sid)
            save_json(friends, RAW_DIR / f"{sid}_friends.json")

            # Only expand if the friend list exists
            if "friendslist" in friends:
                for f in friends["friendslist"]["friends"]:
                    friend_id = f.get("steamid")
                    if friend_id and friend_id not in visited:
                        queue.append(friend_id)
        except Exception as e:
            print(f"Error fetching friend list: {e}")

        # basic rate limit
        time.sleep(delay)

    print(f"\nDone. Collected {len(visited)} accounts.")


def main():
    seeds = load_seed_ids()
    if not seeds:
        print("No seed IDs found, exiting.")
        return

    crawl(seeds, max_accounts=50)  # limited, went from 5 to 50


if __name__ == "__main__":
    main()
