"""Log helper"""

import logging
import sys


def get_logger(name, as_json=False, loglevel=None, stream=sys.stdout):
    """Create a logger instance"""
    if not loglevel:
        loglevel = logging.INFO
    elif isinstance(loglevel, str):
        loglevel = getattr(logging, loglevel)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(loglevel)
    if as_json:
        log_format = (
            '"{timestamp":"%(asctime)s",'
            '"loglevel":"%(levelname)s",'
            '"message":"%(message)s",'
            '"process":%(process)d,'
            '"name":"%(name)s",'
            '"filename": "%(filename)s",'
            '"funcName": "%(funcName)s",'
            '"line_number": "%(lineno)s"}'
        )
        formatter = logging.Formatter(log_format)
        stream_handler.setFormatter(formatter)
    else:
        log_format = "%(asctime)s [%(name)s]{%(levelname)s}" "(%(process)d) %(message)s"
        formatter = logging.Formatter(log_format)
        stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
