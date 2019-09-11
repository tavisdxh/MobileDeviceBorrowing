#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/26 11:47
"""
import pytest

from test.utils import HOST, http_post, http_get

get_user_url = HOST + "user/get_user/{user_id}"
update_user_url = HOST + "user/update_user/{user_id}"
update_password_url = HOST + "user/update_password/{user_id}"
delete_user_url = HOST + "user/delete_user/{user_id}"
get_users_url = HOST + "user/get_users"


def test_get_user_successfully(admin_token):
    """
    成功获取自己的信息，admin用户。admin_or_has_permission_self权限测试。
    :param admin_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=1), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['username'] == 'admin'


def test_get_user_admin_get_other_user_successfully(admin_token):
    """
    成功获取其他用户信息，admin用户。admin_or_has_permission_self权限测试。
    :param admin_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=2), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['id'] == 2


def test_get_user_normal_user_get_own_profile_successfully(test1_token):
    """
    成功获取自己的信息，有权限用户。admin_or_has_permission_self权限测试。
    :param test1_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=2), token=test1_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['id'] == 2


def test_get_user_normal_user_get_other_user_failed(test1_token):
    """
    获取他人信息失败，有权限用户。admin_or_has_permission_self权限测试。
    :param test1_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=3), token=test1_token)
    assert result.status_code == 403
    assert result.json()['code'] == 1003
    assert result.json()['msg'] == "无权限访问"


def test_get_user_not_has_permission_failed(test3_token):
    """
    获取用户信息失败，无权限。admin_or_has_permission_self权限测试。
    :param test3_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=4), token=test3_token)
    assert result.status_code == 403
    assert result.json()['code'] == 1003
    assert result.json()['msg'] == "无权限访问"


def test_get_user_not_exist_user_failed(admin_token):
    """
    获取用户信息失败
    :param admin_token:
    :return:
    """
    result = http_get(get_user_url.format(user_id=999), token=admin_token)
    assert result.json()['code'] == 2004
    assert result.json()['msg'] == "获取用户资料失败"


def test_update_user_successfully(admin_token):
    """
    更新用户信息成功
    :param admin_token:
    :return:
    """
    data = {"username": "admin", "realname": "new_admin", "email": "new@admin.com"}
    result = http_post(update_user_url.format(user_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['realname'] == "new_admin"
    assert result.json()['data']['email'] == "new@admin.com"


@pytest.mark.parametrize("user_id,username,realname,email", [
    (1, "test1", "admin", "admin@admin.com"),
    (999, "test999", "test999", "test999@test.com")
])
def test_update_user_failed(admin_token, user_id, username, realname, email):
    """
    更新用户信息失败
    :param admin_token:
    :return:
    """
    data = {"username": username, "realname": realname, "email": email}
    result = http_post(update_user_url.format(user_id=user_id), data=data, token=admin_token)
    assert result.json()['code'] == 2005
    assert result.json()['msg'] == "更新用户资料失败"


def test_update_password_successfully(test1_token):
    """
    修改密码成功
    :param test1_token:
    :return:
    """
    data = {"old_password": "test1", "new_password": "test1_new", "repeat_password": "test1_new"}
    result = http_post(update_password_url.format(user_id=2), data=data, token=test1_token)
    assert result.json()['code'] == 0


def test_update_password_failed(admin_token):
    """
    修改密码失败，原密码校验不通过
    :param admin_token:
    :return:
    """
    data = {"old_password": "admin_old", "new_password": "admin_new", "repeat_password": "admin_new"}
    result = http_post(update_password_url.format(user_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 2006
    assert result.json()['msg'] == "密码不一致"


def test_update_password_failed_repeat_password(admin_token):
    """
    修改密码失败，新密码输入不一致
    :param admin_token:
    :return:
    """
    data = {"old_password": "admin", "new_password": "admin_new1", "repeat_password": "admin_new2"}
    result = http_post(update_password_url.format(user_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 1000
    assert result.json()['data']['_schema'] == ['password must be equivalent']


def test_delete_user_successfully_by_admin(admin_token):
    """
    成功删除用户，admin用户。admin_or_has_permission权限测试。
    :param admin_token:
    :return:
    """
    result = http_get(delete_user_url.format(user_id=5), token=admin_token)
    assert result.json()['code'] == 0


def test_delete_user_successfully_has_permission(test2_token):
    """
    成功删除用户，普通用户，有权限。admin_or_has_permission权限测试。
    :param test2_token:
    :return:
    """
    result = http_get(delete_user_url.format(user_id=5), token=test2_token)
    assert result.json()['code'] == 0


def test_delete_user_failed_without_permission(test3_token):
    """
    删除用户失败，无权限。admin_or_has_permission权限测试。
    :param test3_token:
    :return:
    """
    result = http_get(delete_user_url.format(user_id=4), token=test3_token)
    assert result.json()['code'] == 1003
    assert result.json()['msg'] == "无权限访问"


def test_get_users_successfully(admin_token):
    """
    成功获取用户列表
    :param admin_token:
    :return:
    """
    params = {"page": 2, "per_page": 3}
    result = http_get(get_users_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['per_page'] == 3
    assert result.json()['page'] == 2
    assert result.json()['data'][0]["username"] == "test3"


def test_get_users_by_filter(admin_token):
    """
    成功获取用户列表，使用参数过滤功能
    :param admin_token:
    :return:
    """
    params = {"page": 1, "per_page": 3, "username": "test1", "realname": "test1", "email": "test1@test1.com",
              "status": 1}
    result = http_get(get_users_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data'][0]["username"] == "test1"
