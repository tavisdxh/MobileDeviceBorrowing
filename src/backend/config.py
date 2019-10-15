#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 10:24
"""

import logging
import os
from pathlib import Path

from apscheduler.jobstores.redis import RedisJobStore
from concurrent_log_handler import ConcurrentRotatingFileHandler


def set_log(app, level):
    Path(__file__).cwd().joinpath("logs").mkdir(parents=True, exist_ok=True)
    file_log_handler = ConcurrentRotatingFileHandler("logs/log", maxBytes=50 * 1024 * 1024, backupCount=5,
                                                     encoding="UTF-8")
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]%(message)s")
    file_log_handler.setFormatter(formatter)
    file_log_handler.setLevel(level)
    app.logger.addHandler(file_log_handler)


class Config:
    SECRET_KEY = "Mobile Device Borrowing by Tavis D"
    # database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # apscheduler
    SCHEDULER_JOBSTORES = {
        'default': RedisJobStore()
    }
    # redis
    REDIS_HOST = os.environ.get('REDIS_HOST') or '127.0.0.1'
    REDIS_URL = "redis://{host}:6379/0".format(host=REDIS_HOST)
    # jwt
    JWT_SECRET_KEY = 'Mobile Device Borrowing by Tavis D'
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 900秒=15min * 60
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    # marshmallow
    JSON_SORT_KEYS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath("dev.db"))

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        set_log(app, cls.LOG_LEVEL)


class ProConfig(Config):
    LOG_LEVEL = logging.INFO
    DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '123456'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}/mobile_device_borrowing?charset=utf8mb4".format(
        user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        set_log(app, cls.LOG_LEVEL)


config = {'dev': DevConfig, 'pro': ProConfig, 'default': DevConfig}
