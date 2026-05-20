import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -------------------------------------------------
# 1. Standardize "missing" values (CRITICAL)
# -------------------------------------------------
df = df.replace(r"^\s*$", pd.NA, regex=True)

# -------------------------------------------------
# 2. Drop rows with ANY missing field
# -------------------------------------------------
df = df.dropna()

# -------------------------------------------------
# 3. Validate event_type
# -------------------------------------------------
valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)]

# -------------------------------------------------
# 4. Clean numeric field
# -------------------------------------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# must re-drop after coercion (important!)
df = df.dropna()
df = df[df["duration_seconds"] > 0]

df["duration_seconds"] = df["duration_seconds"].astype(int)

# -------------------------------------------------
# 5. Timestamp normalization (STRICT ISO 8601)
# -------------------------------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

df["timestamp"] = df["timestamp"].apply(
    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S")
)

# -------------------------------------------------
# 6. Write output
# -------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)