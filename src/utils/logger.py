import logging
from pathlib import Path

from src.utils.config import config


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    """

    log_directory = Path(config["logging"]["log_directory"])
    log_directory.mkdir(exist_ok=True)

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config["logging"]["level"]))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(
        log_directory / "application.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger