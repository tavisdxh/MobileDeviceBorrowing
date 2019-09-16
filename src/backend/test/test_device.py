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


def test_get_device_successful(admin_token):
    result = http_get(get_device_url.format(device_id=1), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data']['id'] == 1


def test_get_device_failed(admin_token):
    result = http_get(get_device_url.format(device_id=999), token=admin_token)
    assert result.json()['code'] == 3002
    assert result.json()['msg'] == "获取设备信息失败"


def test_add_device_successful(admin_token):
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
    params = {"page": 1, "per_page": 2}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['data'][0]["id"] == 1


def test_get_devices_successful_by_filter(admin_token):
    params = {"page": 1, "per_page": 20, "brand": "Apple", "model": "apple"}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['total'] == 2


def test_get_devices_successful_empty(admin_token):
    params = {"page": 1, "per_page": 20, "model": "test"}
    result = http_get(get_devices_url, params=params, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['total'] == 0
