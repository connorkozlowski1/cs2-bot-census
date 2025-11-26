from typing import List, Dict, Any
import requests

from .config import require_steam_api_key

BASE_URL = "https://api.steampowered.com"


def fetch_player_summaries(steam_ids: List[str]) -> Dict[str, Any]:
    if not steam_ids:
        raise ValueError("steam_ids cannot be empty")
    if len(steam_ids) > 100:
        raise ValueError("Max 100 SteamIDs per call")

    api_key = require_steam_api_key()

    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": api_key,
        "steamids": ",".join(steam_ids),
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_owned_games(steam_id: str) -> Dict[str, Any]:
    api_key = require_steam_api_key()

    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_friend_list(steam_id: str) -> Dict[str, Any]:
    api_key = require_steam_api_key()

    url = f"{BASE_URL}/ISteamUser/GetFriendList/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "relationship": "all",
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        # friend list is private or API not allowed; just return empty
        print(f"Warning: could not fetch friend list (status {response.status_code})")
        return {}

    return response.json()



def fetch_cs2_stats(steam_id: str, app_id: int = 730) -> Dict[str, Any]:
    api_key = require_steam_api_key()

    url = f"{BASE_URL}/ISteamUserStats/GetUserStatsForGame/v2/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "appid": app_id,
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return {}

    return response.json()


if __name__ == "__main__":
    import json
    from pathlib import Path

    # replace with your real SteamID64 if needed
    test_steam_id = "76561199047100586"

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching player summaries...")
    summaries = fetch_player_summaries([test_steam_id])

    print("Fetching owned games...")
    owned_games = fetch_owned_games(test_steam_id)

    print("Fetching friend list...")
    friends = fetch_friend_list(test_steam_id)

    print("Fetching CS2 stats...")
    cs2_stats = fetch_cs2_stats(test_steam_id)

    # save to disk as JSON
    (raw_dir / f"{test_steam_id}_player_summaries.json").write_text(
        json.dumps(summaries, indent=2),
        encoding="utf-8",
    )
    (raw_dir / f"{test_steam_id}_owned_games.json").write_text(
        json.dumps(owned_games, indent=2),
        encoding="utf-8",
    )
    (raw_dir / f"{test_steam_id}_friends.json").write_text(
        json.dumps(friends, indent=2),
        encoding="utf-8",
    )
    (raw_dir / f"{test_steam_id}_cs2_stats.json").write_text(
        json.dumps(cs2_stats, indent=2),
        encoding="utf-8",
    )

    print("Saved raw JSON files to data/raw/")

