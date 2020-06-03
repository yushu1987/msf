# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'

from .enum.exception_enum import MsfExceptionEnum
from .logger import msflogger


class MsfException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        if self.message == '':
            self.message = MsfExceptionEnum.get_fields_default_value(code)
        self.emit_log()

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message
        }

    def __str__(self):
        return f'<code:f{self.code} message:f{self.message}>'

    def emit_log(self):
        msflogger.exception(f'raise exception: code[{self.code}] message[{self.message}]')
