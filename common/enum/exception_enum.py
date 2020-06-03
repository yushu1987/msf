# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'
from common.enum import Enum


class MsfExceptionEnum(Enum):
    # 1: system/http error
    UNAUTHORIZED = 1001
    LIMITED = 1002
    PARAM_ERROR = 1003
    TO_MANY = 1004
    RPC_CALL_TIMEOUT = 1005
    DUPLICATE_REQUEST = 1006
    DB_CALL_ERROR = 1007
    SYSTEM_ERROR = 1008

    # 2: user error
    USER_NOT_LOGIN = 2001
    NO_PERMISSION = 2002
    USER_LOAD_ERROR = 2003
    INVALID_OWNER = 2004

    # 3: file error
    UNSUPPORTED_TYPE = 3001
    UPLOAD_TIMEOUT = 3002
    UPLOAD_FAILED = 3003
    UNZIP_ERROR = 3004
    FILE_NOT_FOUND = 3005
    UNAUTHORIZED_VIEW = 3006
    DOWNLOAD_ERROR = 3007
    SEARCH_ERROR = 3008
    VIEW_ERROR = 3009
    APK_ERROR = 3010
    SIZE_ZERO = 3011
    OSS_NOT_CONNECT = 3020
    OSS_PUT_FAILED = 3021
    OSS_FILE_NOT_EXIST = 3022
    READ_FILE_ERROR = 3023

    # 4: job error
    JOB_NOT_EXIST = 4001
    JOB_MSG_PARSE_ERROR = 4002
    JOB_EXEC_FAILED = 4003
    JOB_NOT_OWN = 4004
    JOB_RUN_TIMEOUT = 4010

    # 5: device error

    MapCn = (
        (UNAUTHORIZED, '访问受限'),
        (LIMITED, '访问限流'),
        (PARAM_ERROR, '参数错误'),
        (TO_MANY,'请求过快'),
        (RPC_CALL_TIMEOUT, '远程调用超时'),
        (DUPLICATE_REQUEST, '请求重复'),
        (SYSTEM_ERROR, '系统错误'),

        (USER_NOT_LOGIN, '未登入'),
        (NO_PERMISSION, '权限不足'),
        (USER_LOAD_ERROR, '用户信息加载失败'),

        (UNSUPPORTED_TYPE, '不支持文件类型'),
        (UPLOAD_TIMEOUT, '上传文件超时'),
        (UPLOAD_FAILED, '上传文件失败'),
        (UNZIP_ERROR, '文件解压失败'),
        (FILE_NOT_FOUND, '文件不存在'),
        (UNAUTHORIZED_VIEW, '无权限查看'),
        (DOWNLOAD_ERROR, '文件下载失败'),
        (SEARCH_ERROR, '查询失败'),
        (VIEW_ERROR, '查看失败'),
        (APK_ERROR, 'apk文件错误'),
        (SIZE_ZERO,'文件大小为0'),
        (OSS_NOT_CONNECT, 'OSS链接断开'),
        (OSS_PUT_FAILED, 'OSS上传失败'),
        (OSS_FILE_NOT_EXIST, 'OSS文件不存在'),
        (READ_FILE_ERROR, '读取文件失败'),

        (JOB_NOT_EXIST, 'job不存在'),
        (JOB_MSG_PARSE_ERROR, 'job消息解析错误'),
        (JOB_EXEC_FAILED, 'job执行失败'),
        (JOB_NOT_OWN, '非job owner操作'),
        (JOB_RUN_TIMEOUT, 'job执行超时')
    )
