import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/transformed/events.csv")
OUTPUT_PATH = Path("data/features/events.csv")

df = pd.read_csv(INPUT_PATH)

df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="raise")
df["duration_minutes"] = df["duration_seconds"] / 60

ts = pd.to_datetime(df["timestamp"])
df["weekday"] = ts.dt.day_name()
# Preserve ISO 8601 format with T separator
df["timestamp"] = ts.dt.strftime("%Y-%m-%dT%H:%M:%S")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)