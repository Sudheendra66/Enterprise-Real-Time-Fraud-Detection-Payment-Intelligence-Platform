import logging

from src.utils.logger import get_logger


def test_get_logger_returns_configured_logger():
    logger = get_logger("test_logger")

    assert isinstance(logger, logging.Logger)
    assert logger.handlers
    assert logger.propagate is True
