# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-27'
from flask import request
import abc, time, hashlib

'''
主要做鉴权使用，分三类鉴权；
1. ak + sk 鉴权, 主要使用在api接口的鉴权
2. user 权限鉴权, 主要是rbac鉴权
3. webhook的 token 鉴权，仅限于部分openapi接口
'''
access_key = ''
secret_key = ''
auth_token = ['abc', 'xxx', 'rrr']


class BaseAuth(object, metaclass=abc.ABCMeta):
    def __init__(self, auth_type):
        self.auth_type = auth_type

    @abc.abstractmethod
    def check_auth(self, req: request, **kwargs):
        pass

    @staticmethod
    def fetch_query(req: request):
        return req.path.rep.strip('/').replace('/', '_')


class ApiAuth(BaseAuth):
    def __init__(self):
        super(self, ApiAuth).__init__('api_auth')

    def check_auth(self, req: request, **kwargs):
        if not access_key:
            return False, 'access_key lose'
        if not secret_key:
            return False, 'secret_key lose'
        x_timestamp = int(req.headers.get('X-Timestamp'))
        if x_timestamp <= time.time() - 60 or x_timestamp > time.time() + 30:
            return False, 'request expired'
        signature = str(req.headers.get('X-Signature'))
        params_str = ','.join(['%s=%s' % (k, v) for k, v in req.values.to_dict().items()])
        if signature == hashlib.md5(params_str):
            return True, ''
        return False, 'auth with access_key fail'


class UserAuth(BaseAuth):
    def __init__(self):
        super(self, ApiAuth).__init__('user_auth')

    def check_auth(self, req: request, **kwargs):
        if req.user.get('isLogin'):
            return True, ''
        else:
            return False, 'user not login'


class TokenAuth(BaseAuth):
    def __init__(self):
        super(self, ApiAuth).__init__('token_auth')

    def check_auth(self, req: request, **kwargs):
        params = req.values.to_dict()
        token = req.headers.get('auth_token', '') or params.get('auth_token', '')
        if not token or token in auth_token:
            return True, ''
        else:
            return False, 'user not login'
