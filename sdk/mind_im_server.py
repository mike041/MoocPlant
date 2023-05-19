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


def get_process_id(name):
    child = subprocess.Popen(["pgrep", "-f", name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


class IMServer:
    sys_name = os.name
    if sys_name == 'posix':
        sdk = 'open_im_sdk_electron'
    elif sys_name == 'nt':
        sdk = 'mind_ws_server_win.exe'
    exe_path = os.path.join(rootPath, sdk)
    db_path = os.path.join(rootPath, 'db')

    def __init__(self, env):
        self._env = env
        self.servers = {}
        self.pids = []
        pass

    def build_servers(self, ports):
        self.quit()
        for port in ports:
            self.build_server(port)
        pass

    def build_server(self, port):
        if self.servers.get(port):
            return
        # 停止之前的所有服务
        if self._env == 'test':
            imApiAddress = "http://10.2.4.100:10000"
            imWsAddress = "ws://10.2.4.100:17778"
        else:
            imApiAddress = "https://premind.im30.net/im/api"
            imWsAddress = "wss://premind.im30.net/ws/mobile"
        _cmd = f'{IMServer.exe_path} -openIMApiAddress {imApiAddress} -openIMWsAddress {imWsAddress} -sdkWsPort {port} -openIMDbDir {IMServer.db_path}'
        server = subprocess.Popen(_cmd)
        self.pids.append(str(server.pid))
        self.servers[port] = server
        pass

    def close(self, port):
        server: subprocess.Popen = self.servers.get(port)
        if server:
            server.kill()
            self.servers.pop(port)
        pass

    def quit(self):
        pids = None
        if os.name == 'nt':
            os.system('taskkill /f /im %s' % f'{IMServer.sdk}')
        else:
            pids = get_process_id(IMServer.sdk)
        if not pids:
            print("no target pid to kill,please check")
            # sys.exit(1)
        else:
            for pid in pids:
                print(pid)
                result = os.system("kill -9 " + str(pid))
                if result == 0:
                    print(f'{pid} kill success')

        for server in self.servers.values():
            server.kill()
        self.servers = {}


if __name__ == '__main__':
    pass
