#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/10/18 17:01
"""
from flask import Blueprint, request, current_app
from marshmallow import fields
from marshmallow.validate import Length, OneOf

from app import generate_response, Code, db
from app.api.user.user import UserSchema
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.response import generate_page_response
from app.common.utils import admin_or_has_permission_self, delete_false_empty_page_args, validate_request
from app.model.user import Role, Permission, User

role_bp = Blueprint('role_bp', __name__)


class PermissionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "path", "name", "desc", "create_time", "update_time")


class RoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "name", "desc", "assigned_permissions", "available_permissions", "create_time", "update_time")

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=20))
    desc = fields.Str(validate=Length(max=50))
    assigned_permissions = fields.Nested(PermissionSchema, only=['id', 'name'], many=True)
    available_permissions = fields.Nested(PermissionSchema, only=['id', 'name'], many=True)


class RolesSchema(RoleSchema):
    class Meta(RoleSchema.Meta):
        fields = ("page", "per_page")

    name = fields.Str()
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)


class AssignPermissionSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("action", "permission_ids")

    action = fields.Str(required=True, validate=OneOf(["add", "remove"]))
    permission_ids = fields.List(fields.Integer(), required=True)


class RoleWithUserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "name", "desc", "assigned_users", "available_users", "create_time", "update_time")

    assigned_users = fields.Nested(UserSchema, only=['id', 'username', "realname"], many=True)
    available_users = fields.Nested(UserSchema, only=['id', 'username', "realname"], many=True)


class AssignUserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("action", "user_ids")

    action = fields.Str(required=True, validate=OneOf(["add", "remove"]))
    user_ids = fields.List(fields.Integer(), required=True)


class UserAssignRoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("action", "role_ids")

    action = fields.Str(required=True, validate=OneOf(["add", "remove"]))
    role_ids = fields.List(fields.Integer(), required=True)


class UserWithRoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "username", "realname", "email", "status", "assigned_roles", "available_roles", "create_time",
                  "update_time")

    assigned_roles = fields.Nested(RoleSchema, only=["id", "name"], many=True)
    available_roles = fields.Nested(RoleSchema, only=["id", "name"], many=True)


role_schema = RoleSchema()
roles_schema = RolesSchema()
assign_permission_schema = AssignPermissionSchema()
role_with_user_schema = RoleWithUserSchema()
assign_user_schema = AssignUserSchema()
user_assign_role_schema = UserAssignRoleSchema()
user_with_role_schema = UserWithRoleSchema()


@role_bp.route("/add", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_ADD)
@validate_request(role_schema, "json")
def add_role():
    role = Role.query.filter_by(name=request.json.get("name")).first()
    if role:
        return generate_response(code_msg=Code.ROLE_EXIST)
    role = Role(name=request.json.get("name"), desc=request.json.get("desc"))
    try:
        db.session.add(role)
        db.session.commit()
        return generate_response(data=role_schema.dump(role))
    except Exception as e:
        current_app.logger.error(str(e))
        db.session.rollback()
    return generate_response(code_msg=Code.ROLE_ADD_FAILED)


@role_bp.route("/update/<int:role_id>", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_ADD)
@validate_request(role_schema, "json")
def update_role(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        if role.name == request.json.get("name"):
            return generate_response(code_msg=Code.ROLE_EXIST)
        role.name = request.json.get("name")
        role.desc = request.json.get("desc")
        try:
            db.session.add(role)
            db.session.commit()
            return generate_response(data=role_schema.dump(role))
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)


@role_bp.route("/delete/<int:role_id>")
@admin_or_has_permission_self(OperationPermission.ROLE_DELETE)
def delete_role(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        try:
            db.session.delete(role)
            db.session.commit()
            return generate_response()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)


@role_bp.route("/get/<int:role_id>")
@admin_or_has_permission_self(OperationPermission.ROLE_GET)
def get_role(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        available_permissions = Permission.query.all()
        if role.permissions:
            for permission in role.permissions:
                if permission in available_permissions:
                    available_permissions.remove(permission)
        setattr(role, "assigned_permissions", role.permissions)
        setattr(role, "available_permissions", available_permissions)
        return generate_response(data=role_schema.dump(role))
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)


@role_bp.route("/get_roles")
@admin_or_has_permission_self(OperationPermission.ROLE_GET_ROLES)
@validate_request(roles_schema, "args")
def get_roles():
    query_dict = {}
    query_dict.update(delete_false_empty_page_args(request.args.to_dict()))
    pagination = Role.query.filter_by(**query_dict).order_by(Role.id).paginate(page=request.args.get("page", type=int),
                                                                               per_page=request.args.get("per_page",
                                                                                                         type=int),
                                                                               error_out=False)
    return generate_page_response(data=role_schema.dump(pagination.items, many=True), total=pagination.total,
                                  per_page=pagination.per_page, page=pagination.page, page_count=pagination.pages)


@role_bp.route("/assign_permission/<int:role_id>", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_ASSIGN_PERMISSION)
@validate_request(assign_permission_schema, "json")
def assign_permission(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        if request.json.get("permission_ids"):
            change_permissions = Permission.query.filter(Permission.id.in_(request.json.get("permission_ids"))).all()
            assigned_permissions = set(role.permissions)
            if request.json.get("action") == "add":
                for change_permission in change_permissions:
                    assigned_permissions.add(change_permission)
            elif request.json.get("action") == "remove":
                for change_permission in change_permissions:
                    if change_permission in role.permissions:
                        assigned_permissions.remove(change_permission)
            role.permissions = list(assigned_permissions)
        available_permissions = Permission.query.all()
        if role.permissions:
            for permission in role.permissions:
                if permission in available_permissions:
                    available_permissions.remove(permission)
        try:
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return generate_response(code_msg=Code.ROLE_ASSIGN_PERMISSION_FAILED)
        role.permissions = sorted(role.permissions, key=lambda x: x.id)
        setattr(role, "assigned_permissions", role.permissions)
        setattr(role, "available_permissions", available_permissions)
        return generate_response(data=role_schema.dump(role))
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)


@role_bp.route("/assign_user/<int:role_id>", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_ASSIGN_USER)
@validate_request(assign_user_schema, "json")
def assign_user(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if role:
        if request.json.get("user_ids"):
            change_users = User.query.filter(User.id.in_(request.json.get("user_ids"))).all()
            assigned_users = set(role.user)
            if request.json.get("action") == "add":
                for change_user in change_users:
                    assigned_users.add(change_user)
            elif request.json.get("action") == "remove":
                for change_user in change_users:
                    if change_user in role.user:
                        assigned_users.remove(change_user)
            role.user = list(assigned_users)
        available_users = User.query.all()
        if role.user:
            for user in role.user:
                if user in available_users:
                    available_users.remove(user)
        try:
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return generate_response(code_msg=Code.ROLE_ASSIGN_USER_FAILED)
        role.user = sorted(role.user, key=lambda x: x.id)
        setattr(role, "assigned_users", role.user)
        setattr(role, "available_users", available_users)
        return generate_response(data=role_with_user_schema.dump(role))
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)


@role_bp.route("/user_assign_role/<int:user_id>", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_USER_ASSIGN_ROLE_USER)
@validate_request(user_assign_role_schema, "json")
def user_assign_role(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        if request.json.get("role_ids"):
            change_roles = Role.query.filter(Role.id.in_(request.json.get("role_ids"))).all()
            assigned_roles = set(user.roles)
            if request.json.get("action") == "add":
                for change_role in change_roles:
                    assigned_roles.add(change_role)
            elif request.json.get("action") == "remove":
                for change_role in change_roles:
                    if change_role in user.roles:
                        assigned_roles.remove(change_role)
            user.roles = list(assigned_roles)
        available_roles = Role.query.all()
        if user.roles:
            for role in user.roles:
                if role in available_roles:
                    available_roles.remove(role)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return generate_response(code_msg=Code.ROLE_USER_ASSIGN_ROLE_FAILED)
        user.roles = sorted(user.roles, key=lambda x: x.id)
        setattr(user, "assigned_roles", user.roles)
        setattr(user, "available_roles", available_roles)
        return generate_response(data=user_with_role_schema.dump(user))
    return generate_response(Code.GET_USER_PROFILE_FAILED)
