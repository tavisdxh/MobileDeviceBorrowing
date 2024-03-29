#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 15:35
"""
from flask import Blueprint, request, current_app
from flask_jwt_extended import get_jwt_claims
from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Length

from app import generate_response, Code, db, redis_client
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.response import generate_page_response
from app.common.utils import delete_false_empty_page_args, admin_or_has_permission, admin_or_has_permission_self, \
    validate_request
from app.model.user import User

user_bp = Blueprint('user_bp', __name__)


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "username", "realname", "email", "status", "create_time", "update_time")

    username = fields.Str(required=True, validate=Length(min=4, max=32))
    realname = fields.Str(required=True, validate=Length(min=2, max=32))
    email = fields.Email(required=True)


class PasswordSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("old_password", "new_password", "repeat_password")

    old_password = fields.Str(required=True, load_only=True, validate=Length(min=4))
    new_password = fields.Str(required=True, load_only=True, validate=Length(min=4))
    repeat_password = fields.Str(required=True, load_only=True, validate=Length(min=4))

    @validates_schema
    def valid_password(self, data, **kwargs):
        if data['new_password'] != data['repeat_password']:
            raise ValidationError("password must be equivalent")


class UsersSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "username", "realname", "email", "status", "create_time", "update_time", "page", "per_page")

    page = fields.Number(required=True, load_only=True)
    per_page = fields.Number(required=True, load_only=True)


user_schema = UserSchema()
update_user_schema = UserSchema()
password_schema = PasswordSchema()
users_schema = UsersSchema()


@user_bp.route('/get_user/<int:user_id>')
@admin_or_has_permission_self(OperationPermission.USER_GET_USER)
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return generate_response(data=user_schema.dump(user))
    return generate_response(code_msg=Code.GET_USER_PROFILE_FAILED)


@user_bp.route('/update_user/<int:user_id>', methods=['POST'])
@admin_or_has_permission_self(OperationPermission.USER_UPDATE_USER)
@validate_request(update_user_schema, "json")
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.username = request.json.get("username", user.username)
        user.realname = request.json.get("realname", user.realname)
        user.email = request.json.get("email", user.email)
        user.status = request.json.get("status", user.status)
        try:
            db.session.add(user)
            db.session.commit()
            # 若禁用了，则不允许登录
            if user.status == 0:
                redis_client.set("user_token_expired_{id}".format(id=user_id), 'true',
                                 ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
                redis_client.expire("user_{id}".format(id=user_id), 1)
            return generate_response(data=user_schema.dump(user))
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.UPDATE_USER_PROFILE_FAILED)


@user_bp.route('/update_password/<int:user_id>', methods=['POST'])
@admin_or_has_permission_self(OperationPermission.USER_UPDATE_PASSWORD)
@validate_request(password_schema, "json")
def update_password(user_id):
    claims = get_jwt_claims()
    if user_id != claims['id']:
        return generate_response(code_msg=Code.PERMISSION_DENIED), 403
    user = User.query.filter_by(id=user_id).first()
    if user and user.password == request.json.get("old_password"):
        user.password = request.json.get("new_password")
        try:
            db.session.add(user)
            db.session.commit()
            redis_client.set("user_token_expired_{id}".format(id=user_id), 'true',
                             ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            return generate_response()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.PASSWORD_NOT_CORRECT)


@user_bp.route('/get_users')
@admin_or_has_permission(OperationPermission.USER_GET_USERS)
@validate_request(users_schema, "args")
def get_users():
    query_dict = {}
    query_dict.update(delete_false_empty_page_args(request.args.to_dict()))
    pagination = User.query.filter_by(**query_dict).order_by(User.id).paginate(page=request.args.get("page", type=int),
                                                                               per_page=request.args.get("per_page",
                                                                                                         type=int),
                                                                               error_out=False)
    return generate_page_response(data=users_schema.dump(pagination.items, many=True), total=pagination.total,
                                  per_page=pagination.per_page, page=pagination.page, page_count=pagination.pages)
