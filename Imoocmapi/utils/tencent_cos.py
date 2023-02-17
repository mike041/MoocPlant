from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

secret_id = settings.OSS_SECRET_ID
secret_key = settings.OSS_SECRET_KEY


class TencentCOS:

    def __init__(self):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = "typora-1252339543"
        self.region = "ap-beijing"
        self.token = None
        self.scheme = 'http'

        # 初始化客户端

    def client(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(
            Region=self.region,
            SecretId=self.secret_id,
            SecretKey=self.secret_key,
            Token=self.token,
            Scheme=self.scheme
        )
        # 返回一个初始化的客户端，后续操作都需要基于这个客户端实例
        return CosS3Client(config)

        # 获取对象url

    def get_obj_url(self, bucket, key):
        return self.client().get_object_url(bucket, key)

        # 上传文件，返回上传后的url

    def upload_cos(self, image, key):
        with open(image, 'rb') as fp:
            response = self.client().put_object(
                Bucket=self.bucket,
                Body=fp,
                # key是保存在cos时的名称
                Key=key,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        return self.get_obj_url(self.bucket, key)
