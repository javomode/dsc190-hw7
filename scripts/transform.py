import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/clean/events.csv")
OUTPUT_PATH = Path("data/transformed/events.csv")

df = pd.read_csv(INPUT_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")

# Re-format timestamp back to ISO 8601 with T separator
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)