import fastf1
from typing import Union

from src.rate_limiter import AdaptiveRateLimiter
from src.logging_config import setup_logging
from src.config import Config

logger, error_logger = setup_logging()

# ------------------------------------------------------------
# Global rate limiter (simple, deterministic)
# ------------------------------------------------------------
_rate_limiter = AdaptiveRateLimiter(1.0, 30.0)

# ------------------------------------------------------------
# FastF1 initialization
# ------------------------------------------------------------
def setup_fastf1(cache_dir=None):
    """
    Initialize FastF1 with an explicit cache directory.
    This is REQUIRED by the installed FastF1 version.
    """
    try:
        if cache_dir is None:
            cache_dir = Config.FASTF1_CACHE_DIR

        fastf1.Cache.enable_cache(cache_dir)
        logger.info(f"FastF1 cache enabled at: {cache_dir}")

    except Exception:
        error_logger.error("Failed to initialize FastF1 cache", exc_info=True)
        raise

# ------------------------------------------------------------
# Load a single race session (RACE ONLY)
# ------------------------------------------------------------
def load_race(
    year: int,
    round_no: Union[int, str],
    session: str = "R"
):
    """
    Load a single race session using FastF1.

    Parameters
    ----------
    year : int
        Season year (e.g., 2022)
    round_no : int or str
        Official round number (preferred) or GP name
    session : str
        Session type ("R" = Race)

    Returns
    -------
    fastf1.core.Session
    """

    if round_no is None:
        raise ValueError("round_no must not be None")

    logger.info(
        f"Requesting session — Year={year}, Round={round_no}, Session={session}"
    )

    # Simple throttling (no adaptive feedback)
    _rate_limiter.wait()

    try:
        session_data = fastf1.get_session(year, round_no, session)
        session_data.load()

        logger.info(
            f"Loaded session successfully — "
            f"Year={year}, Round={round_no}, Session={session}"
        )

        return session_data

    except Exception:
        error_logger.error(
            f"FastF1 failed — Year={year}, Round={round_no}, Session={session}",
            exc_info=True
        )
        raise
