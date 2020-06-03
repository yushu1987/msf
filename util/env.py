# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-06-01'

import os


def get_env():
    return 'prod' if os.environ.get('PROD', True) else 'test'


def is_test():
    return os.environ['PROD'] == 'test'


def is_prod():
    return os.environ['PROD'] == 'prod'
