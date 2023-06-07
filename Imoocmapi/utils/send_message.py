"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: send_message.py
@Site:
@time: 2023.05.12
"""
# -*- encoding: utf-8 -*-
import time
from multiprocessing import Process
import random

from Imoocmapi import utils
from Imoocmapi.log import logger
from Imoocmapi.utils import MESSAGE_TYPES
from Imoocmapi.utils.common import robot_message
from sdk.mind_im_server import IMServer

'''
@File    :   meeting.py
@Time    :   2022/12/04 16:26:15
@Author  :   Mushishi 
'''
import sys
import os

rootPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(rootPath)

import requests
import websocket
import json

requests.packages.urllib3.disable_warnings()

sys_name = os.name


class User:

    def __init__(self, env='test', phone_number=None):
        self.env = env
        if env == 'test':
            self.BASE_URL = 'http://mind.im30.lan'
            self.BASE_WS = 'ws://10.2.4.100:30000'
        elif env == 'pre':
            self.BASE_URL = 'https://premind.im30.net'
            self.BASE_WS = 'wss://premind.im30.net/ws/web'

        self.groups = []
        self.phone = int(phone_number)

        self.cookie = {}
        self.base_user_id_or_mind_user_id = None
        self.token_or_mind_token = None
        self.home_mind_token = None
        self.mind_teamid = None
        self.session_id = None
        self.mind_im_token = None
        self.mind_im_userid = None
        self.device_id = utils.getRandom(32)
        self.im_cookie = {}

        file_name = 'user_cookie.json' if env == 'pre' else 'test_user_cookie.json'
        self.user_data = utils.parse_json_file(os.path.join(os.path.dirname(rootPath), 'userdata', file_name))
        # self.user_data = utils.parse_json_file(
        #     os.path.join('D:/pythonProject/MoocPlant/Imoocmapi/', 'userdata', file_name))

        self.header = {
            "device-id": self.device_id,
            "accept": "application/json, text/plain",
            "authority": "premind.im30.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows"
        }

        self.message_params = {}

    def login(self):

        def get_verify_code():
            """
            获取手机验证码
            """
            url = self.BASE_URL + "/api/verifyUser/getVerifyCode"
            data = {
                "source": str(self.phone),
                "verifyLoginType": "phone",
                "countryZone": "+86",
                "module": "login",
                "platform": 5,
            }

            send_request(method="get", url=url, data=data, header=self.header)
            # time.sleep(1)

        def mind_login():
            """
            手机登录
            """
            url = self.BASE_URL + "/api/verifyUser/v2/login"
            data = {
                "source": str(self.phone),
                "verifyLoginType": "phone",
                "countryZone": "+86",
                "module": "login",
                "platform": 5,
                "answerCode": "789456"
            }
            res = send_request(method="post", url=url, data=data, header=self.header).json()
            if res.get("code") == 0:
                self.session_id = res.get("data").get("session_id")
                self.token_or_mind_token = res.get("data").get("token")
                self.home_mind_token = res.get("data").get("token")
                self.mind_teamid = res.get("data").get("user").get("team_id")
                self.base_user_id_or_mind_user_id = res.get("data").get("user").get("base_user_id")
                self.cookie = {
                    "MINDTOKEN": self.token_or_mind_token,
                    "MINDTEAMID": str(self.mind_teamid),
                    "MINDUSERID": self.base_user_id_or_mind_user_id,
                    "home_mind_token": self.home_mind_token,
                    "sessionid": self.session_id
                }
            else:
                return False

        def im_login():
            url = self.BASE_URL + "/api/imVerify/login"
            res = send_request(method="post", url=url, data={}, header=self.header, cookie=self.cookie).json()
            if res.get("code") == 0:
                self.mind_im_token = res.get("data").get("im").get("token")
                self.mind_im_userid = res.get("data").get("im").get("user_id")
                self.im_cookie["MINDIMTOKEN"] = self.mind_im_token
                self.im_cookie["MINDIMUSERID"] = self.mind_im_userid
            else:
                return False

        if self.user_data.get(str(self.phone)):
            print('================有缓存不用登录')
            user_json = self.user_data.get(str(self.phone))
            self.cookie = user_json.get('mind_cookie')
            self.base_user_id_or_mind_user_id = user_json.get('mind_cookie').get('MINDUSERID')
            self.token_or_mind_token = user_json.get('mind_cookie').get('MINDTOKEN')
            self.home_mind_token = user_json.get('mind_cookie').get('MINDTOKEN')
            self.mind_teamid = user_json.get('mind_cookie').get('MINDTEAMID')
            self.session_id = user_json.get('mind_cookie').get('sessionid')

            self.im_cookie = user_json.get('im_cookie')
            self.mind_im_token = user_json.get('im_cookie').get('MINDIMTOKEN')
            self.mind_im_userid = user_json.get('im_cookie').get('MINDIMUSERID')

        # 登录步骤 1、获取验证码 2、mind登录 3、im登录
        else:
            get_verify_code()
            mind_login()
            im_login()

    def start(self, receivers=[], groups=[], message_types=[MESSAGE_TYPES.TEXT, ], port=30001, times=1):
        self.ws = websocket.WebSocketApp(
            # url=self.BASE_WS + "/?sendID={}&token={}&platformID=3".format(self.mind_im_userid, self.mind_im_token),
            url=f"ws://127.0.0.1:{int(port)}/?sendID={self.mind_im_userid}&token={self.mind_im_token}&platformID=3",
            on_message=self.on_message,
            on_pong=self.on_pong,
            cookie=json.dumps(self.im_cookie)
        )
        self.ws.on_open = self.on_open

        self.im = {
            'receivers': receivers,
            'groups': groups,
            'message_types': message_types,
            'times': times,
        }

        self.ws.run_forever()

    def send(self):
        message_type = utils.randomkey(self.im.get('message_types'))
        if self.im.get('receivers') == [] and self.im.get('groups') == []:
            logger.info('发随机消息')
            groupID = utils.randomkey(self.groups)
            if message_type == MESSAGE_TYPES.ROBOT:
                robot_message('脚本机器人消息', channel=groupID, send_type='group')
            else:
                self.im_send(groupID=groupID, message_type=message_type)
            return

        for receiver in self.im.get('receivers'):
            # 把手机号转换为im_user_id
            if len(str(receiver)) == 11:
                if self.user_data.get(str(receiver)):
                    user_json = self.user_data.get(str(receiver))
                    user_id = user_json.get('im_cookie').get('MINDIMUSERID')
                else:
                    user_id = str(receiver)
            logger.info(f'向{receiver}发消息')

            if message_type == MESSAGE_TYPES.ROBOT:
                robot_message('脚本机器人消息', channel=user_id, send_type='personal')
            else:
                self.im_send(recvID=user_id, message_type=message_type)

        for group in self.im.get('groups'):
            logger.info(f'向{group}发消息')

            if message_type == MESSAGE_TYPES.ROBOT:
                robot_message('脚本机器人消息', channel=user_id, send_type='group')
            else:
                self.im_send(groupID=str(group), message_type=message_type)

    def im_send(self, recvID='', groupID='', message_type=MESSAGE_TYPES.TEXT):

        def text(character=''):
            message = {
                "text": f"{character}",
                "json": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"{character}"
                                }
                            ]
                        }
                    ]
                },
                "atUserIDList": [

                ],
                "pictures": [

                ],
                "links": [

                ],
                "isAtAll": False
            }
            return message

        def message_body(message_json={}):
            send_time = int(time.time())
            message = {
                "clientMsgID": f"{utils.getRandom(32)}",
                "serverMsgID": "",
                "createTime": send_time,
                "sendTime": send_time,
                "sessionType": 0,
                "sendID": f"{self.mind_im_userid}",
                "recvID": f"{recvID}",
                "msgFrom": 100,
                "contentType": 140,
                "platformID": 3,
                "senderNickname": f"{self.nickname}",
                "senderFaceUrl": f"{self.faceURL}",
                "groupID": f"{groupID}",
                "content": f"{json.dumps(message_json)}",
                "seq": 0,
                "isRead": False,
                "status": 1,
                "offlinePush": {
                    "title": "",
                    "desc": "",
                    "ex": "",
                    "iOSPushSound": "",
                    "iOSBadgeCount": False
                },
                "attachedInfo": "",
                "ex": "",
                "ext": False,
                "pictureElem": {
                    "sourcePicture": {
                        "uuid": "",
                        "type": "",
                        "size": 0,
                        "width": 0,
                        "height": 0,
                        "url": ""
                    },
                    "bigPicture": {
                        "uuid": "",
                        "type": "",
                        "size": 0,
                        "width": 0,
                        "height": 0,
                        "url": ""
                    },
                    "snapshotPicture": {
                        "uuid": "",
                        "type": "",
                        "size": 0,
                        "width": 0,
                        "height": 0,
                        "url": ""
                    }
                },
                "soundElem": {
                    "dataSize": 0,
                    "duration": 0
                },
                "videoElem": {
                    "videoSize": 0,
                    "duration": 0,
                    "snapshotSize": 0,
                    "snapshotWidth": 0,
                    "snapshotHeight": 0
                },
                "fileElem": {
                    "fileSize": 0
                },
                "mergeElem": {

                },
                "atElem": {
                    "text": "",
                    "atUserList": [

                    ],
                    "isAtSelf": False,
                    "textReal": "",
                    "atUsersInfo": [

                    ]
                },
                "locationElem": {
                    "longitude": 0,
                    "latitude": 0
                },
                "customElem": {
                    "data": "",
                    "description": "",
                    "extension": ""
                },
                "quoteElem": {
                    "text": "",
                    "textReal": ""
                },
                "notificationElem": {

                },
                "attachedInfoElem": {
                    "groupHasReadInfo": {
                        "hasReadUserIDList": [

                        ],
                        "hasReadCount": 0,
                        "groupMemberCount": 0
                    },
                    "isPrivateChat": False,
                    "hasReadTime": 0,
                    "notSenderNotificationPush": False,
                    "isEncryption": False,
                    "inEncryptStatus": False,
                    "isSilent": False
                },
                "senderSignature": "这是我的个性签名www.baidu.com"
            }
            return message

        def get_message():
            text_content = str(time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime())) + " 我会是你这一生最爱的那个，可现在呢，空房间里飘荡着浓烈的酒精味，一个人的孤单"

            text_message = text(text_content)

            if message_type == MESSAGE_TYPES.TEXT:
                default_messages = text_message
            elif message_type == MESSAGE_TYPES.BI:
                pass
            return default_messages

        message = get_message()

        # 跳过大群
        if groupID == '1204918865' or groupID == '1523490576' or groupID == '417454658' or groupID == '2802601985' \
                or groupID == '4247814843' or groupID == 'c5775d24e4f33ae29024323aa7822cf9':
            return
        # 测试

        # 预发
        if groupID == '367694aea403361e2cd42377fd2bcd29' or groupID == '3083466545' or groupID == '1926813162' or groupID == '3446554249':
            return

        data_json = {
            "recvID": recvID,
            "groupID": groupID,
            "offlinePushInfo": json.dumps(
                {"title": "你收到一条新消息", "desc": "", "ex": "", "iOSPushSound": "+1", "iOSBadgeCount": True}),
            "message": json.dumps(message_body(message_json=message)),
            'isResend': False
        }
        send_data = {
            "reqFuncName": "SendMessage",
            "operationID": utils.getRandom(23),
            "userID": self.mind_im_userid,
            "data": json.dumps(data_json)
        }

        self.ws.send(json.dumps(send_data))

    def on_open(self, ws):
        # 向服务器发送连接信息

        userId = self.mind_im_userid
        token = self.mind_im_token
        user_data = json.dumps({
            "userID": userId,
            "token": token,
            "batchMsg": 1,
            "notCheck": False
        })
        data = {
            "reqFuncName": "Login",
            "operationID": utils.getRandom(32),
            "userID": userId,
            "data": user_data,
            "batchMsg": 1
        }
        ws.send(json.dumps(data))

    def on_message(self, ws, message):
        # 输出服务器推送过来的内容
        res = json.loads(message)
        event = res.get("event")
        code = res.get("errCode")

        if event == "SendMessage" and code == 0:
            logger.info('==============================消息发送成功')
        if event == "SendMessage" and code != 0:
            logger.error('======================消息发送失败', str(res))
        elif event == "OnRecvNewMessages" and code == 0:
            print('==============================收到新消息')
            data = res.get('data')
            self.markGroupMessageAsRead(data)  # 将本话题所有消息置为已读

        elif event == "GetJoinedGroupList" and code == 0:
            print('==============================获取群组信息')
            # 把所有人对应的话题列表存起来
            data = res.get('data')
            for group in json.loads(data):
                if group['status'] == 0 and group['dismissTime'] == 0:
                    self.groups.append(group['groupID'])

            while True:
                time.sleep(1)
                self.send()
            self.getTotalUnreadMsgCount(ws)

        elif event == "Login" and code == 0:
            print('==============================登录成功')
            self.get_user_info(ws)

        elif event == "GetSelfUserInfo" and code == 0:
            print('==============================获取到用户信息')
            data = res.get('data')
            self.nickname = json.loads(data)['nickname']
            self.faceURL = json.loads(data)['faceURL']
            self.getJoinedGroupList(ws)

            pass

    def on_pong(self, ws, data):
        userId = self.mind_im_userid
        data = {
            "reqFuncName": "OnPongPong",
            "operationID": utils.getRandom(22),
            "userID": userId,
            "data": ""
        }
        ws.send(json.dumps(data))

    def handleConversationList(self, ws, conversationList):
        userId = self.mind_im_userid
        userConversationDic = {
            userId: []
        }
        for conversation in conversationList:
            showName = conversation.get("showName")
            conversationID = conversation.get("conversationID")
            groupID = conversation.get("groupID")
            userConversationDic.userId.append({showName: {conversationID: groupID}})

    def getJoinedGroupList(self, ws):
        """
        获取用户加入的话题list
        """
        userId = self.mind_im_userid
        group_operationID = utils.getRandom(22)
        data = {
            "reqFuncName": "GetJoinedGroupList",
            "operationID": group_operationID,
            "userID": userId,
            "data": ""
        }
        ws.send(json.dumps(data))

    def getTotalUnreadMsgCount(self, ws):
        """
        获取未读消息总数
        """
        userId = self.mind_im_userid
        data = {
            "reqFuncName": "GetTotalUnreadMsgCount",
            "operationID": utils.getRandom(22),
            "userID": userId,
            "data": ""
        }
        ws.send(json.dumps(data))

    def markGroupMessageAsRead(self, ws, data):
        userId = self.mind_im_userid

        msg_dict = {}
        for msg in json.loads(data):
            groupID = msg.get('groupID')
            msgID = msg.get('clientMsgID')

            if msg_dict.get(groupID):
                msg_dict.get(groupID).append(msgID)
            else:
                msg_dict['groupID'] = [msgID, ]

        for groupID, msgIDList in msg_dict:
            data = {
                "reqFuncName": "MarkGroupMessageAsRead",
                "operationID": utils.getRandom(22),
                "userID": userId,
                "data": json.dumps({"groupID": groupID, "msgIDList": msgIDList})
            }

        ws.send(json.dumps(data))

    def get_user_info(self, ws):
        '''
        获取用户信息
        '''
        userId = self.mind_im_userid
        data = {
            "data": "",
            "operationID": utils.getRandom(22),
            "reqFuncName": "GetSelfUserInfo",
            "userID": userId
        }
        ws.send(json.dumps(data))


def send_request(method, url, data, cookie=None, header=None):
    if method == "get":
        res = requests.get(url=url, params=data, headers=header, cookies=cookie, verify=False)
    else:
        res = requests.post(url=url, json=data, headers=header, cookies=cookie, verify=False)
    return res


class Performance:
    def __init__(self, env):
        self.env = env
        self.server_pids = []
        self.user_pids = []

    def open_servers(self, ports):
        imServer = IMServer(self.env)
        imServer.build_servers(ports)
        self.server_pids = imServer.pids

    def process_run(self, senders, ports, **kwargs):
        # 开启sdk服务
        logger.info('准备开启服务')
        self.open_servers(ports)
        logger.info('开启服务成功')

        process_list = []
        for phone in senders:
            logger.info('开启进程', str(phone))
            port = ports[random.randrange(0, len(ports), 1)]
            kwargs['port'] = port
            kwargs['phone'] = int(phone)
            my_process = Process(target=self.im_run, kwargs=kwargs)
            process_list.append(my_process)
            my_process.daemon

        for process in process_list:
            process.start()
            logger.info('开启进程成功', process.pid)
        for process in process_list:
            process.join()
            self.user_pids.append(str(process.pid))

        return {'server_pids': self.server_pids,
                'user_pids': self.user_pids}

    def im_run(self, **kwargs):
        phone = kwargs.pop('phone')
        user = User(self.env, phone_number=phone)
        user.login()
        user.start(kwargs['receivers'], kwargs['groups'], kwargs['message_types'], kwargs['port'])


if __name__ == "__main__":
    performance = Performance('test')
    performance.process_run(senders=[18500000001, 18500000002], ports=[30001], receivers=[],
                            groups=[],
                            message_types=[MESSAGE_TYPES.TEXT, ],
                            )
