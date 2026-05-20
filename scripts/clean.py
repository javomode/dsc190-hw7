import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -----------------------------
# 1. Remove blank strings early
# -----------------------------
df = df.replace(r"^\s*$", pd.NA, regex=True)

# -----------------------------
# 2. Parse timestamp FIRST and immediately normalize to string
# -----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

# -----------------------------
# 3. Convert numeric AFTER timestamp fix
# -----------------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# -----------------------------
# 4. Drop missing AFTER all parsing
# -----------------------------
df = df.dropna(subset=["event_type", "duration_seconds", "timestamp"]).copy()

# -----------------------------
# 5. Filter event types
# -----------------------------
valid_event_types = {"click", "login", "purchase", "scroll", "view"}
df = df[df["event_type"].isin(valid_event_types)].copy()

# -----------------------------
# 6. Remove invalid durations
# -----------------------------
df = df[df["duration_seconds"] > 0].copy()
df["duration_seconds"] = df["duration_seconds"].astype(int)

# -----------------------------
# 7. Final safety: ensure strict string type
# -----------------------------
df["timestamp"] = df["timestamp"].astype(str)

# -----------------------------
# 8. Save
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)