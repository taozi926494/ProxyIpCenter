#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : run.py
# @Time    : 2019-2-27 10:44
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# ProxyCenter运行文件

import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)


from ProxyIpCenter import run_app

run_app()