#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import main as init_app

sys.path.insert(0, abspath(dirname(__file__)))

# 不同的项目导入的是不一样的

application = init_app.configured_app()
# wsgi需要一个application变量来引用Flask的实例
# from app import app as application

