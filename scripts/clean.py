import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -----------------------------
# 1. Normalize blank strings
# -----------------------------
df = df.replace(r"^\s*$", pd.NA, regex=True)

# -----------------------------
# 2. Parse + coerce types
# -----------------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------------
# 3. Drop rows with ANY missing value
# -----------------------------
df = df.dropna().copy()

# -----------------------------
# 4. Filter valid event types
# -----------------------------
valid_event_types = {"click", "login", "purchase", "scroll", "view"}
df = df[df["event_type"].isin(valid_event_types)].copy()

# -----------------------------
# 5. Remove invalid durations
# -----------------------------
df = df[df["duration_seconds"] > 0].copy()

# -----------------------------
# 6. Ensure integer duration
# -----------------------------
df["duration_seconds"] = df["duration_seconds"].astype(int)

# -----------------------------
# 7. FORCE string ISO format (important fix)
# -----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.strftime(
    "%Y-%m-%dT%H:%M:%S"
)

# -----------------------------
# 8. Final safety drop (in case formatting created NA)
# -----------------------------
df = df.dropna(subset=["timestamp"]).copy()

# -----------------------------
# 9. Save
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)