import pandas as pd

from pathlib import Path

INPUT_PATH = Path("data/transformed/events.csv")
OUTPUT_PATH = Path("data/features/events.csv")

df = pd.read_csv(INPUT_PATH)

# FEATURES

# add column for duration in minutes
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="raise")
df["duration_minutes"] = df["duration_seconds"] / 60

# add column for name of day of the week
df["weekday"] = pd.to_datetime(df["timestamp"]).dt.day_name()


OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)