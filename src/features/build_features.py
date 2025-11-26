from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

DATA_PROCESSED_DIR = Path("data/processed")


def unix_to_datetime(x):
    if pd.isna(x):
        return pd.NA
    try:
        return datetime.fromtimestamp(int(x), tz=timezone.utc)
    except Exception:
        return pd.NA


def build_features():
    accounts_path = DATA_PROCESSED_DIR / "accounts.csv"
    if not accounts_path.exists():
        print("accounts.csv not found in data/processed")
        return

    df = pd.read_csv(accounts_path)

    # account age in days
    now = datetime.now(timezone.utc)
    df["timecreated_dt"] = df["timecreated"].apply(unix_to_datetime)
    df["timecreated_dt"] = pd.to_datetime(df["timecreated_dt"], errors="coerce", utc=True)
    df["account_age_days"] = (now - df["timecreated_dt"]).dt.days

    # last logoff recency in days
    df["lastlogoff_dt"] = df["lastlogoff"].apply(unix_to_datetime)
    df["lastlogoff_dt"] = pd.to_datetime(df["lastlogoff_dt"], errors="coerce", utc=True)
    df["days_since_lastlogoff"] = (now - df["lastlogoff_dt"]).dt.days


    # visibility features
    # 1 = private, 3 = public (Steam convention)
    df["is_public"] = (df["communityvisibilitystate"] == 3).astype(int)
    df["is_private"] = (df["communityvisibilitystate"] != 3).astype(int)

    # CS2 ownership / playtime
    df["has_cs2"] = df["cs2_playtime_forever"].notna().astype(int)
    df["cs2_hours_total"] = (df["cs2_playtime_forever"].fillna(0) / 60.0)
    df["cs2_hours_2weeks"] = (df["cs2_playtime_2weeks"].fillna(0) / 60.0)

    # simple high-playtime flags
    df["cs2_hours_2weeks_over_50"] = (df["cs2_hours_2weeks"] > 50).astype(int)
    df["cs2_hours_2weeks_over_100"] = (df["cs2_hours_2weeks"] > 100).astype(int)

    # stats availability
    df["has_cs2_stats"] = df["has_cs2_stats"].astype(int)

    # keep a clean set of columns
    feature_cols = [
        "steam_id",
        "account_age_days",
        "days_since_lastlogoff",
        "is_public",
        "is_private",
        "has_cs2",
        "cs2_hours_total",
        "cs2_hours_2weeks",
        "cs2_hours_2weeks_over_50",
        "cs2_hours_2weeks_over_100",
        "has_cs2_stats",
    ]

    features = df[feature_cols].copy()
    out_path = DATA_PROCESSED_DIR / "features_accounts.csv"
    features.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(features)} rows")


if __name__ == "__main__":
    build_features()
