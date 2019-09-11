#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 15:26
"""
import datetime

from app import db


class User(db.Model):
    __table__name = 'user'
    __table_args__ = {"extend_existing": True, 'comment': '用户表'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False, comment='用户名')
    password = db.Column(db.String(128), nullable=False, comment='密码')
    realname = db.Column(db.String(32), nullable=False, comment='真实姓名')
    email = db.Column(db.String(40), nullable=False, comment='邮箱')
    status = db.Column(db.Integer, default=1, comment="状态，1：启用，0：禁用")
    roles = db.relationship("Role", backref="user", secondary="user_role")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    def __repr__(self):
        return '<User id={id} username={username}>'.format(id=self.id, username=self.username)


class Role(db.Model):
    __table__name = 'role'
    __table_args__ = {"extend_existing": True, 'comment': '角色表'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), index=True, nullable=False, comment='角色名')
    desc = db.Column(db.String(50), comment='描述')
    permissions = db.relationship("Permission", backref="role", secondary="role_permission")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    def __repr__(self):
        return '<Role id={id} name={name}>'.format(id=self.id, name=self.name)


# 用户和角色表  多对多关系必须创建单独的表来记录关联数据
User_Role = db.Table("user_role",
                     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                     db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True))


class Permission(db.Model):
    __table__name = 'permission'
    __table_args__ = {"extend_existing": True, 'comment': '权限表'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(200), index=True, nullable=False, comment='权限路径')
    name = db.Column(db.String(20), nullable=False, comment='权限名')
    desc = db.Column(db.String(50), comment='描述')
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    def __repr__(self):
        return '<Permission id={id} name={name}>'.format(id=self.id, name=self.name)


# 角色权限表
Role_Permission = db.Table("role_permission",
                           db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
                           db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True))
