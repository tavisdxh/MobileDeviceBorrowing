#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 11:16
"""
from flask import current_app

from app import app


@app.route('/hello')
def hello_world():
    current_app.logger.info('test hello')
    current_app.logger.error('test error hello')
    return 'Hello, World!'


