#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 15:33
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Length

from app import db, redis_client
from app.api.user.user import UserSchema, user_schema
from app.common.base_schema import BaseSchema
from app.common.response import generate_response, Code
from app.common.utils import get_permissions_from_redis, get_roles_from_redis, validate_request
from app.model.user import User, Role

auth_bp = Blueprint('auth_bp', __name__)


class LoginSchema(UserSchema):
    class Meta(BaseSchema.Meta):
        fields = ("username", "password")

    password = fields.Str(required=True, load_only=True, validate=Length(min=4))


class RegisterSchema(UserSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "username", "realname", "email", "status", "create_time",
            "update_time", "password", "repeat_password")

    password = fields.Str(required=True, load_only=True, validate=Length(min=4))
    repeat_password = fields.Str(required=True, load_only=True, validate=Length(min=4))

    @validates_schema
    def valid_password(self, data, **kwargs):
        if data['password'] != data['repeat_password']:
            raise ValidationError("password must be equivalent")


register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route('/register', methods=['POST'])
@validate_request(register_schema, "json")
def register():
    exist_user = User.query.filter_by(username=request.json.get("username")).first()
    if exist_user:
        return generate_response(code_msg=Code.USER_EXIST)
    else:
        try:
            new_user = User(username=request.json.get("username"),
                            password=request.json.get("password"),
                            realname=request.json.get("realname"),
                            email=request.json.get("email"))
            # role = Role.query.filter_by(name="normal").first()
            # new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()
            new_user_dump = user_schema.dump(new_user)
            access_token = create_access_token(identity=new_user.id)
            new_user_dump["permissions"] = get_permissions_from_redis(new_user.id)
            new_user_dump["roles"] = get_roles_from_redis(new_user)
            redis_client.set("user_token_expired_{id}".format(id=new_user.id), 'false',
                             ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            new_user_dump["access_token"] = access_token
            return generate_response(data=new_user_dump)
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.REGISTER_FAILED)


@auth_bp.route('/login', methods=['POST'])
@validate_request(login_schema, "json")
def login():
    exist_user = User.query.filter_by(username=request.json.get("username")).first()
    if exist_user:
        if exist_user.password == request.json.get("password"):
            if exist_user.status == 0:
                return generate_response(code_msg=Code.USER_IS_DISABLED), 401
            exist_user_dump = user_schema.dump(exist_user)
            access_token = create_access_token(identity=exist_user.id)
            redis_client.set("user_token_expired_{id}".format(id=exist_user.id), 'false',
                             ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            exist_user_dump["permissions"] = get_permissions_from_redis(exist_user.id)
            exist_user_dump["roles"] = get_roles_from_redis(exist_user)
            exist_user_dump["access_token"] = access_token
            return generate_response(data=exist_user_dump)
    return generate_response(code_msg=Code.USERNAME_OR_PASSWORD_INVALID)


@auth_bp.route('/logout')
@jwt_required
def logout():
    user_id = get_raw_jwt()['identity']
    # revoked token
    redis_client.set("user_token_expired_{user_id}".format(user_id=user_id), 'true',
                     ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    # remove permissions roles
    redis_client.hdel("user_{user_id}".format(user_id=user_id), "permissions")
    redis_client.hdel("user_{user_id}".format(user_id=user_id), "roles")
    return generate_response()
