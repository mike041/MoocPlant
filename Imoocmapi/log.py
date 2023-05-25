"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: log.py
@Site:
@time: 2023.02.08
"""
import logging
import os
import time

logger = logging.getLogger()
rootpath = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists("logs"):
    os.mkdir("logs")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
filename = os.path.join(rootpath, 'logs', f"log_{time.strftime('%Y%m%d')}.log")
fh = logging.FileHandler(filename=filename)

formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
formatter2 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter2)
logger.addHandler(ch)  # 将日志输出至屏幕
logger.addHandler(fh)  # 将日志输出至文件
