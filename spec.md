Data Sources:
- Steam Web API (GetPlayerSummaries, GetFriendList, GetUserStatsForGame).
- CS2 match history endpoints from public community APIs (document the exact ones once chosen).
Sampling plan:
- Pull N recent players from public CS2 lobbies.
- For each player: fetch profile + match history metadata.
Rate-limit handling:
- Use rotating keys / backoff.

