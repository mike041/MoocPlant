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

import gevent

from Imoocmapi import utils
from Imoocmapi.utils import randomkey
from sdk.mind_im_server import IMServer

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
import json

requests.packages.urllib3.disable_warnings()

group_dict = {}


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
        self.phone = phone_number

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

        if self.env == 'pre':
            json_data: dict = utils.parse_json_file(os.path.join(rootPath, 'userdata', 'user_cookie.json'))
        elif self.env == 'test':
            print('当前是测试环境')
            json_data: dict = utils.parse_json_file(os.path.join(rootPath, 'userdata', 'test_user_cookie.json'))

        if json_data.get(str(self.phone)):
            print('================有缓存不用登录')
            user_json = json_data.get(str(self.phone))
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

    def start(self, mode=2, user_id='', group_id='', message_types=[1, ], port=30001, times=1):

        # 新建ws
        self.ws = websocket.WebSocketApp(
            # url=self.BASE_WS + "/?sendID={}&token={}&platformID=3".format(self.mind_im_userid, self.mind_im_token),
            url=f"ws://127.0.0.1:{int(port)}/?sendID={self.mind_im_userid}&token={self.mind_im_token}&platformID=3",
            on_message=self.on_message,
            on_pong=self.on_pong,
            cookie=json.dumps(self.im_cookie)
        )
        self.ws.on_open = self.on_open

        # 把手机号转换为im_user_id
        if len(str(user_id)) == 11:
            if self.env == 'pre':
                json_data: dict = utils.parse_json_file(os.path.join(rootPath, 'userdata', 'user_cookie.json'))
            elif self.env == 'test':
                print('当前是测试环境')
                json_data: dict = utils.parse_json_file(os.path.join(rootPath, 'userdata', 'test_user_cookie.json'))
            if json_data.get(str(self.phone)):
                user_json = json_data.get(str(user_id))
                user_id = user_json.get('im_cookie').get('MINDIMUSERID')
            else:
                user_id = ''

        self.im = {
            'mode': mode,
            'user_id': user_id,
            'group_id': group_id,
            'message_types': message_types,
            'times': times,

        }

        self.ws.run_forever()

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

        def message_body(groupID='', message_json={}):
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

        if self.im.get('mode') == 1:
            recvID = ''
            groupID = utils.randomkey(self.groups)
        else:
            recvID = self.im.get('user_id')
            groupID = self.im.get('group_id')
        # todo 消息类型还没写完

        all_messages = [text('这是文本消息'), text('这是bi消息'), text('这是机器人消息')]
        # 随机获取想发送的消息类型
        messages = [all_messages[i - 1] for i in self.im.get('message_types')]
        # message = utils.randomkey(messages)
        message = text(time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime()) + '若发起人为自己，则所有状态的审批单都可发起再次提交，并且将原单的值赋到最新版本的审批单中；否则不会显示【再次提交】的按钮（1）若新版本审批单的控件发生变化，则仅将与原单相同控件的值自动带入即可举例：原审批单表单控件为A B C，新版本表单控件为A D，则再次提交时，仅将A值带入新版本审批单即可（2）若该审批单被停用，则再次提交时，仅toast提示“该审批类型已停用，暂不支持再次提交”即可（3）若该审批单被删除，则再次提交时，仅taost提示“该审批类型已删除，不支持再次提交”即可PC端效果（审批中心与IM)侧边栏相同')

        data_json = {
            "recvID": recvID,
            "groupID": groupID,
            "offlinePushInfo": json.dumps(
                {"title": "你收到一条新消息", "desc": "", "ex": "", "iOSPushSound": "+1", "iOSBadgeCount": True}),
            "message": json.dumps(message_body(groupID=groupID, message_json=message)),
            'isResend': False
        }
        send_data = {
            "reqFuncName": "SendMessage",
            "operationID": utils.getRandom(23),
            "userID": self.mind_im_userid,
            "data": json.dumps(data_json)
        }

        ws.send(json.dumps(send_data))

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
            print('==============================消息发送成功')
        if event == "SendMessage" and code != 0:
            print(res)
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
            print('======groups', self.groups)
            for i in range(self.im.get('times')):
                self.im_send(ws)
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


'''
websockt相关方法
'''


def process_run(func, phone_list):
    process_list = []
    for phone in phone_list:
        my_process = Process(target=func, args=(phone,))
        process_list.append(my_process)
        my_process.daemon
        my_process.start()
    for process in process_list:
        print('=======进程pid', process.pid)
        process.join()


def im_run(phone):
    user = User('pre', phone_number=phone)
    user.login()
    # user.start(group_id='489320452')
    user.start(mode=2, user_id='15902379217', times=5)


if __name__ == "__main__":
    # python case/meeting.py 50  1
    # 50 代表并发人数，最大100，  1代表执行方式，1纯文字聊天、2增加会议人数  3 文字聊天加增加人数，3还没写。
    '''
    纯聊天发文字
    '''
    server = IMServer('pre')
    server.build_server('30001')
    process_run(im_run, [18500000002, 18899530117])
