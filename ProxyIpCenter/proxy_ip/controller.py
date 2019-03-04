#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : controller.py
# @Time    : 2019-2-27 11:02
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
import time

from flask import Blueprint, request, jsonify
from ProxyIpCenter import app
from threading import Lock
from ProxyIpCenter.proxy_ip.model import ProxyIpRecord, ProxyIpStorage
from ProxyIpCenter.config.model import Config
from ProxyIpCenter.proxy_ip import proxy

lock = Lock()

bp_proxy_ip = Blueprint('bp_proxy_ip', __name__)


@app.route('/get_proxy_ip', methods=['GET'])
def get_proxy_ip():
    """
    获取代理IP的接口
    :return:
    """
    req_keys = request.args.keys()
    if 'timestamp' not in req_keys or 'project' not in req_keys:
        return jsonify({
            'code': 400,
            'msg': 'Lack of request params, need `timestamp` `project`'
        })

    req_time = request.args.get('timestamp', type=int)
    if not req_time:
        return jsonify({
            'code': 400,
            'msg': 'Param `timestamp` must be Int Number bigger than 0 !'
        })

    # 把请求参数转字典，将之后传递给请求代理IP函数的无用的参数pop出去
    req_args = request.args.to_dict()
    req_project = req_args.pop('project')
    req_args.pop('timestamp')
    req_obtain_num = request.args.get('obtain_num', type=int)

    # 加锁，同一时间只处理一个请求，避免重复更新IP
    with lock:
        # 获取最后一次代理IP请求数据
        last_record = ProxyIpRecord.query.order_by(ProxyIpRecord.id.desc()).limit(1).scalar()
        # 系统第一次启动last_record不存在
        last_proxy_record_time = 0
        if last_record:
            # 最后一次代理IP获取的时间
            last_proxy_record_time = int(last_record.date_created.timestamp())
            system_nowtime = int(time.time())
            # 系统的时间和请求的时间不能相差太大
            if abs(system_nowtime - req_time) > 30:
                return jsonify({
                    'code': 400,
                    'msg': 'Your time differ server\'s time more than 30 seconds'
                })

        # 获取代理IP的配置信息
        obtain_num = req_obtain_num if req_obtain_num else int(Config.get('proxy_obtain_num'))
        # 代理过期时间等于上一次请求代理IP的时间加上存活时间
        live_seconds = int(Config.get('proxy_live_seconds'))
        proxy_expire_time = last_proxy_record_time + live_seconds

        # 如果请求切换IP的时间 大于 代理过期时间
        # 表明当前数据库IP已经失效，请求新的IP
        if proxy_expire_time < req_time:
            # ToDO 从数据库里面取代理IP配置信息
            conf_args = {
                'num': obtain_num,
                'type': 2,
                'pack': 37479
            }
            conf_url = 'http://webapi.http.zhimacangku.com/getip'
            conf_args.update(req_args)
            response = proxy.obtain_ip(url=conf_url
                                       , method='GET'
                                       , get_params=conf_args)

            if response['code'] == 200:
                # 刷新存储代理IP的数据库数据
                ProxyIpStorage.refresh_storage(response['data'])
                # 添加IP请求数据
                req_ip = request.remote_addr
                ProxyIpRecord.insert_one(req_ip=req_ip, req_project=req_project
                                         , obtain_num=obtain_num, live_seconds=live_seconds)
                response['proxy_expire_time'] = int(time.time()) + live_seconds
            return jsonify(response)

        else:
            ret_data = {
                'code': 302,
                'msg': 'IP is still living',
                'proxy_expire_time': proxy_expire_time,
                'data': ProxyIpStorage.query_all()
            }
            return jsonify(ret_data)
