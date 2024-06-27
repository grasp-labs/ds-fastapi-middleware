"""Uniform Logger for ds"""

import logging
import os
import sys


class ContextFilter(logging.Filter):
    """Context filter to add customized field in the logging"""

    def __init__(self, prefix: str = None):
        self._prefix = prefix

    def filter(self, record):
        if not hasattr(record, "prefix"):
            record.prefix = "---"
        record.prefix = self._prefix
        return True


class Logger:
    """
    Setup logger for ds.
    One of the most import aspects of a general logging system
    is the ability to enforce a common pattern for log messages,
    in addition to tagging of information, especially when applied
    to an event driven platform. What we hope to acheive is a uniform
    use of prefixes in log messages, which will help users to quickly
    find all log items of an event, across all services and log silos.

    Usage:
    logger = Logger()

    # set prefix
    # 1 handlers are set up here
    # 1. Stream handler for console
    # all the messages from daas-service will be in the specified format
    # [%(asctime)s][%(levelname)s]%(prefix)s[%(module)s]: %(message)s

    logger.setup_logger(prefix="prefix")

    # logging
    logger.info(msg)

    # send log file to s3
    logger.send_to_s3(key)

    # shutdown
    logger.shutdown()
    """

    logger_name = os.environ.get("DS_LOGGER_NAME", "ds-logger")
    LOGGER = logging.getLogger(logger_name)
    FORMATTER = logging.Formatter(
        "[%(asctime)s][%(levelname)s]%(prefix)s[%(module)s]: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    def __init__(self, log_level=logging.DEBUG) -> None:
        self.LOGGER.setLevel(log_level)

    def setup_logger(self, prefix: str) -> None:
        """
        Instantiates logger with a handler and a log message prefix.
        :param prefix: Prefix in log message.
        """
        # to avoid multithread access, clear the handler when setup
        self.shutdown()
        self.LOGGER.addHandler(self._setup_stream_handler(prefix))

    def info(self, msg: str):
        """
        Wrapper for logging info func
        """
        self.LOGGER.info(msg)

    def warning(self, msg: str):
        """
        Wrapper for logging info func
        """
        self.LOGGER.warning(msg)

    def error(self, msg: str):
        """
        Wrapper for logging info func
        """
        self.LOGGER.error(msg)

    def debug(self, msg: str):
        """
        Wrapper for logging debug func
        """
        self.LOGGER.debug(msg)

    @staticmethod
    def shutdown():
        Logger.LOGGER.handlers = []

    def _setup_stream_handler(self, prefix: str):
        """
        Sets up stream handler for logger with logging prefix.
        :param prefix: Prefix applied on every log to add context: Who!
        :return: logging.StreamHandler
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.FORMATTER)
        handler.addFilter(ContextFilter(prefix))
        handler.name = "console"
        return handler
