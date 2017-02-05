#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname


sys.path.insert(0, abspath(dirname(__file__)))

# 不同的项目导入的是不一样的
from app import init_app
application = init_app()
# wsgi需要一个application变量来引用Flask的实例
# from app import app as application
