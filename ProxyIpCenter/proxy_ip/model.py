#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : model.py
# @Time    : 2019-2-27 10:59
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 代理IP数据库类
from ProxyIpCenter.db_base import db, Base


class ProxyIpRecord(Base):
    """
    代理IP获取记录表
    """
    __tablename__ = 'proxy_ip_record'
    req_ip = db.Column(db.String(255), comment='请求获取代理IP的IP地址')
    req_project = db.Column(db.String(255), comment='请求获取代理IP的爬虫项目')
    obtain_num = db.Column(db.Integer, comment='本次获取IP的数量')
    live_seconds = db.Column(db.Integer, comment='本次IP的存活时间（秒）')

    @classmethod
    def insert_one(cls, req_ip, req_project, obtain_num, live_seconds):
        record = cls(req_ip=req_ip, req_project=req_project, obtain_num=obtain_num, live_seconds=live_seconds)
        db.session.add(record)
        db.session.commit()

class ProxyIpStorage(Base):
    __tablename__ = 'proxy_ip_storage'
    ip = db.Column(db.String(50))  # ip
    port = db.Column(db.Integer)  # 端口

    @classmethod
    def empty_storage(cls):
        """
        清空数据库里面的数据
        :return:
        """
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def refresh_storage(cls, proxy_ip_list):
        """
        存储代理ip
        :param proxy_ip_list:
        :return:
        """
        # 先清空数据库
        cls.empty_storage()
        save_list = []
        for proxy_ip in proxy_ip_list:
            save_list.append(cls(ip=proxy_ip.get('ip'), port=proxy_ip.get('port')))

        db.session.add_all(save_list)
        db.session.commit()

    @classmethod
    def query_all(cls):
        proxy_ip_list = cls.query.all()
        re_data = []
        for proxy_ip in proxy_ip_list:
            re_data.append({
                'ip': proxy_ip.ip,
                'port': proxy_ip.port,
            })
        return re_data
