# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-06-01'

from configparser import ConfigParser
import codecs


class Config(object):
    def __init__(self, conf_path):
        self.path = conf_path
        self.cf = ConfigParser()
        self.cf.read_file(codecs.open(self.path, 'r', 'utf8'))

    def sections(self):
        result = None
        try:
            result = self.cf.sections()
        except:
            pass
        return result

    def options(self, section):
        result = None
        try:
            result = self.cf.options(section)
        except:
            pass
        return result

    def items(self, section):
        result = None
        try:
            result = dict(self.cf.items(section))
            for k ,v in result.items():
                print(k ,v)
                if int(v) > 0:
                    result[k] = int(v)
            return result
        except:
            pass
        return result

    def get(self, section, option):
        result = None
        try:
            result = self.cf.get(section, option)
        except:
            pass
        return result

    def get_int(self, section, option):
        result = None
        try:
            result = self.cf.getint(section, option)
        except:
            pass
        return result

    def get_bool(self, section, option):
        result = None
        try:
            result = self.cf.getboolean(section, option)
        except:
            pass
        return result

    def get_float(self, section, option):
        result = None
        try:
            result = self.cf.getfloat(section, option)
        except:
            pass
        return result

    def get_value(self, section, option, value_type='str'):
        if value_type == 'float':
            return self.get_float(section, option)
        elif value_type == 'int':
            return self.get_int(section, option)
        elif value_type == 'bool':
            return self.get_bool(section, option)
        elif value_type == 'str':
            return self.cf.get(section, option)
        else:
            return None

