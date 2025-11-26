# CS2 Bot Census

Estimate the share of bot accounts in Counter-Strike 2 using public match and account data.

## Objectives

- Collect a large sample of CS2 player accounts.
- Engineer behavioral and account-level features.
- Use rules + anomaly detection to estimate which accounts are likely bots.
- Publish:
  - A bot-rate estimate over the sample.
  - A dashboard to explore results.
  - A transparent methodology report.

## Status

- [x] Project spec
- [x] Data source exploration
- [x] Data ingestion pipeline
- [ ] Feature engineering
- [ ] Modeling + evaluation
- [ ] Dashboard deployment
- [ ] Final report


## Environment
- Python 3.11+
- Copy the template env file:

      copy .env.example .env

- Then open `.env` and set:

      STEAM_API_KEY=your_real_steam_api_key_here
