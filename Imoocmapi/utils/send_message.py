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

from Imoocmapi import utils

'''
@File    :   meeting.py
@Time    :   2022/12/04 16:26:15
@Author  :   Mushishi 
'''
import sys
import os

rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(rootPath)

import requests
import websocket
import random
import json

requests.packages.urllib3.disable_warnings()

group_dict = {}


class User:

    def __init__(self, env='test', phone_number=None):
        if env == 'test':

            self.BASE_URL = 'http://mind.im30.lan'
            self.BASE_WS = 'ws://10.2.4.100:30000'
        else:
            self.BASE_URL = 'https://premind.im30.net'
            self.BASE_WS = 'wss://premind.im30.net/ws/web'

        self.groups = []
        self.phone = phone_number

        self.cookie = {}
        self.base_user_id_or_mind_user_id = None
        self.token_or_mind_token = None
        self.home_mind_token = None
        self.mind_teamid = None
        self.session_id = None
        self.mind_im_token = None
        self.mind_im_userid = None
        self.meeting_id = None
        self.sendID = self.mind_im_userid
        self.device_id = utils.getRandom(32)
        self.im_cookie = {}
        self.header = {
            "device-id": self.device_id,
            "accept": "application/json, text/plain",
            "authority": "premind.im30.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows"
        }

        self.ws = websocket.WebSocketApp(
            url=self.BASE_WS + "/?sendID={}&token={}&platformID=5".format(self.mind_im_userid, self.mind_im_token),
            on_message=self.on_message,
            on_pong=self.on_pong,
            cookie=json.dumps(self.im_cookie)
        )
        self.ws.on_open = self.on_open

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

        # 登录步骤 1、获取验证码 2、mind登录 3、im登录
        get_verify_code()
        mind_login()
        im_login()

    def start(self, mode=2, user_id='', group_id='', message_types=[1, ]):

        self.im = {
            'mode': mode,
            'user_id': user_id,
            'group_id': group_id,
            'message_types': message_types,
        }

        self.ws.run_forever(ping_interval=10, ping_timeout=5)

    def im_send(self, ws):

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

        def message_body(sendID='', senderNickname='', groupID='', message_json={}):
            send_time = int(time.time())
            message = {
                "clientMsgID": f"{utils.getRandom(16)}",
                "serverMsgID": "",
                "createTime": send_time,
                "sendTime": send_time,
                "sessionType": 0,
                "sendID": f"{sendID}",
                "recvID": "",
                "msgFrom": 100,
                "contentType": 140,
                "platformID": 5,
                "senderNickname": f"{senderNickname}",
                "senderFaceUrl": "https://cdn-file-mind.im30.net/image_picker1883742117465822451.jpg",
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

        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")

        if self.im.get('mode') == 1:
            recvID = ''
            groupID = utils.randomkey(self.groups)
        else:
            recvID = self.im.get('user_id')
            groupID = self.im.get('group_id')
        # todo 消息类型还没写完
        all_messages = [text('这是文本消息'), text('这是bi消息'), text('这是机器人消息')]
        # 随机获取想发送的消息类型
        messages = [all_messages[i] for i in self.im.get('message_types')]
        message = utils.randomkey(messages)

        message_json = message_body(sendID=recvID, groupID=groupID, message_json=message)

        data_json = {
            "recvID": recvID,
            "groupID": groupID,
            "offlinePushInfo": "{\"title\":\"你收到一条新消息\",\"desc\":\"\",\"ex\":\"\",\"iOSPushSound\":\"+1\",\"iOSBadgeCount\":true}",
            "message": json.dumps(message_json)
        }
        send_data = {
            "reqFuncName": "SendMessage",
            "operationID": utils.getRandom(23),
            "userID": userId,
            "data": json.dumps(data_json)
        }

        ws.send(json.dumps(send_data))

    def on_open(self, ws):
        # 向服务器发送连接信息
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
        token = cookie.get("MINDIMTOKEN")
        user_data = json.dumps({
            "userID": userId,
            "token": token
        })
        data = {
            "reqFuncName": "Login",
            "operationID": utils.getRandom(32),
            "userID": userId,
            "data": user_data
        }
        ws.send(json.dumps(data))

    def on_message(self, ws, message):
        # 输出服务器推送过来的内容
        res = json.loads(message)
        event = res.get("event")
        code = res.get("errCode")
        print(res)
        if event == "Login" and code == 0:
            print('==============================登录')
            self.get_user_info(ws)
            self.getJoinedGroupList(ws)
            self.getTotalUnreadMsgCount(ws)

        if event == "GetSelfUserInfo" and code == 0:
            # create_message(ws)
            print('==============================获取用户信息')
            pass

        # if event == "SendMessage" and code == 0:
        #     print('消息发送成功')
        if event == "OnRecvNewMessages" and code == 0:
            data = res.get('data')
            self.im_send(ws)
            self.markGroupMessageAsRead(data)  # 将本话题所有消息置为已读

        if event == "GetJoinedGroupList" and code == 0:
            print('==============================获取群组信息')
            cookie = json.loads(ws.cookie)
            userId = cookie.get("MINDIMUSERID")
            # 把所有人对应的话题列表存起来
            data = res.get('data')
            for group in json.loads(data):
                if group['status'] == 0 and group['dismissTime'] == 0:
                    self.groups.append(group['groupID'])
            self.im_send(ws)

    def on_pong(self, ws, data):
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
        data = {
            "reqFuncName": "OnPongPong",
            "operationID": utils.getRandom(22),
            "userID": userId,
            "data": ""
        }
        ws.send(json.dumps(data))

    def handleConversationList(self, ws, conversationList):
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
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
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
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
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
        data = {
            "reqFuncName": "GetTotalUnreadMsgCount",
            "operationID": utils.getRandom(22),
            "userID": userId,
            "data": ""
        }
        ws.send(json.dumps(data))

    def markGroupMessageAsRead(self, ws, data):
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")

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
        cookie = json.loads(ws.cookie)
        userId = cookie.get("MINDIMUSERID")
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


'''
websockt相关方法
'''

if __name__ == "__main__":
    # python case/meeting.py 50  1
    # 50 代表并发人数，最大100，  1代表执行方式，1纯文字聊天、2增加会议人数  3 文字聊天加增加人数，3还没写。
    '''
    纯聊天发文字
    '''
    # gevent_run(im_run)

    user = User(phone_number=15902379218)
    user.login()
    # user.send_message()
    print(user)
