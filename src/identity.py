# src/identity.py
from pathlib import Path

def parse_race_identity(race_dir: Path):
    """
    Extract season, round, and race_id from standardized directory path.
    Example:
      year=2024/round=10_Spanish_Grand_Prix
    """
    season = int(race_dir.parts[-2].split("=")[1])
    round_ = int(race_dir.name.split("_")[0].split("=")[1])
    race_id = f"{season}_{round_}"
    return season, round_, race_id
