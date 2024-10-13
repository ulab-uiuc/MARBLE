"""
Logging utility module.
"""

import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
    return logger