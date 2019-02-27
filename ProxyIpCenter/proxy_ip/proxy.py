#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : proxy.py
# @Time    : 2019-2-27 11:31
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
# 从IP代理商取得IP的模块

import json

import requests
def get_ip(num):
    url = 'http://webapi.http.zhimacangku.com/getip?' \
          'num=%s&type=2&pro=&city=0&yys=0&port=1&pack=37479&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    response = requests.get(url % num)
    if response.status_code == 200:
        result = json.loads(response.text)
        if result.get('success'):
            return {
                'code': 200,
                'msg': 'success',
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
