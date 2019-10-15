#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 10:42
"""

from flask import Flask
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
app = Flask(__name__)
scheduler = APScheduler()
redis_client = FlaskRedis()
jwt = JWTManager()

# JWT
from app.common.jwt_custom_behavior import *


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    redis_client.init_app(app)
    jwt.init_app(app)

    from app.test import hello_world
    # 引入model
    from app.model.user import User, Role, User_Role, Permission, Role_Permission
    from app.model.device import Device, DeviceApplyRecord

    # 注册蓝图
    from app.api.auth.auth import auth_bp
    from app.api.user.user import user_bp
    from app.api.device.device import device_bp
    from app.api.device.device_apply import device_apply_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(device_bp, url_prefix='/api/device')
    app.register_blueprint(device_apply_bp, url_prefix='/api/device')

    return app
