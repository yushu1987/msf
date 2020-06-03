# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'
import datetime
from sqlalchemy import BigInteger, Column, Integer, String, DateTime
from .mysql import BaseModel, BaseDal


class User(BaseModel):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(BigInteger, nullable=False, default=0, index=True)
    username = Column(String, nullable=False, default='')
    realname = Column(String, nullable=False, default='')
    email = Column(String, nullable=False, default='')
    active = Column(Integer, nullable=False, default=1),  # 未激活
    role = Column(Integer, nullable=False, default=0)
    createTime = Column(DateTime, name='create_time', nullable=False, default=datetime.datetime.now)
    lastLogin = Column(DateTime, name='last_login', nullable=False, default='')


class UserDal(BaseDal):
    def __init__(self):
        pass

    def load_user(self, uid):
        where = {'uid': uid}
        return self.select(User, where, one=True)

    def set_role(self, uid, role):
        where = {'uid': uid}
        upd = {'role': role}
        return self.update(User, where, update_data=upd, limit=1)

    def set_login(self, uid, last_login):
        where = {'uid': uid}
        upd = {'lastLogin': last_login}
        return self.update(User, where, update_data=upd, limit=1)
