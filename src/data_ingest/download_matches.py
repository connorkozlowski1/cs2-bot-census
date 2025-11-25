from typing import List, Dict

def fetch_player_summaries(steam_ids: List[str]) -> Dict:
    """
    Call ISteamUser.GetPlayerSummaries for up to 100 SteamIDs at a time.
    Returns the raw JSON response.
    """
    pass

def fetch_owned_games(steam_id: str) -> Dict:
    """
    Call IPlayerService.GetOwnedGames for a single SteamID.
    Returns the raw JSON response.
    """
    pass

def fetch_friend_list(steam_id: str) -> Dict:
    """
    Call ISteamUser.GetFriendList for a single SteamID.
    Returns the raw JSON response.
    """
    pass

def fetch_cs2_stats(steam_id: str) -> Dict:
    """
    Optional: Call ISteamUserStats.GetUserStatsForGame for CS2 app id.
    Returns the raw JSON response.
    """
    pass

def crawl_accounts(seed_ids: List[str], max_accounts: int = 10000) -> None:
    """
    BFS/expansion over the friend graph starting from seed_ids.
    Writes raw JSON files under data/raw/.
    """
    pass
