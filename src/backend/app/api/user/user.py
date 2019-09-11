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
from app.common.utils import delete_false_empty_page_args, admin_or_has_permission, admin_or_has_permission_self
from app.model.user import User

user_bp = Blueprint('user_bp', __name__)


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "username", "realname", "email", "status", "create_time", "update_time")

    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True, validate=Length(min=4, max=32))
    realname = fields.Str(required=True, validate=Length(min=2, max=32))
    email = fields.Email(required=True)


user_schema = UserSchema()


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


@user_bp.route('/get_user/<int:user_id>')
@admin_or_has_permission_self(OperationPermission.USER_GET_USER)
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return generate_response(data=user_schema.dump(user))
    return generate_response(code_msg=Code.GET_USER_PROFILE_FAILED)


@user_bp.route('/update_user/<int:user_id>', methods=['POST'])
@admin_or_has_permission_self(OperationPermission.USER_UPDATE_USER)
def update_user(user_id):
    update_user_schema = UserSchema()
    validate_result = update_user_schema.validate(request.form)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.username = request.form.get("username", user.username)
        user.realname = request.form.get("realname", user.realname)
        user.email = request.form.get("email", user.email)
        user.status = request.form.get("status", user.status)
        try:
            db.session.add(user)
            db.session.commit()
            return generate_response(data=user_schema.dump(user))
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.UPDATE_USER_PROFILE_FAILED)


@user_bp.route('/update_password/<int:user_id>', methods=['POST'])
@admin_or_has_permission_self(OperationPermission.USER_UPDATE_PASSWORD)
def update_password(user_id):
    password_schema = PasswordSchema()
    validate_result = password_schema.validate(request.form)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    claims = get_jwt_claims()
    if user_id != claims['id']:
        return generate_response(code_msg=Code.PERMISSION_DENIED), 403
    user = User.query.filter_by(id=user_id).first()
    if user and user.password == request.form.get("old_password"):
        user.password = request.form.get("new_password")
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


@user_bp.route('/delete_user/<int:user_id>')
@admin_or_has_permission(OperationPermission.USER_DELETE_USER)
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.status = 0
        try:
            db.session.add(user)
            db.session.commit()
            redis_client.set("user_token_expired_{id}".format(id=user_id), 'true',
                             ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            return generate_response()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.DELETE_USER_FAILED)


@user_bp.route('/get_users')
@admin_or_has_permission(OperationPermission.USER_GET_USERS)
def get_users():
    users_schema = UsersSchema()
    validate_result = users_schema.validate(request.args)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    query_dict = {}
    query_dict.update(delete_false_empty_page_args(request.args.to_dict()))
    pagination = User.query.filter_by(**query_dict).order_by(User.id).paginate(page=request.args.get("page", type=int),
                                                                               per_page=request.args.get("per_page",
                                                                                                         type=int),
                                                                               error_out=False)
    return generate_page_response(data=users_schema.dump(pagination.items, many=True), total=pagination.total,
                                  per_page=pagination.per_page, page=pagination.page, page_count=pagination.pages)
