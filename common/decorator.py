# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-27'
from flask import request, Response
import threading, functools, json, traceback
from .exception import MsfException
from .enum.exception_enum import MsfExceptionEnum
from .logger import msflogger
from .auth import ApiAuth, UserAuth, TokenAuth

AUTH_MAP = dict(
    api_auth=ApiAuth,
    user_auth=UserAuth,
    token_auth=TokenAuth
)


def auth_wrapper(auth_types):
    def handle_func(func):
        @functools.wraps(func)
        def handle_args(*args, **kwargs):
            msflogger.info('[request] url: %s, params: {%s} headers:{%s}' % (
                request.url, ','.join(request.values.to_dict()), request.headers))
            for auth in auth_types:
                is_pass, message = AUTH_MAP[auth].check_sign()
                if is_pass:
                    return func(*args, **kwargs)
                else:
                    msflogger.warning('[auth request] auth [%s] fail message:[%s]' % (auth, message))
            raise MsfException(MsfExceptionEnum.UNAUTHORIZED, 'auth fail: ' + message)

        return handle_args

    return handle_func


def response_json(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        try:
            rsp = func(*args, **kwargs)
            return Response(
                json.dumps(dict(error=0, msg=0, data=rsp)),
                content_type='application/json'
            )
        except MsfException as e:
            return Response(
                json.dumps(dict(error=e.code, msg=e.message, data=[])),
                content_type='application/json'
            )
        except Exception:
            msflogger.error('system fatal happened! fatal cause:%s' % traceback.format_exc())
            return Response(
                json.dumps(dict(error=8000, msg='系统错误', data=[])),
                content_type='application/json'
            )

    return _func


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def _memoize(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return _memoize


def async_call(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
        thr.setName(f'func-name-{f.__name__}')

    return wrapper
