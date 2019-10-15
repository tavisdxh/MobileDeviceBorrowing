#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/25 11:34
"""
import json

from flask import Blueprint, request, current_app
from flask_jwt_extended import get_jwt_claims
from marshmallow import fields
from sqlalchemy import not_

from app import generate_response, Code, db, redis_client
from app.common.base_schema import BaseSchema
from app.common.permission import OperationPermission
from app.common.utils import admin_or_has_permission
from app.model.device import Device, DeviceApplyRecord

device_apply_bp = Blueprint('device_apply_bp', __name__)


class DeviceApplySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("start_time", "end_time", "application_desc")

    start_time = fields.DateTime()
    end_time = fields.DateTime()


class DeviceAuditSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = ("approval", "reason")

    approval = fields.Integer(required=True)
    reason = fields.Str()


apply_schema = DeviceApplySchema()
audit_schema = DeviceAuditSchema()


@device_apply_bp.route('/apply/<int:device_id>', methods=["POST"])
@admin_or_has_permission(OperationPermission.DEVICE_APPLY)
def apply(device_id):
    validate_result = apply_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    claims = get_jwt_claims()
    applicant_id = claims['id']
    device = Device.query.filter_by(id=device_id).filter(Device.status != 0).first()
    if device:
        apply_records = DeviceApplyRecord.query.filter_by(device_id=device_id, applicant_id=applicant_id).filter(
            not_(DeviceApplyRecord.status.in_([0, 5]))).all()
        # 同一用户不允许多次申请同一设备
        if apply_records:
            return generate_response(code_msg=Code.APPLY_DEVICE_DUPLICATE)
        else:
            apply_record = DeviceApplyRecord(device_id=device_id, applicant_id=applicant_id,
                                             start_time=request.json.get("start_time"),
                                             end_time=request.json.get("end_time"),
                                             application_desc=request.json.get("application_desc"))
            try:
                db.session.add(apply_record)
                db.session.commit()
                return generate_response()
            except Exception as e:
                current_app.logger.error(str(e))
                db.session.rollback()
            return generate_response(code_msg=Code.APPLY_FAILED)
    else:
        return generate_response(code_msg=Code.APPLY_DEVICE_NOT_READY)


@device_apply_bp.route('/return/<int:apply_id>', methods=["GET"])
@admin_or_has_permission(OperationPermission.DEVICE_RETURN)
def return_back(apply_id):
    claims = get_jwt_claims()
    applicant_id = claims['id']
    apply_record = DeviceApplyRecord.query.filter_by(id=apply_id).first()
    # 只有申请通过、归还不通过状态才可以进行归还
    if apply_record and apply_record.applicant_id == applicant_id and apply_record.status in [2, 6]:
        apply_record.status = 4
        try:
            db.session.add(apply_record)
            db.session.commit()
            return generate_response()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
    return generate_response(code_msg=Code.APPLY_DEVICE_RETURN_FAILED)


@device_apply_bp.route('/audit/<int:apply_id>', methods=["POST"])
@admin_or_has_permission(OperationPermission.DEVICE_AUDIT)
def audit(apply_id):
    validate_result = audit_schema.validate(request.json)
    if validate_result:
        return generate_response(data=validate_result, code_msg=Code.PARAMS_ERROR), 400
    claims = get_jwt_claims()
    auditor_id = claims['id']
    apply_record = DeviceApplyRecord.query.filter_by(id=apply_id).first()
    device = Device.query.filter_by(id=apply_record.device_id).first()
    # 审批“申请中”、“归还中”
    if apply_record and apply_record.status in [1, 4] and device:
        auditor_is_admin = False
        audit_or_not = False
        result = redis_client.hget("user_{user_id}".format(user_id=auditor_id), "roles")
        if result:
            roles = json.loads(result.decode('utf-8'))
            if "admin" in roles:
                auditor_is_admin = True
        # admin角色可以审批所有申请、归还记录
        if auditor_is_admin:
            audit_or_not = True
        else:
            # 非admin角色只能处理owner是自己的申请、归还记录。
            if device.owner_id == auditor_id:
                audit_or_not = True
        if audit_or_not:
            # 申请的记录
            if apply_record.status == 1:
                apply_record.apply_audit_reason = request.json.get("reason")
                apply_record.apply_auditor_id = auditor_id
                if request.json.get("approval") == 1:
                    apply_record.status = 2
                    device.current_user_id = apply_record.applicant_id
                else:
                    apply_record.status = 3
            else:
                apply_record.return_audit_reason = request.json.get("reason")
                apply_record.return_auditor_id = auditor_id
                if request.json.get("approval") == 1:
                    apply_record.status = 5
                    device.current_user_id = None
                else:
                    apply_record.status = 6
            try:
                db.session.add(apply_record)
                db.session.add(device)
                print(device)
                print(device.current_user_id)
                db.session.commit()
                return generate_response()
            except Exception as e:
                current_app.logger.error(str(e))
                db.session.rollback()
    return generate_response(code_msg=Code.APPLY_DEVICE_AUDIT_FAILED)
