# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'

import os
import logging
from logging.handlers import WatchedFileHandler
from conf import log_conf
import settings


class LogLevelFilter(logging.Filter):
    def __init__(self, name='', level=logging.INFO):
        super(LogLevelFilter, self).__init__(name)
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level


class Logger(object):
    def __init__(self):
        self.extra = None
        self.logger = logging.getLogger(__name__)
        self._add_handler()
        log_level = logging.DEBUG if settings.DEBUG else log_conf.loglevel
        self.logger.setLevel(log_level)

    def _add_handler(self):
        for level, rate in {'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN,
                            'error': logging.ERROR}.items():
            log_dir = os.path.dirname(getattr(log_conf, f'{level}_file'))
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)
            log_handler = WatchedFileHandler(getattr(log_conf, f'{level}_file'))
            log_handler.setLevel(rate)
            log_handler.addFilter(LogLevelFilter(level=rate))
            log_handler.setFormatter(logging.Formatter(fmt=log_conf.logformat, datefmt=log_conf.datefmt))

            self.logger.addHandler(log_handler)

    def set_extra(self, extra={}):
        if not self.extra:
            self.extra = {
                'ip': extra.get('ip', 'unknow ip'),
                'logid': extra.get('logid', 'unknown'),
                'env': extra.get('env', 'unknown'),
                'action': extra.get('action', 'unknown_action')
            }
        for k, v in extra.items():
            self.extra[k] = v
        self.logger = logging.LoggerAdapter(self.logger, extra)

    def get_extra(self):
        return self.extra

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def fatal(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)


msflogger = None


def init_logger(extra={}):
    global msflogger
    if not msflogger:
        msflogger = Logger()
    msflogger.set_extra(extra)
