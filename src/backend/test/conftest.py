#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/9/11 10:53
"""
import sqlite3
from pathlib import Path

import pytest

db_file = str(Path(__file__).parent.parent.joinpath("dev.db"))

@pytest.fixture(scope="session")
def init():
    print("initializing db..........")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open(str(Path(__file__).parent.joinpath("data.sql")), encoding="utf-8") as f:
        cursor.executescript(f.read())
        conn.commit()
    cursor.close()
    conn.close()
