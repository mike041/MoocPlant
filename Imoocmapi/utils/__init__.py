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

sys_name = os.name


class MESSAGE_TYPES:
    ROBOT = 'robot'
    TEXT = 'text'
    BI = 'bi'


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
    sdk = 'open_im_sdk_electron' if sys_name == 'posix' else 'mind_ws_server_win.exe'

    if pids is [] or pids == ['']:
        _cmd = 'taskkill /f /im %s' % f'{sdk}' if sys_name == 'posix' else f"sudo ps -ef | grep {sdk} | grep -v grep " + "| awk '{print $2}' | xargs kill -9"
        os.system(_cmd)
        return
    command = 'taskkill /f /PID ' if os.name == 'nt' else "sudo kill -9 "
    for pid in pids:
        result = os.system(command + str(pid))
