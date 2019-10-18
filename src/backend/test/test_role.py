#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/10/18 17:39
"""
from test.utils import HOST, http_post

add_role_url = HOST + "role/add"
update_role_url = HOST + "role/update/{role_id}"


def test_add_role_successful(admin_token, execute_sql):
    sql = """
    DELETE FROM "main"."role" WHERE name="角色1";
    """
    execute_sql(sql)
    data = {"name": "角色1", "desc": "描述1"}
    result = http_post(add_role_url, data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_add_role_failed_already_exist(admin_token, execute_sql):
    sql = """
    INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (999, '角色1', '描述1', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
    """
    execute_sql(sql)
    data = {"name": "角色1", "desc": "描述1"}
    result = http_post(add_role_url, data=data, token=admin_token)
    assert result.json()['code'] == 4000
    assert result.json()['msg'] == "角色已存在"


def test_update_role_successful(admin_token, execute_sql):
    sql = """
        INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (998, '角色998', '描述998', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
        """
    execute_sql(sql)
    data = {"name": "角色998_new", "desc": "描述998"}
    result = http_post(update_role_url.format(role_id=998), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_update_role_failed(admin_token, execute_sql):
    data = {"name": "角色997", "desc": "描述998"}
    result = http_post(update_role_url.format(role_id=997), data=data, token=admin_token)
    assert result.json()['code'] == 4002
    assert result.json()['msg'] == "角色不存在"


def test_update_role_failed_already_exist(admin_token, execute_sql):
    sql = """
        INSERT INTO "main"."role"("id", "name", "desc", "create_time", "update_time") VALUES (996, '角色996', '描述996', '2019-10-18 17:45:21.690807', '2019-10-18 17:45:21.690807');
        """
    execute_sql(sql)
    data = {"name": "角色996", "desc": "描述996"}
    result = http_post(update_role_url.format(role_id=996), data=data, token=admin_token)
    assert result.json()['code'] == 4000
    assert result.json()['msg'] == "角色已存在"
