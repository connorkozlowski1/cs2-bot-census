# Ingestion Plan (Steam Web API only)

## Goals

- Collect 10,000+ CS2 player accounts.
- For each account, fetch:
  - Player summary (name, visibility, country, last logoff).
  - Owned games (to check CS2 ownership and playtime).
  - Friend list (degree and clustering).
  - CS2-specific stats (if exposed by `GetUserStatsForGame`).

## Seeding Strategy

1. Start from a manually curated list of known CS2 player SteamIDs (seed file: `data/raw/seed_steam_ids.csv`).
2. Expand via friend-of-friend sampling:
   - For each seed ID:
     - Get friend list.
     - Randomly sample friends to add to queue.
   - Continue until N unique CS2 owners collected.

## API Calls

- `GET ISteamUser/GetPlayerSummaries`
- `GET ISteamUser/GetFriendList`
- `GET IPlayerService/GetOwnedGames`
- `GET ISteamUserStats/GetUserStatsForGame` (for CS2 app id).

## Storage

- Raw JSON responses → `data/raw/steam_player_summaries/*.json`
- Processed tables:
  - `data/processed/accounts.csv`
  - `data/processed/account_friends.csv`
  - `data/processed/account_games.csv`
  - `data/processed/account_cs2_stats.csv`

## Rate Limits

- Basic backoff: sleep between requests, batch by 100 SteamIDs when using `GetPlayerSummaries`.
