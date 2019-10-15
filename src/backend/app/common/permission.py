#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 14:46
"""


class OperationPermission:
    # user业务
    USER_GET_USER = 'user_get_user'
    USER_UPDATE_USER = 'user_update_user'
    USER_UPDATE_PASSWORD = 'user_update_password'
    USER_GET_USERS = 'user_get_users'

    # device业务
    DEVICE_ADD_DEVICE = 'device_add_device'
    DEVICE_UPDATE_DEVICE = 'device_update_device'
    DEVICE_GET_DEVICE = 'device_get_device'
    DEVICE_GET_DEVICES = 'device_get_devices'

    # device申请、归还、审批
    DEVICE_APPLY = 'device_apply'
    DEVICE_RETURN = 'device_return'
    DEVICE_AUDIT = 'device_audit'
