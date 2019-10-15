#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/10/15 15:31
"""
import pytest
from test.utils import HOST, http_get, http_post, get_db_session

apply_url = HOST + "device/apply/{device_id}"
return_url = HOST + "device/return/{apply_id}"
audit_url = HOST + "device/audit/{apply_id}"


@pytest.fixture
def empty_device_apply_record():
    def _empty(device_id, apply_id=None):
        session = get_db_session()
        session.execute("delete from main.device_apply_record where device_id={device_id}".format(device_id=device_id))
        session.commit()
        if apply_id:
            session.execute("delete from main.device_apply_record where id={id}".format(id=apply_id))
            session.commit()

    return _empty


def test_apply_device_successful(admin_token, empty_device_apply_record):
    """
    申请设备成功
    :param admin_token:
    :param empty_device_apply_record:
    :return:
    """
    empty_device_apply_record(1)
    data = {
        "start_time": "2019-10-15 09:28:55", "end_time": "2019-10-30 00:55:55", "application_desc": "测试需要"
    }
    result = http_post(apply_url.format(device_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_apply_device_failed_not_available(admin_token):
    """
    申请设备失败，设备不可用
    :param admin_token:
    :return:
    """
    data = {
        "start_time": "2019-10-15 09:28:55", "end_time": "2019-10-30 00:55:55", "application_desc": "测试需要"
    }
    result = http_post(apply_url.format(device_id=9999), data=data, token=admin_token)
    assert result.json()['code'] == 3004
    assert result.json()['msg'] == "设备不可用"


def test_apply_device_failed_duplicate_apply(admin_token, empty_device_apply_record):
    """
    申请设备失败，重复申请
    :param admin_token:
    :param empty_device_apply_record:
    :return:
    """
    empty_device_apply_record(1)
    data = {
        "start_time": "2019-10-15 09:28:55", "end_time": "2019-10-30 00:55:55", "application_desc": "测试需要"
    }
    http_post(apply_url.format(device_id=1), data=data, token=admin_token)
    result = http_post(apply_url.format(device_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 3005
    assert result.json()['msg'] == "重复申请"


def test_return_back_successful(admin_token, empty_device_apply_record, execute_sql):
    """
    归还设备成功
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
    INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 6, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
    """
    execute_sql(sql)
    result = http_get(return_url.format(apply_id=1), token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_return_back_failed(admin_token, empty_device_apply_record):
    """
    归还设备失败
    :param admin_token:
    :param empty_device_apply_record:
    :return:
    """
    empty_device_apply_record(1, 999)
    result = http_get(return_url.format(apply_id=999), token=admin_token)
    assert result.json()['code'] == 3006
    assert result.json()['msg'] == "归还失败"


def test_return_back_failed_wrong_status(admin_token, empty_device_apply_record, execute_sql):
    """
    归还设备失败，错误的设备状态
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
        INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 3, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
        """
    execute_sql(sql)
    result = http_get(return_url.format(apply_id=1), token=admin_token)
    assert result.json()['code'] == 3006
    assert result.json()['msg'] == "归还失败"


def test_admin_approval_apply_successful(admin_token, empty_device_apply_record, execute_sql):
    """
    admin审批通过apply的记录
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
            INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 1, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
            """
    execute_sql(sql)
    data = {"approval": 1, "reason": "admin审批apply记录，通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_admin_not_approval_apply_successful(admin_token, empty_device_apply_record, execute_sql):
    """
    admin不通过apply的记录
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
                INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 1, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
                """
    execute_sql(sql)
    data = {"approval": 0, "reason": "admin审批apply记录，不通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_admin_approval_return_successful(admin_token, empty_device_apply_record, execute_sql):
    """
    admin通过return记录
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
    INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 4, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
    """
    execute_sql(sql)
    data = {"approval": 1, "reason": "admin审批return记录，通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_admin_not_approval_return_successful(admin_token, empty_device_apply_record, execute_sql):
    """
    admin不通过return记录
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
        INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 4, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
        """
    execute_sql(sql)
    data = {"approval": 0, "reason": "admin审批return记录，不通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_admin_approval_return_failed(admin_token, empty_device_apply_record, execute_sql):
    """
    审批记录失败
    :param admin_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """
            INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 1, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 3, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
            """
    execute_sql(sql)
    data = {"approval": 0, "reason": "admin审批return记录，不通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=admin_token)
    assert result.json()['code'] == 3007
    assert result.json()['msg'] == "审批失败"


def test_owner_approval_apply_successful(test1_token, empty_device_apply_record, execute_sql):
    """
    owner通过申请
    :param test1_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 4, 2, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 1, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
    """
    execute_sql(sql)
    data = {"approval": 1, "reason": "owner审批apply记录，通过"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=test1_token)
    assert result.json()['code'] == 0
    assert result.json()['msg'] == "ok"


def test_owner_approval_apply_failed(test1_token, empty_device_apply_record, execute_sql):
    """
    owner审批失败，不能审批其他owner的
    :param test1_token:
    :param empty_device_apply_record:
    :param execute_sql:
    :return:
    """
    empty_device_apply_record(1, 1)
    sql = """INSERT INTO "main"."device_apply_record"("id", "device_id", "applicant_id", "start_time", "end_time", "application_desc", "status", "apply_auditor_id", "return_auditor_id", "apply_audit_reason", "return_audit_reason", "notify_status", "notify_count", "create_time", "update_time") VALUES (1, 1, 2, '2019-10-15 09:28:55', '2019-10-30 00:55:55', '测试需要', 1, NULL, NULL, NULL, NULL, 0, 0, '2019-10-15 16:16:48.399755', '2019-10-15 16:16:48.399755');
    """
    execute_sql(sql)
    data = {"approval": 1, "reason": "owner审批apply记录，失败"}
    result = http_post(audit_url.format(apply_id=1), data=data, token=test1_token)
    assert result.json()['code'] == 3007
    assert result.json()['msg'] == "审批失败"
