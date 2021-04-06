import os
import logging
from datetime import date

import skippy.config

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(
        os.path.join(skippy.config.LOGS_FOLDER, f"{str(date.today())}.log"),
        'w', 'utf-8')

    c_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    f_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    f_handler.setLevel(logging.DEBUG)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


log = get_logger('skippy')
