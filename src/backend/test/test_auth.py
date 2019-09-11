#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/23 10:01
"""

import pytest

from app.model.user import User
from test.test_user import get_user_url
from test.utils import get_db_session, HOST, http_post, http_get

register_url = HOST + "auth/register"
login_url = HOST + "auth/login"
logout_url = HOST + "auth/logout"


@pytest.fixture()
def delete_test_user():
    session = get_db_session()
    user = session.query(User).filter_by(username='username_test').first()
    if user:
        session.delete(user)
        session.commit()


@pytest.fixture()
def add_test_user():
    session = get_db_session()
    user = session.query(User).filter_by(username='username_test').first()
    if not user:
        user = User(username='username_test',
                    realname="realname_test",
                    email="test@test.com",
                    password="1234")
        session.add(user)
        session.commit()


def test_register_successfully(delete_test_user):
    """
    成功注册
    :param delete_test_user:
    :return:
    """
    data = {"username": "username_test",
            "realname": "realname_test",
            "email": "test@test.com",
            "password": "1234",
            "repeat_password": "1234"}
    result = http_post(register_url, data)
    assert result.json()["code"] == 0
    assert result.json()["data"]["username"] == "username_test"


def test_register_has_exist_user(add_test_user):
    """
    用户名已存在，注册失败
    :param add_test_user:
    :return:
    """
    data = {"username": "username_test",
            "realname": "realname_test",
            "email": "test@test.com",
            "password": "1234",
            "repeat_password": "1234"}
    result = http_post(register_url, data)
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
def test_register_error_parameter(username, realname, email, password, repeat_password):
    """
    使用错误参数注册失败
    :param username:
    :param realname:
    :param email:
    :param password:
    :param repeat_password:
    :return:
    """
    data = {"username": username,
            "realname": realname,
            "email": email,
            "password": password,
            "repeat_password": repeat_password}
    result = http_post(register_url, data)
    assert result.json()['code'] == 1000
    assert result.json()['msg'] == "参数错误"


def test_login_successfully(add_test_user):
    """
    成功登录
    :param add_test_user:
    :return:
    """
    data = {"username": "username_test",
            "password": "1234"}
    result = http_post(login_url, data)
    assert result.json()['code'] == 0
    assert result.json()['data']['username'] == 'username_test'
    assert result.json()['data']['access_token']


def test_login_disable_user(add_test_user):
    """
    已被禁用的用户无法登录
    :param add_test_user:
    :return:
    """
    session = get_db_session()
    user = session.query(User).filter_by(username='username_test').first()
    user.status = 0
    session.add(user)
    session.commit()
    data = {"username": "username_test",
            "password": "1234"}
    result = http_post(login_url, data)
    assert result.json()['code'] == 2002
    assert result.json()['msg'] == "用户已被禁用"


@pytest.mark.parametrize("username,password", [
    ("username_test", "12345"),
    ("username_test_wrong", "1234"),
])
def test_login_error(add_test_user, username, password):
    """
    用户名或密码不正确，登录失败
    :param add_test_user:
    :param username:
    :param password:
    :return:
    """
    data = {"username": username,
            "password": password}
    result = http_post(login_url, data)
    assert result.json()['code'] == 2003
    assert result.json()['msg'] == "用户名或密码无效"


def test_logout_successfully(admin_token):
    """
    注销用户成功
    :param admin_token:
    :return:
    """
    result = http_get(logout_url, token=admin_token)
    assert result.json()['code'] == 0
    result = http_get(get_user_url.format(user_id=1), token=admin_token)
    assert result.status_code == 401
    assert result.json()['code'] == 1002
    assert result.json()['msg'] == "认证错误"
