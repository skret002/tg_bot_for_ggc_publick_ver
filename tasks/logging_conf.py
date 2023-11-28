
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging,functools, time
import logging.handlers
from logging.config import dictConfig

#logger = logging.getLogger(configure_logging())

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}
def configure_logging():
    dictConfig(DEFAULT_LOGGING)

    default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler('tasks/celery.log', maxBytes=10485760,backupCount=300, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(default_formatter)
    console_handler.setFormatter(default_formatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
    
logger = logging.getLogger(configure_logging())


def logg(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start = time.perf_counter()
            val = func(*args, **kwargs)
            end = time.perf_counter()
            work_time = end - start
            logger.info(f"Время выполнения {func.__name__!r}: {work_time:.4f} сек. Args:{args} Kwargs {kwargs}")
            return val
        except Exception as e:
            logger.error(f"Detect error in function  {func.__name__!r} : \n {e}")
    return wrapper