from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_PROCESSED_DIR = Path("data/processed")


def main() -> None:
    features_path = DATA_PROCESSED_DIR / "features_accounts.csv"
    if not features_path.exists():
        print("features_accounts.csv not found")
        return

    df = pd.read_csv(features_path)

    print("Shape:", df.shape)
    print("\nColumns:", list(df.columns))

    print("\nBasic summary (numeric):")
    print(df.describe())

    # crude "suspicious" flag v0:
    # - has_cs2 == 1
    # - cs2_hours_2weeks > 60
    # - account_age_days < 30 OR is_private == 1
    suspicious = df[
        (df["has_cs2"] == 1)
        & (df["cs2_hours_2weeks"] > 60)
        & ((df["account_age_days"] < 30) | (df["is_private"] == 1))
    ].copy()

    print("\nSuspicious candidates (v0 heuristic):")
    print(suspicious[["steam_id", "account_age_days", "cs2_hours_2weeks", "is_private"]])

    out_path = DATA_PROCESSED_DIR / "suspicious_candidates_v0.csv"
    suspicious.to_csv(out_path, index=False)
    print(f"\nWrote {out_path} with {len(suspicious)} rows")


if __name__ == "__main__":
    main()
