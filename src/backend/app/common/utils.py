#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019-8-22 12:14
"""
import json
from functools import wraps

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

from app import redis_client, generate_response, Code
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


def get_permissions_from_redis(user_id):
    result = redis_client.hget("user_{user_id}".format(user_id=user_id), "permissions")
    if result:
        return json.loads(result.decode('utf-8'))
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


def get_roles_from_redis(user):
    result = redis_client.hget("user_{user_id}".format(user_id=user.id), "roles")
    if result:
        return json.loads(result.decode('utf-8'))
    roles = set()
    if user.roles:
        for role in user.roles:
            roles.add(role.name)
        redis_client.hset("user_{user_id}".format(user_id=user.id), "roles", json.dumps(list(sorted(roles))))
        redis_client.expire("user_{user_id}".format(user_id=user.id), current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    return list(sorted(roles))


def admin_or_has_permission(permission):
    """
    admin或有权限
    :param permission:
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            # admin角色可以访问所有
            result = redis_client.hget("user_{user_id}".format(user_id=claims['id']), "roles")
            if result:
                roles = json.loads(result.decode('utf-8'))
                if "admin" in roles:
                    return func(*args, **kwargs)
            # 或者有操作权限
            permissions = get_permissions_from_redis(claims['id'])
            if permission in permissions:
                return func(*args, **kwargs)
            return generate_response(code_msg=Code.PERMISSION_DENIED), 403

        wrapper.__name__ = func.__name__
        return wrapper

    return decorate


def admin_or_has_permission_self(permission):
    """
    admin可以处理所有数据。或有权限，且有权限时只能处理自己的数据。
    :param permission:
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            # admin角色可以访问所有
            result = redis_client.hget("user_{user_id}".format(user_id=claims['id']), "roles")
            if result:
                roles = json.loads(result.decode('utf-8'))
                if "admin" in roles:
                    return func(*args, **kwargs)
            # 或者有操作权限
            permissions = get_permissions_from_redis(claims['id'])
            if permission in permissions and "user_id" in kwargs.keys() and kwargs['user_id'] == claims['id']:
                return func(*args, **kwargs)
            return generate_response(code_msg=Code.PERMISSION_DENIED), 403

        wrapper.__name__ = func.__name__
        return wrapper

    return decorate
