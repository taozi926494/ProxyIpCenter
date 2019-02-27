#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : model.py
# @Time    : 2019-2-27 11:29
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 基础配置的ORM类

from ProxyIpCenter.db_base import db, Base

class Config(Base):
    __tablename__ = 'config'
    name = db.Column(db.String(50), unique=True, comment='配置项唯一标识')
    value = db.Column(db.String(255), comment='配置值')

    @classmethod
    def get(cls, conf_name):
        conf_item = cls.query.filter_by(name=conf_name).scalar()
        if conf_item:
            return conf_item.value