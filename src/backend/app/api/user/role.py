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
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.response import generate_page_response
from app.common.utils import admin_or_has_permission_self, delete_false_empty_page_args, validate_request
from app.model.user import Role, Permission

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


class AssignedSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("action", "permission_ids")

    action = fields.Str(required=True, validate=OneOf(["add", "remove"]))
    permission_ids = fields.List(fields.Integer(), required=True)


role_schema = RoleSchema()
roles_schema = RolesSchema()
assigned_schema = AssignedSchema()


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
@admin_or_has_permission_self(OperationPermission.ROLE_ASSIGNED_PERMISSION)
@validate_request(assigned_schema, "json")
def assign(role_id):
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
            role.permissions = list(sorted(assigned_permissions, key=lambda x: x.id))
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
            return generate_response(code_msg=Code.ROLE_ASSIGN_FAILED)
        setattr(role, "assigned_permissions", role.permissions)
        setattr(role, "available_permissions", available_permissions)
        return generate_response(data=role_schema.dump(role))
    return generate_response(code_msg=Code.ROLE_NOT_EXIST)
