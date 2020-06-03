# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-27'
from flask import request, session
import abc
from common.context import thread_local_ctx, generate_logid, host_ip
from .logger import msflogger


class BaseMiddleware(object, metaclass=abc.ABCMeta):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        self.before_request()
        rsp = self.app(environ, start_response)
        for i in rsp:
            yield i

    @abc.abstractmethod
    def before_request(self):
        pass


class UserMiddleware(BaseMiddleware):
    anonymousUser = {
        'isLogin': False,
        'username': 'anonymous',
        'uid': 0,
        'realname': 'not login'
    }

    def __init__(self, app):
        super(self, UserMiddleware).__init__(app)

    def before_request(self):
        request.user = self.check_login()

    @staticmethod
    def check_login():
        session_id = request.cookies.get('sessionId', '')
        if not session_id:
            return UserMiddleware.anonymousUser
        user = session.get(session_id)
        return user


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, app):
        super(self, LoggingMiddleware).__init__(app)

    def before_request(self):
        self._init_logger_ctx()
        msflogger.set_extra(thread_local_ctx)

    @staticmethod
    def _init_logger_ctx():
        if thread_local_ctx.log_id == '':
            thread_local_ctx.log_id = generate_logid()

        if thread_local_ctx.ip == '':
            thread_local_ctx.ip = host_ip()
