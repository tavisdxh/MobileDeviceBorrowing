#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019-8-22 12:14
"""
import json

from flask import current_app

from app import redis_client
from app.model.user import User


def delete_false_page_args(args):
    """
    只获取非None的入参
    :param args:
    :return:
    """
    query_dict = {}
    for k, v in args.items():
        if v is not None and k != "page" and k != "per_page":
            query_dict.update({k: v})
    return query_dict


def delete_false_empty_page_args(args):
    """
    只获取非None、非空的入参
    :param args:
    :return:
    """
    query_dict = {}
    for k, v in args.items():
        if v and k != "page" and k != "per_page":
            query_dict.update({k: v})
    return query_dict


def get_operation_permission(user_id):
    result = redis_client.hget("user_{user_id}".format(user_id=user_id), "permissions")
    if result:
        return json.loads(result.decode('utf-8'))
    else:
        permissions = set()
        user = User.query.filter_by(id=user_id).first()
        if user.roles:
            for role in user.roles:
                for permission in role.permissions:
                    permissions.add(permission.path)
        if permissions:
            redis_client.hset("user_{user_id}".format(user_id=user_id), "permissions",
                              json.dumps(list(sorted(permissions))))
            redis_client.expire("user_{user_id}".format(user_id=user_id),
                                current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        return list(sorted(permissions))


def set_roles_to_redis(user):
    roles = set()
    if user.roles:
        for role in user.roles:
            roles.add(role.name)
        redis_client.hset("user_{user_id}".format(user_id=user.id), "roles", json.dumps(list(sorted(roles))))
        redis_client.expire("user_{user_id}".format(user_id=user.id), current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    return list(sorted(roles))
