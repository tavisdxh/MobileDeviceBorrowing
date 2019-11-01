#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/23 10:04
"""
import sqlite3
from pathlib import Path

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DevConfig

HOST = "http://127.0.0.1:5000/api/"


def get_db_session():
    engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    return Session()


def http_get(url, params=None, token=None):
    headers = {}
    print("\nGet url: ", url)
    if token:
        headers = {"Authorization": "Bearer " + str(token)}
        print("Token ", headers)
    if params:
        print("Params: ", params)
    else:
        params = {}
    result = requests.get(url, params=params, headers=headers)
    print("Response code: ", result.status_code)
    print("Response body: ", result.json())
    return result


def http_post(url, data, token=None):
    headers = {}
    print("\nPost url: ", url)
    if token:
        headers = {"Authorization": "Bearer " + str(token)}
        print("Token ", headers)
    print("Data: ", data)
    result = requests.post(url, json=data, headers=headers)
    print("Response code: ", result.status_code)
    print("Response body: ", result.json())
    return result
