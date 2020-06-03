# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-29'
from model.device import DeviceDal
from common.decorator import singleton
from thirdparty.adb.adb_device import get_connect_device

@singleton
class DeviceService(object):

    def get_connect_device(self):
        self.device_id = get_connect_device()




