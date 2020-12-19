#! _*_ encoding=utf-8 _*_


import json
import socket

from operate_system.pool import ThreadPool as tp
from operate_system.asyncTask import AsyncTask
from computer_network.processor.net.parser import IPParser
from computer_network.processor.trans.udp.parser import UDPParser
from computer_network.processor.trans.tcp.parser import TCPParser


class ProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super(ProcessTask, self).__init__(func=self.process, *args, **kwargs)

    def process(self):
        headers = {
            # 网络层头部
            'network_header': None,
            # 传输层头部
            'transport_header': None
        }
        ip_header = IPParser.parse(self.packet)
        headers['network_header'] = ip_header
        # 传输层使用UDP协议
        if ip_header['protocol'] == 17:
            udp_header = UDPParser.parse(self.packet)
            headers['transport_header'] = udp_header
        # 传输层使用TCP协议
        elif ip_header['protocol'] == 6:
            tcp_header = TCPParser.parse(self.packet)
            headers['transport_header'] = tcp_header
        return headers


# 网络嗅探工具
class Server:

    def __init__(self):
        # 工作协议类型 AF_INET：IPv4、套接字类型：原始套接字、工作具体的协议：IP协议
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        # 自己主机IP和端口
        self.ip = '192.168.1.5'
        self.port = 9999
        self.sock.bind((self.ip, self.port))

        # windows设置网卡为混杂模式
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        self.pool = tp(10)
        self.pool.start()

    def loop_server(self):
        while True:
            # 1.接收
            packet, addr = self.sock.recvfrom(65535)
            # 2.生产task
            task = ProcessTask(packet)
            # 3.提交task
            self.pool.put(task)
            # 4.获取task结果
            result = task.get_result()
            result = json.dumps(
                result,
                indent=4
            )
            print(result)


if __name__ == '__main__':
    server = Server()
    server.loop_server()
