# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-06-01'
from .adb_cmd import cmd_execute
from common.decorator import memoize


#@memoize
def get_connect_device() -> [str]:
    '''
    only support one connect device
    :return:
    '''
    cmd = 'devices'
    timeout = 3
    stdout, _ = cmd_execute(cmd, timeout)
    try:
        for line in stdout.splitlines():
            if line.contains('\t') > 0:
                return line.split('\t')[0]
    except:
        return ''


#@memoize
def get_screen_size(device_id: str ) -> str:
    '''
    obtain device screen size
    :param device_id:
    :return:
    '''
    cmd = 'shell wm size'
    timeout = 1
    stdout, _ = cmd_execute(cmd, device_id, timeout)
    try:
        for line in stdout.splitlines():
            if line.contains('Physical size'):
                return line.split(' ')[-1]
    except:
        return ''


