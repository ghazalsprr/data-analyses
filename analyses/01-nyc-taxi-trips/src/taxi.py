"""Loading, cleaning and feature engineering for the NYC taxi trips analysis.

The raw file is a 6,433-trip sample of NYC TLC yellow and green cab records
from March 2019 (distributed with the seaborn example datasets).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_DIR / "data" / "raw" / "taxis.csv"
PROCESSED_PATH = PROJECT_DIR / "data" / "processed" / "taxis_clean.csv"

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DISTANCE_BINS = [0, 1, 2, 5, 10, 40]
DISTANCE_LABELS = ["0-1 mi", "1-2 mi", "2-5 mi", "5-10 mi", "10+ mi"]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Read the raw trip records with pickup/dropoff parsed as datetimes."""
    return pd.read_csv(path, parse_dates=["pickup", "dropoff"])


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive duration, speed, time-of-day and tip features."""
    out = df.copy()
    out["duration_min"] = (out["dropoff"] - out["pickup"]).dt.total_seconds() / 60
    out["speed_mph"] = out["distance"] / (out["duration_min"] / 60)
    out["fare_per_mile"] = out["fare"] / out["distance"]
    out["hour"] = out["pickup"].dt.hour
    out["day_of_week"] = pd.Categorical(out["pickup"].dt.day_name(), DAY_ORDER, ordered=True)
    out["is_weekend"] = out["pickup"].dt.dayofweek >= 5
    out["is_airport"] = (
        out["pickup_zone"].str.contains("Airport", na=False)
        | out["dropoff_zone"].str.contains("Airport", na=False)
    )
    out["distance_band"] = pd.cut(out["distance"], DISTANCE_BINS, labels=DISTANCE_LABELS)
    # Tip as a share of the metered fare. Only meaningful for card payments:
    # cash tips are not recorded in TLC data (they are always 0).
    out["tip_pct"] = (out["tip"] / out["fare"] * 100).where(out["payment"] == "credit card")
    return out


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop records that cannot be real trips.

    Returns the cleaned frame and a one-row-per-rule log of how many rows
    each rule removed, so the filtering is auditable.
    """
    df = add_features(df)
    rules = {
        "pickup outside March 2019": ~df["pickup"].between("2019-03-01", "2019-04-01"),
        "zero distance": df["distance"] <= 0,
        "duration under 1 min or over 3 h": ~df["duration_min"].between(1, 180),
        "non-positive fare": df["fare"] <= 0,
        "implausible speed (> 70 mph)": df["speed_mph"] > 70,
    }
    keep = pd.Series(True, index=df.index)
    log = []
    for name, bad in rules.items():
        removed = int((keep & bad).sum())
        keep &= ~bad
        log.append({"rule": name, "rows_removed": removed})
    log_df = pd.DataFrame(log)
    return df[keep].reset_index(drop=True), log_df


def load_clean(save: bool = True) -> pd.DataFrame:
    """Load, clean and optionally write the processed dataset."""
    df, _ = clean(load_raw())
    if save:
        PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(PROCESSED_PATH, index=False)
    return df


if __name__ == "__main__":
    cleaned, removed = clean(load_raw())
    print(removed.to_string(index=False))
    print(f"\n{len(cleaned):,} trips kept")
