import pandas as pd

from pathlib import Path

INPUT_PATH = Path("data/clean/events.csv")
OUTPUT_PATH = Path("data/transformed/events.csv")

df = pd.read_csv(INPUT_PATH)

# TRANSFORMATIONS

# temporarily convert to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# add column, format into YYYY-MM-DD
df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)
