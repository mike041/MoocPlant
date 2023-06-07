# -*- encoding: utf-8 -*-
"""
@File    :   common.py
@Time    :   2022/12/26 21:35
@Author  :   Mushishi 
"""
import datetime
import json

import redis
import requests
import os, sys


class HandleRedis(object):
    def __init__(self) -> None:
        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def get_value_str(self, key):
        return self.connect.get(key)

    def get_value_list(self, key):
        '''
        根据key，获取一个list所有值
        '''
        return self.connect.lrange(key, 0, -1)

    def get_value_dict(self, key):
        '''
        根据key获取dict
        '''
        return self.connect.hgetall(key)

    def set_value(self, key, value):
        '''
        自动根据value类型添加值
        '''
        if isinstance(value, str):
            self.connect.set(key, value, ex=86400)
        if isinstance(value, list):
            self.connect.rpush(key, *value)
        if isinstance(value, dict):
            self.connect.hmset(key, value)


def robot_message(name, text, channel='', send_type='personal'):
    if send_type == 'personal' and not channel.__contains__('@'):
        channel = '@' + channel
    # mind推送
    url = "https://mind.im30.net/api/hooks/mq6bi815w7gxdqufs1grmkwadw"
    data = {
        "text": f"{text}",
        "channel": channel,
        "username": name}
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.request("POST", url, headers=headers, data=payload)


def change_system_date(data):
    date = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=8)
    command = 'sudo date -s "{}"'.format(date)
    os.system(command)
    # sys.exit()

# handle_redis = HandleRedis()
