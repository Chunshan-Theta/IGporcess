import os
import logging
import logging.handlers
from ImageWin.util.config import HOSTDIR,LOGDIR

default_logger_name = 'Main'


logging.basicConfig(
    format='%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def get_logger(name: str = None, file_name: str = 'Main', ENABLE_LOG_TO_FILE:bool=True):
    logger = logging.getLogger(f'{default_logger_name}-{name}' or default_logger_name)
    if ENABLE_LOG_TO_FILE is True:
        file_name = os.path.join(LOGDIR, f'{file_name}.log')
        if not os.path.exists(LOGDIR):
            os.makedirs(LOGDIR)
        filehandler = logging.handlers.TimedRotatingFileHandler(file_name,
                                                                when="midnight",
                                                                interval=1,
                                                                backupCount=10,
                                                                encoding="utf-8")
        formatter = logging.Formatter(fmt='%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
        filehandler.setFormatter(fmt=formatter)
        filehandler.suffix = "%Y-%m-%d.log"
        if len(logger.handlers) == 0 :
            logger.addHandler(filehandler)
    logger.setLevel(level='INFO')
    return logger
