# https://www.toptal.com/python/in-depth-python-logging
# https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-python-apps/#send-events-using-pythons-sysloghandler
import logging
import socket
from logging.handlers import TimedRotatingFileHandler

from kube_secrets_utility.config import LOG_HANDLER, LOG_LEVEL


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


FORMATTER = logging.Formatter(
    "%(asctime)s %(hostname)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
LOG_FILE = "kube_secrets_utility.log"


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.addFilter(ContextFilter())
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_sys_handler():
    syslog = logging.StreamHandler()
    syslog.addFilter(ContextFilter())
    syslog.setFormatter(FORMATTER)
    return syslog


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if LOG_LEVEL == "info":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    if LOG_HANDLER == "sys":
        logger.addHandler(get_sys_handler())
    else:
        logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
