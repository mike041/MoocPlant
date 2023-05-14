"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: mind_im_server
@Site:
@time: 2023.01.09
"""
import os
import subprocess
import sys
import threading

rootPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(rootPath)


class IMServer:
    exe_path = os.path.join(rootPath, 'mind_ws_server_win.exe')
    db_path = os.path.join(rootPath, 'db')

    def __init__(self, env):
        self._env = env
        self.servers = {}
        pass

    def build_servers(self, ports):
        for port in ports:
            self.build_server(port)
        pass

    def build_server(self, port):
        if self.servers.get(port):
            return
        if self._env == 'test':
            imApiAddress = "http://10.2.4.100:10000"
            imWsAddress = "ws://10.2.4.100:17778"
        else:
            imApiAddress = "https://premind.im30.net/im/api"
            imWsAddress = "wss://premind.im30.net/ws/mobile"
        _cmd = f'{IMServer.exe_path} -openIMApiAddress {imApiAddress} -openIMWsAddress {imWsAddress} -sdkWsPort {port} -openIMDbDir {IMServer.db_path}'
        server = subprocess.Popen(_cmd)

        self.servers[port] = server
        pass

    def close(self, port):
        server: subprocess.Popen = self.servers.get(port)
        if server:
            server.kill()
            self.servers.pop(port)
        pass

    def quit(self):
        for server in self.servers.values():
            server.kill()
        self.servers = {}


if __name__ == '__main__':
    server = IMServer('pre')
    server.build_server('30001')
    server.quit()
