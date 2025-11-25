Data Sources:
Steam Web API (ISteamUser.GetPlayerSummaries, ISteamUser.GetFriendList, IPlayerService.GetOwnedGames, ISteamUserStats.GetUserStatsForGame for CS2 if available).

Scope:
v1 estimates bot-likelihood using account-level and coarse activity features only.

v2 may add per-match telemetry from third-party providers.
Sampling plan:
- Pull N recent players from public CS2 lobbies.
- For each player: fetch profile + match history metadata.
Rate-limit handling:
- Use rotating keys / backoff.

