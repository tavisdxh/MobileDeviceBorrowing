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

    # 注册蓝图
    from app.api.auth.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app
