#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/23 10:04
"""
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


HOST = "http://127.0.0.1:5000/api/"
db_file = str(Path(__file__).cwd().parent.joinpath("dev.db"))


def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open("data.sql", encoding="utf-8") as f:
        cursor.executescript(f.read())
        conn.commit()
    cursor.close()
    conn.close()


def get_db_session():
    engine = create_engine('sqlite:///' + db_file)
    Session = sessionmaker(bind=engine)
    return Session()

