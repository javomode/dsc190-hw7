import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -----------------------------
# 1. Normalize empty strings
# -----------------------------
df = df.replace(r"^\s*$", pd.NA, regex=True)

# -----------------------------
# 2. Convert types FIRST
# -----------------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------------
# 3. Drop ANY row with missing values (after conversion)
# -----------------------------
df = df.dropna()

# -----------------------------
# 4. Filter valid event types
# -----------------------------
valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)].copy()

# -----------------------------
# 5. Remove invalid durations
# -----------------------------
df = df[df["duration_seconds"] > 0].copy()
df["duration_seconds"] = df["duration_seconds"].astype(int)

# -----------------------------
# 6. Normalize timestamp to ISO 8601
# -----------------------------
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

# -----------------------------
# 7. Save output
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)