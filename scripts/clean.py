import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# 1. Remove blank strings early
df = df.replace(r"^\s*$", pd.NA, regex=True)

# 2. Parse timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# 3. Convert numeric
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# 4. Drop rows with ANY missing field (covers all columns, including coerced NaT/NaN)
df = df.dropna().copy()

# 5. Now format timestamp to ISO 8601 (no NaT values remain, so strftime is safe)
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

# 6. Filter event types
valid_event_types = {"click", "login", "purchase", "scroll", "view"}
df = df[df["event_type"].isin(valid_event_types)].copy()

# 7. Remove invalid durations
df = df[df["duration_seconds"] > 0].copy()
df["duration_seconds"] = df["duration_seconds"].astype(int)

# 8. Save
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)