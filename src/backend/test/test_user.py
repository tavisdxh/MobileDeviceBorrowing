#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/26 11:47
"""
from app.model.user import User
from test.utils import get_db_session


def setup_admin_user():
    session = get_db_session()
    user = session.query(User).filter_by(username='admin').first()
    if not user:
        user = User(username='admin',
                    realname="admin",
                    email="admin@admin.com",
                    password="admin",
                    status=1
                    )
        session.add(user)
        session.commit()
