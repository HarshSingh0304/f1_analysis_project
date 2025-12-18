import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Project root (authoritative)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]


class Config:
    # --------------------------------------------------------
    # Project
    # --------------------------------------------------------
    PROJECT_NAME = "f1_analysis_project"
    ENV = os.getenv("ENV", "development")

    # --------------------------------------------------------
    # Data paths
    # --------------------------------------------------------
    DATA_DIR = BASE_DIR / "data"

    RAW_DATA_DIR = DATA_DIR / "raw"
    FASTF1_CACHE_DIR = RAW_DATA_DIR / "fastf1_cache"

    INTERIM_DATA_DIR = DATA_DIR / "interim"
    STANDARDIZED_DATA_DIR = INTERIM_DATA_DIR / "standardized"

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def validate(cls):
        missing = []
        for key in ["DB_USER", "DB_PASSWORD", "DB_NAME"]:
            if getattr(cls, key) is None:
                missing.append(key)
        if missing:
            raise EnvironmentError(f"Missing env vars: {missing}")
