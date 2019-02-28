#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : db_base.py
# @Time    : 2019-2-27 10:51
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 数据库的一些基础配置
import datetime

from ProxyIpCenter import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app, session_options=dict(autocommit=False, autoflush=True))

@app.teardown_request
def teardown_request(exception):
    """
    每一个请求之后该函数，遇到了异常使数据库回滚
    :param exception:
    :return:
    """
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


def get_china_time():
    """
    获取中国制时区时间
    :return: datetime
    """
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))


class Base(db.Model):
    """
    数据库的基类，包含自增id，创建时间，自动更新的修改时间
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=get_china_time)
    date_modified = db.Column(db.DateTime, default=get_china_time, onupdate=get_china_time)


from ProxyIpCenter.proxy_ip.model import *
from ProxyIpCenter.config.model import *


def init_database():
    db.init_app(app)
    db.create_all()

    # 获取ip的数量
    proxy_obtain_num = Config.query.filter_by(name='proxy_obtain_num').scalar()
    if not proxy_obtain_num:
        db.session.add(Config(name='proxy_obtain_num', value='30'))
        db.session.commit()
    # 获取IP的存活时间
    proxy_live_seconds = Config.query.filter_by(name='proxy_live_seconds').scalar()
    if not proxy_live_seconds:
        db.session.add(Config(name='proxy_live_seconds', value='300'))
        db.session.commit()

