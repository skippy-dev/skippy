"""Logger class

Attributes:
    log (logging.Logger): Skippy logger
    LOG_LEVELS (Dict[str, logging.LEVEL]): Log levels same as logging._nameToLevel
"""
import skippy.config

import datetime
import logging
import os


LOG_LEVELS = logging._nameToLevel


def get_file_handler() -> logging.FileHandler:
    """Get file handler

    Returns:
        logging.FileHandler: File handler
    """
    file_handler = logging.FileHandler(
        os.path.join(
            skippy.config.LOGS_FOLDER,
            f"{datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log",
        ),
        "a",
        "utf-8",
        True,
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    file_handler.setLevel(logging.DEBUG)

    return file_handler


def get_stream_handler() -> logging.StreamHandler:
    """Get stream handler

    Returns:
        logging.StreamHandler: Stream handler
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )

    return stream_handler


def get_logger(name: str) -> logging.Logger:
    """Get logger by name

    Args:
        name (str): Logger name

    Returns:
        logging.Logger: Logger class
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logger.addHandler(get_stream_handler())
    logger.addHandler(get_file_handler())

    return logger


log = get_logger("skippy")
