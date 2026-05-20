import pandas as pd

from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# CLEANING

# keep only valid event types
valid_event_types = {'click', 'login', 'scroll', 'view', 'buy', 'purchase'}
df = df[df["event_type"].isin(valid_event_types)]

# keep only positive durations
df = df[df["duration_seconds"] > 0]

# normalize timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="mixed",
    errors="coerce"
)

df = df.dropna()

df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)