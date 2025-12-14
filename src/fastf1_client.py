import fastf1
import logging
from src.config import Config
from src.rate_limiter import AdaptiveRateLimiter

logger = logging.getLogger(__name__)
rate_limiter = AdaptiveRateLimiter()

def setup_fastf1():
    Config.FASTF1_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(Config.FASTF1_CACHE_DIR))

def load_race(year, gp_name, session="R"):
    try:
        rate_limiter.wait()
        session_data = fastf1.get_session(year, gp_name, session)
        session_data.load()
        rate_limiter.success()
        return session_data
    except Exception as e:
        rate_limiter.failure()
        logger.error(f"FastF1 error {year} {gp_name}", exc_info=True)
        raise
