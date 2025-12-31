from pathlib import Path
import hashlib
import pandas as pd
from typing import Iterable, Optional, Dict, Callable
from datetime import timedelta


# ============================================================
# Filesystem & generic helpers (UNCHANGED)
# ============================================================

def ensure_dir(path: Path) -> None:
    """
    Create a directory if it does not exist.
    Safe to call repeatedly.
    """
    path.mkdir(parents=True, exist_ok=True)


def dataframe_fingerprint(df: pd.DataFrame) -> str:
    """
    Create a stable hash of a DataFrame's structure and contents.
    Useful for caching, change detection, and reproducibility.
    """
    content = pd.util.hash_pandas_object(df, index=True).values
    return hashlib.md5(content).hexdigest()


def validate_dataframe_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    df_name: str = "DataFrame"
) -> None:
    """
    Raise a clear error if required columns are missing.
    """
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(
            f"{df_name} is missing required columns: {sorted(missing)}"
        )


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lowercase
    - snake_case
    - stripped whitespace
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def chunk_iterable(iterable, chunk_size: int):
    """
    Yield items from iterable in fixed-size chunks.
    Used for batch processing (years, races, sessions).
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


# ============================================================
# Domain normalization helpers (UNCHANGED)
# ============================================================

def normalize_lap_time_to_ms(value) -> Optional[int]:
    """
    Normalize lap time values to integer milliseconds.
    """
    if value is None or pd.isna(value):
        return None

    if isinstance(value, (pd.Timedelta, timedelta)):
        return int(value.total_seconds() * 1000)

    if isinstance(value, (int, float)):
        return int(value * 1000)

    if isinstance(value, str):
        try:
            minutes, seconds = value.split(":")
            total_seconds = int(minutes) * 60 + float(seconds)
            return int(total_seconds * 1000)
        except ValueError:
            return None

    return None


def normalize_tyre_compound(value) -> Optional[str]:
    """
    Normalize tyre compound representations to canonical values:
    SOFT / MEDIUM / HARD
    """
    if value is None or pd.isna(value):
        return None

    value = str(value).strip().upper()

    if value in {"SOFT", "S", "C5", "RED"}:
        return "SOFT"
    if value in {"MEDIUM", "M", "C4", "C3", "YELLOW"}:
        return "MEDIUM"
    if value in {"HARD", "H", "C2", "C1", "WHITE"}:
        return "HARD"

    return None


def normalize_track_status(value) -> Optional[str]:
    """
    Normalize track status codes to canonical values:
    GREEN / SC / RED
    """
    if value is None or pd.isna(value):
        return None

    value = str(value).strip().upper()

    if value in {"1", "GREEN"}:
        return "GREEN"
    if value in {"2", "3", "4", "SC", "VSC"}:
        return "SC"
    if value in {"5", "RED"}:
        return "RED"

    return None


# ============================================================
# NEW: schema-driven normalization utilities
# ============================================================

def normalize_time_columns_to_ms(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    Normalize all specified time-like columns to milliseconds (Int64).
    """
    df = df.copy()

    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .apply(normalize_lap_time_to_ms)
                .astype("Int64")
            )

    return df


def drop_unsafe_columns(
    df: pd.DataFrame,
    unsafe_columns: Iterable[str],
) -> pd.DataFrame:
    """
    Drop unsafe or contextual columns explicitly defined by schema.
    """
    df = df.copy()
    to_drop = [c for c in unsafe_columns if c in df.columns]
    return df.drop(columns=to_drop, errors="ignore")


# ============================================================
# NEW: strict schema enforcement (FINAL GUARANTEE)
# ============================================================

def enforce_schema(
    df: pd.DataFrame,
    stable_columns: Iterable[str],
    normalized_columns: Iterable[str],
    df_name: str
) -> pd.DataFrame:
    """
    Enforce strict schema invariants:
    - Keep ONLY stable + normalized columns
    - Fail if any required column is missing
    - Deterministic column ordering
    """
    stable_columns = list(stable_columns)
    normalized_columns = list(normalized_columns)

    allowed = stable_columns + normalized_columns

    validate_dataframe_columns(df, allowed, df_name)

    # Deterministic ordering: stable first, normalized second
    return df[allowed].copy()
