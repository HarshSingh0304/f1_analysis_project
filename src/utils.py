from pathlib import Path
import hashlib
import pandas as pd
from typing import Iterable


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
