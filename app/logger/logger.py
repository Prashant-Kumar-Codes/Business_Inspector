import logging
import os
import sys


logger = logging.getLogger('businsp_app')


def setup_logging(app=None):
    level = logging.DEBUG if os.getenv('FASTAPI_ENV', 'development') != 'production' else logging.WARNING
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        logger.addHandler(handler)

    return logger


setup_logging()
    