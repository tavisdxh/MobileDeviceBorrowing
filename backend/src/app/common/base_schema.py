#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 14:43
"""

from marshmallow import Schema


class BaseSchema(Schema):
    class Meta:
        ordered = True
        datetimeformat = '%Y-%m-%d %H:%M:%S'
