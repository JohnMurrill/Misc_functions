import logging
import sys
import watchtower
from logging.handlers import TimedRotatingFileHandler


class Logger:
    FORMATTER = None
    LOGGER = None
    LOG_FILE = None

    def __init__(self, loggerName, filename=None, fmat=None):
        logging.basicConfig(level=logging.DEBUG)
        if fmat is None:
            self.FORMATTER = logging.Formatter("%(levelname)s:%(name)s — %(asctime)s — %(message)s")
        else:
            self.FORMATTER = logging.Formatter(fmat)
        self.LOGGER = self.__get_logger(loggerName)
        self.LOG_FILE = filename

    def __get_console_handler(self):
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(self.FORMATTER)
        return ch

    def __get_file_handler(self):
        fh = TimedRotatingFileHandler(self.LOG_FILE, when='midnight')
        fh.setFormatter(self.FORMATTER)
        return fh

    def __get_cloudwatch_handler(self):
        cwh = watchtower.CloudWatchLogHandler()
        cwh.setFormatter(self.FORMATTER)
        return cwh

    def __get_logger(self, logger_name):
        lg = logging.getLogger(logger_name)
        lg.setLevel(logging.DEBUG)
        lg.addHandler(self.__get_console_handler())
        lg.addHandler(self.__get_file_handler())
        lg.propagate = False
        return lg
