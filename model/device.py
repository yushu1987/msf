# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'

import datetime
from sqlalchemy import Text, Column, Integer, String, DateTime
from .mysql import BaseModel, BaseDal


class Device(BaseModel):
    __tablename__ = 't_device'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceId = Column(String, name='device_id', nullable=False, default=0, index=True, unique=True)
    deviceType = Column(String, name='device_type', nullable=False, default='')
    deviceBrand = Column(String, name='device_brand', nullable=False, default='')
    deviceScreen = Column(String, name='device_screen', nullable=False, default='')
    deviceExtra = Column(Text, name='device_extra', nullable=False, default='')
    deviceActive = Column(Integer, name='device_active', nullable=False, default=1)  # 未激活
    deviceOwner = Column(String, name='device_owner', nullable=False, default=datetime.datetime.now)
    createTime = Column(DateTime, name='create_time', nullable=False, default='')


class DeviceDal(BaseDal):

    def get_device_info(self, device_id):
        where = {'deviceId': device_id}
        return self.select(__class__, where, one=True)

    def save_device_info(self, save_data={}):
        where = {'deviceId': save_data['device_id']}
        device_info = self.select(Device, where, one=True)
        if device_info:
            save_data.pop('device_id')
            return self.update(Device, where, update_data=save_data)
        else:
            return self.add(Device, save_data)

    def change_device_owner(self, device_id, owner):
        where = {'deviceId': device_id}
        upd = {'deviceOwner': owner}
        return self.update(Device, where, update_data=upd)
