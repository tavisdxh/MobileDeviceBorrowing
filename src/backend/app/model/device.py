#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/12 10:33
"""
import datetime

from app import db


class Device(db.Model):
    __table__name = 'device'
    __table_args__ = {"extend_existing": True, 'comment': '设备信息表'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(15), nullable=False, comment='设备类别，phone|pad')
    brand = db.Column(db.String(32), nullable=False, comment='品牌')
    model = db.Column(db.String(100), nullable=False, comment='设备型号')
    os = db.Column(db.String(15), nullable=False, comment='系统')
    os_version = db.Column(db.String(32), comment='系统版本')
    resolution = db.Column(db.String(32), comment='分辨率')
    asset_no = db.Column(db.String(100), comment='资产编号')
    root = db.Column(db.String(3), default="no", comment='是否root/越狱')
    location = db.Column(db.String(32), default="", comment='所在地')
    status = db.Column(db.Integer, default=1, comment="状态，1：启用，0：禁用，2：使用中")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="所属者")
    current_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="当前使用者")
    owner = db.relationship("User", foreign_keys=[owner_id])
    current_user = db.relationship("User", foreign_keys=[current_user_id])
    desc = db.Column(db.String(500), comment='描述说明')
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    def __repr__(self):
        return '<Device id={id} model={model}>'.format(id=self.id, model=self.model)
