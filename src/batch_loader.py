import logging
from src.fastf1_client import load_race

logger = logging.getLogger(__name__)

def load_multiple_years(years, gp_name):
    results = []

    for year in years:
        logger.info(f"Loading {gp_name} {year}")
        try:
            session = load_race(year, gp_name)
            results.append(session)
        except Exception:
            logger.error(f"Failed year {year}", exc_info=True)

    return results
