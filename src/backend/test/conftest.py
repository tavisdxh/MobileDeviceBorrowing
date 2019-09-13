#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/11 10:53
"""
import sqlite3
from pathlib import Path

import pytest

from app.model.user import User
from test.utils import http_post, HOST, get_db_session

db_file = str(Path(__file__).parent.parent.joinpath("dev.db"))


@pytest.fixture(scope="module", autouse=True)
def init():
    print("\nInitializing db..........")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open(str(Path(__file__).parent.joinpath("data.sql")), encoding="utf-8") as f:
        cursor.executescript(f.read())
        conn.commit()
    cursor.close()
    conn.close()


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
