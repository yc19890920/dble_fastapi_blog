"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

import logging
from .settings import LOGGER_CONSOLE_LEVEL


class Logger:
    @staticmethod
    def get_logger(name):
        _handler = logging.StreamHandler()
        log_format = '%(asctime)s %(threadName)-10s %(process)d %(levelname)-8s (%(filename)s:%(lineno)d) %(message)s'
        _handler.setFormatter(logging.Formatter(log_format))
        log = logging.getLogger(name)
        log.addHandler(_handler)
        log.setLevel(LOGGER_CONSOLE_LEVEL)
        return log
