import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")

df = pd.read_csv(INPUT_PATH)

# -------------------------------------------------
# 1. Standardize missing values
# -------------------------------------------------
df = df.replace(r"^\s*$", pd.NA, regex=True)

# -------------------------------------------------
# 2. Validate event_type FIRST
# -------------------------------------------------
valid_event_types = {'click', 'login', 'purchase', 'scroll', 'view'}
df = df[df["event_type"].isin(valid_event_types)].copy()

# -------------------------------------------------
# 3. Numeric cleanup
# -------------------------------------------------
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# -------------------------------------------------
# 4. Timestamp cleanup
# -------------------------------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -------------------------------------------------
# 5. NOW drop ALL invalid rows once (critical fix)
# -------------------------------------------------
df = df.dropna()
df = df[df["duration_seconds"] > 0].copy()

df["duration_seconds"] = df["duration_seconds"].astype(int)

# -------------------------------------------------
# 6. Force strict ISO format
# -------------------------------------------------
df["timestamp"] = df["timestamp"].map(
    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S")
)

# -------------------------------------------------
# 7. Output
# -------------------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)