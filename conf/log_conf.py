# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'
import logging
import settings

logformat = "%(levelname)s %(asctime)s %(pathname)s:%(lineno)s %(psm)s %(logid)s %(ip)s %(message)s"
datefmt = '%Y-%m-%d %H:%M:%S'
loglevel = logging.INFO


debug_file = settings.ROOT_PATH + '/log/debug.log'
info_file = settings.ROOT_PATH + '/log/info.log'
error_file = settings.ROOT_PATH + '/log/error.log'
warn_file = settings.ROOT_PATH + '/log/warning.log'