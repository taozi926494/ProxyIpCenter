#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : proxy.py
# @Time    : 2019-2-27 11:31
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 从IP代理商取得IP的模块

import json
from urllib.parse import urlencode

import requests
def obtain_ip(url, method, get_params={}, post_params={}):
    """
    发出请求从IP服务提供商获取IP
    :param url: 请求地址
    :param method: 请求方法
    :param get_params: get请求参数
    :param post_params: post请求参数
    :return:
    """
    # ToDo: method == 'POST' method == 'GETPOST'
    if method == 'GET':
        if not get_params:
            return {
                'code': 424,
                'msg': 'Lack of GET params'
            }
        req_url = "%s?%s" % (url, urlencode(get_params))
        response = requests.get(req_url)
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('success'):
                return {
                    'code': 200,
                    'msg': 'Success get ip from ProxyIp Service Provider',
                    'data': result.get('data')
                }
            else:
                return {
                    'code': 424,
                    'msg': 'Get IP return failed message is %s' % result.get('msg')
                }
        else:
            return {
                'code': 424,
                'msg': 'Get IP status not 200'
            }
