# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-27'
import os
from common import conf_agent
from util import env

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
Conf = conf_agent.Config(ROOT_PATH + '/conf/' + env.get_env() + '.env.conf')

DEBUG =False

SESSION = {
    'SESSION_TYPE': 'redis',
    'SESSION_REDIS': {
        'host': '127.0.0.1',
        'port': 6379
    },
    'SESSION_USE_SIGNER': True,
    'SECRET_KEY': os.urandom(32),
    'SESSION_PERMANENT': False,
    'PERMANENT_SESSION_LIFETIME': 3600*30
}

PROCESS_WORKER = 5

ADB_BINARY = ''