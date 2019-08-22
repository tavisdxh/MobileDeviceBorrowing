#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 15:35
"""
from marshmallow import fields
from marshmallow.validate import Length

from app.common.base_schema import BaseSchema


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "id", "username", "realname", "email", "status", "create_time", "update_time")

    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True, validate=Length(min=4, max=32))
    realname = fields.Str(required=True, validate=Length(min=2, max=10))
    email = fields.Email(required=True)


user_schema = UserSchema()
