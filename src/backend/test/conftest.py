#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/11 10:53
"""

import pytest

from test.utils import init_db


@pytest.fixture(scope="session")
def init():
    print("initializing db..........")
    init_db()
