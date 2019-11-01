#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/11 10:53
"""
import sqlite3
import subprocess
from pathlib import Path

import pytest
import redis
import sqlalchemy
from sqlalchemy import create_engine

from app.model.user import User
from config import DevConfig
from test.utils import http_post, HOST, get_db_session


@pytest.fixture(scope="module", autouse=True)
def init():
    # init db
    data_file = str(Path(__file__).parent.joinpath("data.sql"))
    engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    with open(data_file, encoding="utf-8") as f:
        for line in f.readlines():
            connection.execute(line[:-1])
    # remove redis record
    r = redis.StrictRedis(host=DevConfig.REDIS_HOST)
    r.flushall()


@pytest.fixture(scope="module")
def admin_token():
    session = get_db_session()
    user = session.query(User).filter_by(username='admin').first()
    if not user:
        user = User(id=1,
                    username='admin',
                    realname="admin",
                    email="admin@admin.com",
                    password="admin",
                    status=1
                    )
        session.add(user)
        session.commit()
    data = {"username": "admin",
            "password": "admin"}
    return http_post(HOST + "auth/login", data).json()['data']['access_token']


@pytest.fixture(scope="module")
def test1_token():
    session = get_db_session()
    user = session.query(User).filter_by(username='test1').first()
    if not user:
        user = User(id=2,
                    username='test1',
                    realname="test1",
                    email="test1@test1.com",
                    password="test1",
                    status=1
                    )
        session.add(user)
        session.commit()
    data = {"username": "test1",
            "password": "test1"}
    return http_post(HOST + "auth/login", data).json()['data']['access_token']


@pytest.fixture
def execute_sql():
    def _execute(sql):
        session = get_db_session()
        session.execute(sql)
        session.commit()

    return _execute
