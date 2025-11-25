Objectives:
- Collect at least 5k unique CS2 accounts.
- For each account: profile data, last 20–50 matches, timestamps, performance stats (if available).

Steps:
1. Seed with a list of known-active CS2 players (e.g., random SteamID ranges + activity filter).
2. For each SteamID:
   - Call GetPlayerSummaries.
   - Filter out non-CS2 accounts.
   - Pull CS2 stats endpoint.
   - Request match history from selected public API.
3. Store raw JSON in data/raw/.
4. Parse into normalized tables:
   - accounts.csv
   - matches.csv
   - performance.csv
