#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/23 10:04
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

HOST = "http://127.0.0.1:5000/api/"


def get_db_session():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    return Session()
