# _*_ coding: utf-8 _*_
# @FileName : logger.py
# @Author   : sjl
# @CreatedAt     :  2021/03/16 11:09:12
# @UpdatedAt     :  2021/03/16 11:09:12
# @description: loopholes project's logger for logging
# @Software : VSCode

import logging
from logging.handlers import RotatingFileHandler


class LoggerInterface(object):
    """Interface Class
    """
    def __init__(self, logger_name, log_file_name):
        raise Exception("Interface class could't instantiate!")

    def get_logger(self):
        raise Exception("This methos must be implemented!")


class SimpleLogger(LoggerInterface):
    """
    """
    def __init__(self, logger_name, log_file_name):
        self.logger_name = logger_name
        self.log_file_name = log_file_name

    def get_logger(self, level=logging.INFO, max_bytes=100*1024*1024, backup_count=5, log_format=None):
        logger = logging.getLogger(self.logger_name)
        rfh = RotatingFileHandler(self.log_file_name, maxBytes=max_bytes, backupCount=backup_count)
        if not log_format:
            log_format = "%(asctime)s [%(levelname)s] %(name)s %(filename)s/%(lineno)d %(message)s"
        formatter = logging.Formatter(fmt=log_format)
        # set log level
        logger.setLevel(level)
        rfh.setLevel(level)

        logger.addHandler(rfh)
        rfh.setFormatter(formatter)

        return logger
