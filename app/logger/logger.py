'''
A centralized logging 
* Developement (default): Shows all logs (Debug level)
* Production (FASTAPI_ENV=production): Shows only Warning and above
'''

import logger
import os, sys

def setup_logging(app=None):
    '''Configure logging based on environment'''
    is_dev = os.getenv("FASTAPI_ENV", 'development') != 'production'
    if app:
        is_dev = is_dev or app.Debug

    level = logging.DEBUG if is_dev else logging.WARNING

    app_logger = logging.getLogger('businsp_app')
    app_logger.setLevel(level)

    if not app_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        ))
        app.logger.addHandler(handler)

    return app_logger


# Ready-to-import logger instace
logger = logger.getLogger('businsp_app')
if not logger.handlers:
    setup_logger()
    