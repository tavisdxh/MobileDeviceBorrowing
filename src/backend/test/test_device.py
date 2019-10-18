#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019-09-13 10:05
"""
from test.utils import HOST, http_get, http_post

get_device_url = HOST + "device/get_device/{device_id}"
add_device_url = HOST + "device/add_device"
update_device_url = HOST + "device/update_device/{device_id}"
get_devices_url = HOST + "device/get_devices"
disable_device_url = HOST + "device/disable_device/{device_id}"


def test_get_device_successful(admin_token):
    """
    获取设备详情成功
    :param admin_token:
    :return:
    """
    result = http_get(get_device_url.format(device_id=1), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['id'] == 1


def test_get_device_failed(admin_token):
    """
    获取设备详情失败
    :param admin_token:
    :return:
    """
    result = http_get(get_device_url.format(device_id=999), token=admin_token)
    assert result.json()['code'] == 3002
    assert result.json()['msg'] == "获取设备信息失败"


def test_add_device_successful(admin_token):
    """
    添加设备成功
    :param admin_token:
    :return:
    """
    data = {
        "type": "phone",
        "brand": "小米",
        "model": "小米9 4800万超广角三摄 8GB+256GB",
        "os": "android",
        "os_version": "9.0",
        "resolution": "2340*1080",
        "asset_no": "20150731-4444",
        "root": "yes",
        "location": "广州",
        "owner": {
            "id": 2,
            "realname": "test1"
        },
        "current_user": {
            "id": 2,
            "realname": "test1"
        },
        "desc": "京东链接：https://item.jd.com/100002757767.html"
    }
    result = http_post(add_device_url, data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['model'] == "小米9 4800万超广角三摄 8GB+256GB"


def test_update_device_successful(admin_token):
    """
    更新设备成功
    :param admin_token:
    :return:
    """
    data = {
        "type": "phone",
        "brand": "小米",
        "model": "小米9 4800万超广角三摄 8GB+256GB update",
        "os": "android",
        "os_version": "9.0",
        "resolution": "2340*1080",
        "asset_no": "20150731-5555",
        "root": "yes",
        "location": "北京",
        "owner": {
            "id": 2,
            "realname": "test1"
        },
        "current_user": {
            "id": 2,
            "realname": "test1"
        },
        "desc": "京东链接：https://item.jd.com/100002757767.html"
    }
    result = http_post(update_device_url.format(device_id=4), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['model'] == "小米9 4800万超广角三摄 8GB+256GB update"


def test_update_device_failed(admin_token):
    """
    更新设备失败
    :param admin_token:
    :return:
    """
    data = {
        "type": "phone",
        "brand": "小米",
        "model": "小米9 4800万超广角三摄 8GB+256GB update",
        "os": "android",
        "os_version": "9.0",
        "resolution": "2340*1080",
        "asset_no": "20150731-5555",
        "root": "yes",
        "location": "北京",
        "owner": {
            "id": 2,
            "realname": "test1"
        },
        "current_user": {
            "id": 2,
            "realname": "test1"
        },
        "desc": "京东链接：https://item.jd.com/100002757767.html"
    }
    result = http_post(update_device_url.format(device_id=999), data=data, token=admin_token)
    assert result.json()['code'] == 3001
    assert result.json()['msg'] == "更新设备失败"


def test_get_devices_successful(admin_token):
    """
    获取设备列表成功
    :param admin_token:
    :return:
    """
    params = {"page": 1, "per_page": 2}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data'][0]["id"] == 1


def test_get_devices_successful_by_filter(admin_token):
    """
    使用过滤条件获取设备列表成功
    :param admin_token:
    :return:
    """
    params = {"page": 1, "per_page": 20, "brand": "Apple", "model": "apple"}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['total'] == 2


def test_get_devices_successful_empty(admin_token):
    """
    获取设备列表成功，空列表
    :param admin_token:
    :return:
    """
    params = {"page": 1, "per_page": 20, "model": "test"}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['total'] == 0


def test_admin_disable_device_successful(admin_token, execute_sql):
    """
    admin禁用设备成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
    INSERT INTO "main"."device"("id", "type", "brand", "model", "os", "os_version", "resolution", "asset_no", "root", "location", "status", "owner_id", "current_user_id", "desc", "create_time", "update_time") VALUES (10, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'android', '12.1.4', '1792×828', '20150731-0134', 'no', '北京', 1, 2, 3, '这个是补充信息', '2019-09-13 09:28:55', '2019-10-17 16:34:51.058186');
    """
    execute_sql(sql)
    data = {"disable": "true"}
    result = http_post(disable_device_url.format(device_id=10), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_common_user_disable_device_successful(test1_token, execute_sql):
    """
    普通用户禁用自己的设备成功
    :param test1_token:
    :param execute_sql:
    :return:
    """
    sql = """
    INSERT INTO "main"."device"("id", "type", "brand", "model", "os", "os_version", "resolution", "asset_no", "root", "location", "status", "owner_id", "current_user_id", "desc", "create_time", "update_time") VALUES (11, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'android', '12.1.4', '1792×828', '20150731-0134', 'no', '北京', 1, 2, 3, '这个是补充信息', '2019-09-13 09:28:55', '2019-10-17 16:34:51.058186');
    """
    execute_sql(sql)
    data = {"disable": "true"}
    result = http_post(disable_device_url.format(device_id=11), data=data, token=test1_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_common_user_disable_device_failed(test1_token, execute_sql):
    """
    普通用户禁用他人设备失败
    :param test1_token:
    :param execute_sql:
    :return:
    """
    sql = """
        INSERT INTO "main"."device"("id", "type", "brand", "model", "os", "os_version", "resolution", "asset_no", "root", "location", "status", "owner_id", "current_user_id", "desc", "create_time", "update_time") VALUES (12, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'android', '12.1.4', '1792×828', '20150731-0134', 'no', '北京', 1, 3, 3, '这个是补充信息', '2019-09-13 09:28:55', '2019-10-17 16:34:51.058186');
        """
    execute_sql(sql)
    data = {"disable": "true"}
    result = http_post(disable_device_url.format(device_id=12), data=data, token=test1_token)
    assert result.json()['code'] == 3009
    assert result.json()['msg'] == "禁用失败"


def test_admin_enable_device_successful(admin_token, execute_sql):
    """
    admin启用设备成功
    :param admin_token:
    :param execute_sql:
    :return:
    """
    sql = """
        INSERT INTO "main"."device"("id", "type", "brand", "model", "os", "os_version", "resolution", "asset_no", "root", "location", "status", "owner_id", "current_user_id", "desc", "create_time", "update_time") VALUES (13, 'phone', 'Apple', 'Apple iPhone XR (A2108) 128GB 黑色 移动联通电信4G手机 双卡双待', 'android', '12.1.4', '1792×828', '20150731-0134', 'no', '北京', 0, 2, 3, '这个是补充信息', '2019-09-13 09:28:55', '2019-10-17 16:34:51.058186');
        """
    execute_sql(sql)
    data = {"disable": "false"}
    result = http_post(disable_device_url.format(device_id=13), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"
