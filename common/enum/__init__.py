# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'


class Enum(object):
    @classmethod
    def display_name(cls, action):
        return dict(cls.MapCn).get(action, '')

    @classmethod
    def is_enum(cls, action):
        return action in dict(cls.MapCn).keys()

    @classmethod
    def is_enum_cn(cls, action_cn):
        return action_cn in dict(cls.MapCn).values()

    @classmethod
    def get_fields_keys(cls):
        return dict(cls.Fields).keys()

    @classmethod
    def is_fields_key(cls, key):
        return key in cls.get_fields_keys()

    @classmethod
    def get_fields_default_value(cls, key):
        return dict(cls.Fields).get(key, '')
