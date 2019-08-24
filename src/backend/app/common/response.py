#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 14:43
"""


class Code:
    # 默认值
    SUCCESS = {'code': 0, 'msg': 'ok'}  # 成功
    FAILURE = {'code': -1, 'msg': 'error'}  # 失败

    # 系统公共1000~1999
    PARAMS_ERROR = {'code': 1000, 'msg': '参数错误'}
    DB_ERROR = {'code': 1001, 'msg': 'DB错误'}
    AUTH_ERROR = {'code': 1002, 'msg': '认证错误'}
    PERMISSION_DENIED = {'code': 1003, 'msg': '无权限访问'}

    # user业务
    USER_EXIST = {'code': 2000, 'msg': '用户已存在'}
    REGISTER_FAILED = {"code": 2001, "msg": "注册失败"}
    USER_IS_DISABLED = {"code": 2002, "msg": "用户已被禁用"}
    USERNAME_OR_PASSWORD_INVALID = {"code": 2003, "msg": "用户名或密码无效"}
    GET_USER_PROFILE_FAILED = {"code": 2004, "msg": "获取用户资料失败"}
    UPDATE_USER_PROFILE_FAILED = {"code": 2005, "msg": "更新用户资料失败"}
    PASSWORD_NOT_CORRECT = {"code": 2006, "msg": "密码不一致"}
    DELETE_USER_FAILED = {"code": 2007, "msg": "删除用户失败"}


def generate_response(data=None, code=None, msg=None, code_msg=None):
    if code_msg:
        code = code_msg['code']
        msg = code_msg['msg']
    if not code:
        code = Code.SUCCESS['code']
    if not msg:
        msg = Code.SUCCESS['msg']
    return {
        'data': data,
        'code': code,
        'msg': msg
    }


def generate_page_response(data=None, total=None, per_page=None, page=None, page_count=None):
    return {
        "data": data,
        "total": total,
        "per_page": per_page,
        "page": page,
        "page_count": page_count,
        "code": Code.SUCCESS["code"],
        "msg": Code.SUCCESS["msg"]
    }
