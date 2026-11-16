"""
Logging utility module.
"""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger.

    The level defaults to ``DEBUG`` and can be overridden with the
    ``MARBLE_LOG_LEVEL`` environment variable (e.g. ``INFO`` or ``WARNING``).

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        level_name = os.environ.get("MARBLE_LOG_LEVEL", "DEBUG").upper()
        logger.setLevel(getattr(logging, level_name, logging.DEBUG))
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        # Avoid duplicated lines when the root logger is also configured.
        logger.propagate = False
    return logger
