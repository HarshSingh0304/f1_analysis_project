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

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # File handler (already UTF-8 safe)
        file_handler = logging.FileHandler(project_log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # Console handler (FIXED)
        import sys
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        try:
            stream_handler.stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)

    error_logger = logging.getLogger("errors")
    error_logger.setLevel(logging.ERROR)

    if not error_logger.handlers:
        error_handler = logging.FileHandler(
            error_log_path, encoding="utf-8"
        )
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )
        error_handler.setLevel(logging.ERROR)
        error_logger.addHandler(error_handler)

    return logging.getLogger(__name__), error_logger
