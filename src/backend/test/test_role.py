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
assign_permission_url = HOST + "role/assign_permission/{role_id}"
assign_user_url = HOST + "role/assign_user/{role_id}"
user_assign_role_url = HOST + "role/user_assign_role/{user_id}"


def test_add_role_successful(admin_token, execute_sql):
    """
    添加角色成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
    DELETE FROM "role" WHERE name="角色1";
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
    INSERT INTO "role"("id", "name", "desc", "create_time", "update_time") VALUES (999, '角色1', '描述1', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
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
        INSERT INTO "role"("id", "name", "desc", "create_time", "update_time") VALUES (998, '角色998', '描述998', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
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
        INSERT INTO "role"("id", "name", "desc", "create_time", "update_time") VALUES (996, '角色996', '描述996', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
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
    DELETE FROM "role" where id=995;
    """
    sql2 = """
    DELETE FROM role_permission where role_id=995;
    """
    sql3 = """
            INSERT INTO "role"("id", "name", "desc", "create_time", "update_time") VALUES (995, '角色995', '描述995', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
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
    DELETE FROM "role" where id=994;
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


def test_assign_permission_add_successful(admin_token, execute_sql):
    """
    添加角色权限成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql1 = """
    DELETE FROM role_permission where role_id=3;
    """
    sql2 = """
    INSERT INTO "role_permission"("role_id", "permission_id") VALUES (3, 1);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    data = {"action": "add", "permission_ids": [2, 5]}
    result = http_post(assign_permission_url.format(role_id=3), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_permissions"]) == 3
    assert result.json()["data"]["assigned_permissions"][0]["id"] == 1
    assert result.json()["data"]["assigned_permissions"][1]["id"] == 2
    assert result.json()["data"]["assigned_permissions"][2]["id"] == 5
    assert 2 not in [x["id"] for x in result.json()["data"]["available_permissions"]]
    assert 5 not in [x["id"] for x in result.json()["data"]["available_permissions"]]


def test_assign_permission_remove_successful(admin_token, execute_sql):
    """
    删除角色权限成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql1 = """
    DELETE FROM role_permission where role_id=3;
    """
    sql2 = """
    INSERT INTO "role_permission"("role_id", "permission_id") VALUES (3, 1);
    """
    sql3 = """
    INSERT INTO "role_permission"("role_id", "permission_id") VALUES (3, 4);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    execute_sql(sql3)
    data = {"action": "remove", "permission_ids": [1, 5]}
    result = http_post(assign_permission_url.format(role_id=3), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_permissions"]) == 1
    assert result.json()["data"]["assigned_permissions"][0]["id"] == 4
    assert 1 in [x["id"] for x in result.json()["data"]["available_permissions"]]


def test_assign_user_add_successful(admin_token, execute_sql):
    """
    添加角色用户成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql1 = """
    DELETE FROM user_role where role_id=3;
    """
    sql2 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (3, 3);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    data = {"action": "add", "user_ids": [2, 5]}
    result = http_post(assign_user_url.format(role_id=3), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_users"]) == 3
    assert result.json()["data"]["assigned_users"][0]["id"] == 2
    assert 2 not in [x["id"] for x in result.json()["data"]["available_users"]]


def test_assign_user_remove_successful(admin_token, execute_sql):
    """
    删除角色用户成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql1 = """
    DELETE FROM user_role where role_id=3;
    """
    sql2 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (3, 3);
    """
    sql3 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (5, 3);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    execute_sql(sql3)
    data = {"action": "remove", "user_ids": [2, 5]}
    result = http_post(assign_user_url.format(role_id=3), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_users"]) == 1
    assert result.json()["data"]["assigned_users"][0]["id"] == 3
    assert 2 in [x["id"] for x in result.json()["data"]["available_users"]]
    assert 5 in [x["id"] for x in result.json()["data"]["available_users"]]


def test_user_assign_role_add_successful(admin_token, execute_sql):
    sql1 = """
    DELETE FROM user_role where user_id=4;
    """
    sql2 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (4, 3);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    data = {"action": "add", "role_ids": [1, 3]}
    result = http_post(user_assign_role_url.format(user_id=4), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_roles"]) == 2
    assert result.json()["data"]["assigned_roles"][0]["id"] == 1
    assert 1 not in [x["id"] for x in result.json()["data"]["available_roles"]]


def test_user_assign_role_remove_successful(admin_token, execute_sql):
    sql1 = """
    DELETE FROM user_role where user_id=4;
    """
    sql2 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (4, 3);
    """
    sql3 = """
    INSERT INTO "user_role"("user_id", "role_id") VALUES (4, 2);
    """
    execute_sql(sql1)
    execute_sql(sql2)
    execute_sql(sql3)
    data = {"action": "remove", "role_ids": [1, 2]}
    result = http_post(user_assign_role_url.format(user_id=4), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
    assert len(result.json()["data"]["assigned_roles"]) == 1
    assert result.json()["data"]["assigned_roles"][0]["id"] == 3
    assert 1 in [x["id"] for x in result.json()["data"]["available_roles"]]
