#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/10/18 17:01
"""
from flask import Blueprint, request, current_app
from marshmallow import fields
from marshmallow.validate import Length

from app import generate_response, Code, db
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.response import generate_page_response
from app.common.utils import admin_or_has_permission_self, delete_false_empty_page_args, validate_request
from app.model.user import Role

role_bp = Blueprint('role_bp', __name__)


class RoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "name", "desc", "permissions", "create_time", "update_time")

    def dump_permissions(self, obj):
        permissions = []
        if obj.permissions:
            for permission in obj.permissions:
                permissions.append(permission.id)
        return permissions

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=20))
    desc = fields.Str(validate=Length(max=50))
    permissions = fields.Method("dump_permissions")


class RolesSchema(RoleSchema):
    class Meta(RoleSchema.Meta):
        fields = ("page", "per_page")

    name = fields.Str()
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)


role_schema = RoleSchema()
roles_schema = RolesSchema()


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
