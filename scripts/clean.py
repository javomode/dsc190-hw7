import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

df = df.replace(r"^\s*$", pd.NA, regex=True)

valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)].copy()

df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

df = df.dropna(subset=["event_type", "duration_seconds", "timestamp"])

df = df[df["duration_seconds"] > 0].copy()

df["duration_seconds"] = df["duration_seconds"].astype(int)

df["timestamp"] = df["timestamp"].map(
    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S")
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)