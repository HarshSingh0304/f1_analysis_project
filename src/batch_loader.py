from typing import List
import fastf1
from src.fastf1_client import load_race
from src.logging_config import setup_logging

logger, error_logger = setup_logging()


def load_season_races(year: int):
    """
    Load ALL race sessions ("R") for a given Formula 1 season.

    Rules (derived empirically from FastF1 diagnostics):
    - Use fastf1.get_event_schedule(year)
    - Ignore testing sessions (RoundNumber == 0)
    - Each RoundNumber >= 1 corresponds to exactly one race weekend
    - Race session is always session type "R"
    """

    logger.info(f"Fetching race schedule for season {year}")

    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception:
        error_logger.error(
            f"Failed to fetch event schedule for season {year}",
            exc_info=True
        )
        raise

    # Filter valid race weekends only
    race_events = schedule[
        (schedule["RoundNumber"] >= 1) &
        (schedule["EventFormat"] != "testing")
    ]

    total_races = len(race_events)
    logger.info(f"Discovered {total_races} race weekends for season {year}")

    race_sessions = []
    success_count = 0

    for _, event in race_events.iterrows():
        round_number = int(event["RoundNumber"])
        event_name = event["EventName"]

        logger.info(
            f"Loading race session — {year} Round {round_number}: {event_name}"
        )

        try:
            session = load_race(year, round_number)
            race_sessions.append(session)
            success_count += 1
        except Exception:
            error_logger.error(
                f"Failed to load race — {year} Round {round_number}: {event_name}",
                exc_info=True
            )
            continue

    logger.info(
        f"Season {year} completed — "
        f"{success_count}/{total_races} races loaded successfully"
    )

    return race_sessions


def load_multiple_years(years: List[int]):
    """
    Load race sessions for multiple seasons.
    Returns a dict: {year: [race_sessions]}
    """

    all_sessions = {}

    for year in years:
        try:
            all_sessions[year] = load_season_races(year)
        except Exception:
            error_logger.error(
                f"Failed to load season {year}",
                exc_info=True
            )
            all_sessions[year] = []

    return all_sessions
