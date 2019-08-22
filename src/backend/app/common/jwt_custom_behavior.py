#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/1 10:36
"""

from app import jwt, redis_client
from app.common.response import generate_response, Code


@jwt.claims_verification_failed_loader
def my_claims_verification_failed_loader():
    return generate_response(code_msg=Code.AUTH_ERROR, data="User claims verification failed"), 400


@jwt.expired_token_loader
def my_expired_token_loader(data):
    return generate_response(code_msg=Code.AUTH_ERROR, data="Token has expired"), 401


@jwt.invalid_token_loader
def my_invalid_token_loader(reason):
    return generate_response(code_msg=Code.AUTH_ERROR, data=reason), 422


@jwt.needs_fresh_token_loader
def my_needs_fresh_token_loader():
    return generate_response(code_msg=Code.AUTH_ERROR, data="Fresh token required"), 401


@jwt.revoked_token_loader
def my_revoked_token_loader():
    return generate_response(code_msg=Code.AUTH_ERROR, data="Token has been revoked"), 401


@jwt.unauthorized_loader
def my_unauthorized_loader(reason):
    return generate_response(code_msg=Code.AUTH_ERROR, data=reason), 401


@jwt.user_loader_error_loader
def my_user_loader_error_loader(identity):
    return generate_response(code_msg=Code.AUTH_ERROR,
                             data="Error loading the user {identity}".format(identity=identity)), 401


@jwt.user_claims_loader
def add_claims_to_access_token(user_id):
    return {
        'id': user_id,
    }


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_client.get(jti)
    if entry is None:
        return True
    return bytes.decode(entry) == 'true'
