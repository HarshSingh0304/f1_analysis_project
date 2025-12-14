import logging
from pathlib import Path


def _get_project_root() -> Path:
    """
    Resolve project root reliably regardless of where code is executed from.
    Assumes this file lives in: project_root/src/logging_config.py
    """
    return Path(__file__).resolve().parents[1]


def setup_logging():
    project_root = _get_project_root()
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    project_log_path = log_dir / "project.log"
    error_log_path = log_dir / "errors.log"

    # ------------------------------------------------------------------
    # Root logger (avoid duplicate handlers in Jupyter)
    # ------------------------------------------------------------------
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Project log file
        file_handler = logging.FileHandler(project_log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # Console output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)

    # ------------------------------------------------------------------
    # Dedicated error logger
    # ------------------------------------------------------------------
    error_logger = logging.getLogger("errors")
    error_logger.setLevel(logging.ERROR)

    if not error_logger.handlers:
        error_handler = logging.FileHandler(error_log_path)
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )
        error_handler.setLevel(logging.ERROR)
        error_logger.addHandler(error_handler)

    return logging.getLogger(__name__), error_logger
