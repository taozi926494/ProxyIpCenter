#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2019-2-27 10:44
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com

import os
import json
import time

from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


from ProxyIpCenter.db_base import init_database


from ProxyIpCenter.proxy_ip.controller import bp_proxy_ip
app.register_blueprint(bp_proxy_ip)

def run_app():
    database_url = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'ProxyIpCenter.db')
    app.config.update(dict(
        SQLALCHEMY_DATABASE_URI=database_url,
    ))
    init_database()
    app.run(debug=True)
    # app.run(threaded=True)
