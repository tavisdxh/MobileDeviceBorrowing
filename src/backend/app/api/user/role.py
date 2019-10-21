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
from app.common.utils import admin_or_has_permission_self
from app.model.user import Role

role_bp = Blueprint('role_bp', __name__)


class RoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("id", "name", "desc")

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=20))
    desc = fields.Str(validate=Length(max=50))


role_schema = RoleSchema()


@role_bp.route("/add", methods=['POST'])
@admin_or_has_permission_self(OperationPermission.ROLE_ADD)
def add_role():
    validate_result = role_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
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
def update_role(role_id):
    validate_result = role_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
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
