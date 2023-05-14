# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py
@Time    :   2022/10/27 15:49
@Author  :   Mushishi 
"""
import json
import random


def parse_json_file(filepath):
    with open(filepath, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        return json_data


def getRandom(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    digits = "0123456789"
    ascii_letters = "abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def randomkey(li: list):
    index = random.randrange(0, len(li), 1)
    return li[index]
