#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/10/18 17:39
"""
from test.utils import HOST, http_post, http_get

add_role_url = HOST + "role/add"
update_role_url = HOST + "role/update/{role_id}"
delete_role_url = HOST + "role/delete/{role_id}"
get_role_url = HOST + "role/get/{role_id}"
get_roles_url = HOST + "role/get_roles"


def test_add_role_successful(admin_token, execute_sql):
    """
    添加角色成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
    DELETE FROM "main"."role" WHERE name="角色1";
    """
    execute_sql(sql)
    data = {"name": "角色1", "desc": "描述1"}
    result = http_post(add_role_url, data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_add_role_failed_already_exist(admin_token, execute_sql):
    """
    添加角色失败，已存在的角色
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
    INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (999, '角色1', '描述1', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
    """
    execute_sql(sql)
    data = {"name": "角色1", "desc": "描述1"}
    result = http_post(add_role_url, data=data, token=admin_token)
    assert result.json()['code'] == 4000
    assert result.json()['msg'] == "角色已存在"


def test_update_role_successful(admin_token, execute_sql):
    """
    更新角色成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
        INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (998, '角色998', '描述998', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
        """
    execute_sql(sql)
    data = {"name": "角色998_new", "desc": "描述998"}
    result = http_post(update_role_url.format(role_id=998), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_update_role_failed(admin_token, execute_sql):
    """
    更新角色失败，不存在的角色
    :param admin_token:
    :param execute_sql:
    :return:
    """
    data = {"name": "角色997", "desc": "描述998"}
    result = http_post(update_role_url.format(role_id=997), data=data, token=admin_token)
    assert result.json()['code'] == 4002
    assert result.json()['msg'] == "角色不存在"


def test_update_role_failed_already_exist(admin_token, execute_sql):
    """
    更新角色失败，角色重名
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
        INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (996, '角色996', '描述996', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
        """
    execute_sql(sql)
    data = {"name": "角色996", "desc": "描述996"}
    result = http_post(update_role_url.format(role_id=996), data=data, token=admin_token)
    assert result.json()['code'] == 4000
    assert result.json()['msg'] == "角色已存在"


def test_delete_role_successful(admin_token, execute_sql):
    """
    删除角色成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql1 = """
    DELETE FROM "main"."role" where id=995;
    """
    sql2 = """
    DELETE FROM role_permission where role_id=995;
    """
    sql3 = """
            INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (995, '角色995', '描述995', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
            """
    execute_sql(sql1)
    execute_sql(sql2)
    execute_sql(sql3)
    result = http_get(delete_role_url.format(role_id=995), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_delete_role_failed(admin_token, execute_sql):
    """
    删除角色失败
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
    DELETE FROM "main"."role" where id=994;
    """
    execute_sql(sql)
    result = http_get(delete_role_url.format(role_id=994), token=admin_token)
    assert result.json()['code'] == 4002
    assert result.json()['msg'] == "角色不存在"


def test_get_role_successful(admin_token):
    """
    获取角色详情成功
    :param admin_token:
    :return:
    """
    result = http_get(get_role_url.format(role_id=2), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert result.json()['data']['id'] == 2


def test_get_role_failed(admin_token):
    """
    获取角色信息失败
    :param admin_token:
    :return:
    """
    result = http_get(get_role_url.format(role_id=993), token=admin_token)
    assert result.json()['code'] == 4002
    assert result.json()['msg'] == "角色不存在"


def test_get_roles_successful(admin_token):
    """
    获取角色列表成功
    :param admin_token:
    :return:
    """
    result = http_get(get_roles_url + "?page=1&per_page=2", token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()['data']) == 2
    assert result.json()['per_page'] == 2


def test_get_roles_successful_empty(admin_token):
    """
    获取角色列表成功，空列表
    :param admin_token:
    :return:
    """
    result = http_get(get_roles_url + "?page=10&per_page=10", token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()['data']) == 0
    assert result.json()['per_page'] == 10
