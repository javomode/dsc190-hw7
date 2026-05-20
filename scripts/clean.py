import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# 1. valid event types
valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)]

# 2. numeric cleanup
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# 3. timestamp cleanup (ROBUST FIX)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# 4. drop missing REQUIRED fields only
df = df.dropna(subset=["event_type", "duration_seconds", "timestamp"])

# 5. filters
df = df[df["duration_seconds"] > 0]
df["duration_seconds"] = df["duration_seconds"].astype(int)

# 6. FORCE ISO FORMAT (key fix)
df.loc[:, "timestamp"] = df["timestamp"].apply(
    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S")
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)