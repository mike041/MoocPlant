# -*- encoding: utf-8 -*-
"""
@File    :   common.py
@Time    :   2022/12/26 21:35
@Author  :   Mushishi 
"""
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
import os

secret_id = settings.OSS_SECRET_ID
secret_key = settings.OSS_SECRET_KEY


def upload_file(local_file_path):
    remote_file = 'moocplant/{}'.format(os.path.basename(local_file_path))
    region = 'ap-beijing'
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)
    try:
        response = client.upload_file(
            Bucket='typora-1252339543',
            LocalFilePath=local_file_path,
            Key=remote_file,
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        if len(response.get("ETag"))>5:
            return "https://typora-1252339543.cos.ap-beijing.myqcloud.com/moocplant/{}".format(os.path.basename(local_file_path))
    except:
        return False
