#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/12 11:53
"""
from flask import Blueprint, request, current_app
from marshmallow import fields

from app import generate_response, Code, db
from app.api.user.user import UserSchema
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.utils import admin_or_has_permission
from app.model.device import Device

device_bp = Blueprint('device_bp', __name__)


class DeviceSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "type", "brand", "model", "os", "os_version", "resolution", "asset_no", "root", "location", "status",
            "owner",
            "current_user", "desc", "create_time",
            "update_time")

    id = fields.Integer(dump_only=True)
    type = fields.Str(required=True)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
    os = fields.Str(required=True)
    owner = fields.Nested(UserSchema, only=("id", "realname"))
    current_user = fields.Nested(UserSchema, only=("id", "realname"))


device_schema = DeviceSchema()


@device_bp.route("/add_device", methods=["POST"])
@admin_or_has_permission(OperationPermission.DEVICE_ADD_DEVICE)
def add_device():
    validate_result = device_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    device = Device(type=request.json.get("type"),
                    brand=request.json.get("brand"),
                    model=request.json.get("model"),
                    os=request.json.get("os"),
                    os_version=request.json.get("os_version"),
                    resolution=request.json.get("resolution"),
                    asset_no=request.json.get("asset_no"),
                    root=request.json.get("root"),
                    location=request.json.get("location"),
                    owner_id=request.json.get("owner").get("id") if request.json.get("owner") else None,
                    current_user_id=request.json.get("current_user").get("id") if request.json.get(
                        "current_user") else None,
                    desc=request.json.get("desc"))
    try:
        db.session.add(device)
        db.session.commit()
        device_dump = device_schema.dump(device)
        return generate_response(data=device_dump)
    except Exception as e:
        current_app.logger.error(str(e))
        db.session.rollback()
    return generate_response(code_msg=Code.ADD_DEVICE_FAILED)


@device_bp.route('/update_device/<int:device_id>', methods=["POST"])
@admin_or_has_permission(OperationPermission.DEVICE_UPDATE_DEVICE)
def update_device(device_id):
    validate_result = device_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    exist_device = Device.query.filter_by(id=device_id).first()
    if exist_device:
        exist_device.type = request.json.get("type")
        exist_device.brand = request.json.get("brand")
        exist_device.model = request.json.get("model")
        exist_device.os = request.json.get("os")
        exist_device.os_version = request.json.get("os_version")
        exist_device.resolution = request.json.get("resolution")
        exist_device.asset_no = request.json.get("asset_no")
        exist_device.root = request.json.get("root")
        exist_device.location = request.json.get("location")
        exist_device.owner_id = request.json.get("owner").get("id") if request.json.get("owner") else None
        exist_device.current_user_id = request.json.get("current_user").get("id") if request.json.get(
            "current_user") else None
        exist_device.desc = request.json.get("desc")
        try:
            db.session.add(exist_device)
            db.session.commit()
            device_dump = device_schema.dump(exist_device)
            return generate_response(data=device_dump)
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(Code.UPDATE_DEVICE_FAILED)
