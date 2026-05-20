import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -----------------------
# 1. VALID EVENT TYPES
# -----------------------
valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)]

# -----------------------
# 2. NUMERIC CLEANING
# -----------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# -----------------------
# 3. TIMESTAMP CLEANING
# -----------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------
# 4. DROP ANY ROW WITH MISSING VALUES
#    (THIS FIXES YOUR "blank fields" ERROR)
# -----------------------
df = df.dropna()

# -----------------------
# 5. FILTER POSITIVE DURATIONS
# -----------------------
df = df[df["duration_seconds"] > 0]
df["duration_seconds"] = df["duration_seconds"].astype(int)

# -----------------------
# 6. FINAL ISO FORMAT (THIS FIXES TIMESTAMP ERROR)
# -----------------------
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)