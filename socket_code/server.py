#! _*_ encoding=utf-8 _*_


import socket


def server():
    # 创建socket
    s = socket.socket()
    host = "127.0.0.1"
    port = 9999
    # 绑定套接字
    s.bind((host, port))

    # 监听
    s.listen(5)

    while True:
        c, addr = s.accept()
        print('Connect Addr: ', addr)
        c.send(b'Welcome to my course.')
        c.close()


if __name__ == '__main__':
    server()
