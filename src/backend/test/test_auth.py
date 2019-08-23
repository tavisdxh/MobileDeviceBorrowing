#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/23 10:01
"""

import pytest
import requests

from app.model.user import User
from test.utils import get_db_session, HOST


@pytest.fixture()
def register_url():
    return HOST + "auth/register"


@pytest.fixture()
def login_url():
    return HOST + "auth/login"


@pytest.fixture()
def setup_delete_user():
    session = get_db_session()
    user = session.query(User).filter_by(username='username_tavisd').first()
    if user:
        session.delete(user)
        session.commit()


@pytest.fixture()
def setup_add_user():
    session = get_db_session()
    user = session.query(User).filter_by(username='username_tavisd').first()
    if not user:
        user = User(username='username_tavisd',
                    realname="TavisD",
                    email="test@tavisd.com",
                    password="1234")
        session.add(user)
        session.commit()


def test_register_successfully(register_url, setup_delete_user):
    data = {"username": "username_tavisd",
            "realname": "TavisD",
            "email": "test@tavisd.com",
            "password": "1234",
            "repeat_password": "1234"}
    result = requests.post(register_url, data)
    assert result.json()["code"] == 0
    assert result.json()["data"]["username"] == "username_tavisd"


def test_register_has_exist_user(register_url, setup_add_user):
    data = {"username": "username_tavisd",
            "realname": "TavisD",
            "email": "test@tavisd.com",
            "password": "1234",
            "repeat_password": "1234"}
    result = requests.post(register_url, data)
    assert result.json()["code"] == 2000
    assert result.json()["msg"] == "用户已存在"


@pytest.mark.parametrize("username,realname,email,password,repeat_password", [
    ('a', "aaaa", "1@1.com", "1234", "1234"),
    ('aaaa', "a", "1@1.com", "1234", "1234"),
    ('aaaa', "aaaa", "test", "1234", "1234"),
    ('aaaa', "aaaa", "1@1.com", "12", "12"),
    ('aaaa', "aaaa", "1@1.com", "1234", "12"),
    ('aaaa', "aaaa", "1@1.com", "1234", "12"),
])
def test_register_error_parameter(register_url, username, realname, email, password, repeat_password):
    data = {"username": username,
            "realname": realname,
            "email": email,
            "password": password,
            "repeat_password": repeat_password}
    result = requests.post(register_url, data)
    assert result.json()['code'] == 1000
    assert result.json()['msg'] == "参数错误"


def test_login_successfully(login_url, setup_add_user):
    data = {"username": "username_tavisd",
            "password": "1234"}
    result = requests.post(login_url, data)
    assert result.json()['code'] == 0
    assert result.json()['data']['username'] == 'username_tavisd'
    assert result.json()['data']['access_token']


@pytest.mark.parametrize("username,password", [
    ("username_tavisd", "12345"),
    ("username_tavis", "1234"),
])
def test_login_error(login_url, setup_add_user, username, password):
    data = {"username": username,
            "password": password}
    result = requests.post(login_url, data)
    assert result.json()['code'] == 2003
    assert result.json()['msg'] == "用户名或密码无效"
