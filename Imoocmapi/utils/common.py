# -*- encoding: utf-8 -*-
"""
@File    :   common.py
@Time    :   2022/12/26 21:35
@Author  :   Mushishi 
"""
import redis


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


handle_redis = HandleRedis()
