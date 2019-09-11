#!/usr/bin/env python
# coding=UTF-8
"""
Desc：
Author：TavisD 
Time：2019/8/22 10:51
"""

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
app = create_app(os.getenv('FLASK_ENV') or 'default')
manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
