# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py
@Time    :   2022/10/27 15:49
@Author  :   Mushishi 
"""
import json
import os
import random
import subprocess


def get_process_id(name) -> list:
    child = subprocess.Popen(["pgrep", "-f", name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


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


def task_kill(pids: list):
    if pids is []:
        return
    command = 'taskkill /f /PID ' if os.name == 'nt' else "kill -9 "
    for pid in pids:
        result = os.system(command + str(pid))
