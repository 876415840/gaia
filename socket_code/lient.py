#! _*_ encoding=utf-8 _*_


import socket

def client(i):
    # 创建套接字
    s = socket.socket()
    # 连接服务端套接字
    s.connect(('127.0.0.1', 9999))

    print('Recv msg: %s, Client: %d' % (s.recv(1024), i))
    s.close()


if __name__ == '__main__':
    for i in range(10):
        client(i)
