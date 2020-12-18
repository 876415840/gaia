#! _*_ encoding=utf-8 _*_


import struct
import socket


# IP报文解析器
class IPParser:

    # IP协议前20个字节为头部(不包含 选项options)
    IP_HEADER_LENGTH = 20

    @classmethod
    def parse_ip_header(cls, ip_header):
        """
        IP 报文格式
        1. 4位版本 4位首部长度 8位服务类型(TOS) 16位总长度(字节)
        2. 16位标识 3位标志 13位片偏移
        3. 8位TTL 8位协议 16位首部校验和
        4. 32位源IP地址
        5. 32位目的IP地址
        :param ip_header:
        :return:
        """
        # 第一行 前4个字节，按1:1:2格式化；分别是 版本+首部长度、服务类型、总长度
        line1 = struct.unpack('>BBH', ip_header[:4])
        # 4位版本(高4位)，右移4位 eg：11110000 -> 00001111
        ip_version = line1[0] >> 4
        # 4位首部长度(低4位)，和15与运算，单位是32位4字节乘4转换成字节 eg：11111111 & 00001111 -> 00001111
        iph_length = line1[0] & 15 * 4
        # 包总长度
        packet_length = line1[2]

        # 第三行 第9~12字节，按1:1:2格式化；分别是 TTL、协议、首部校验和
        line3 = struct.unpack('>BBH', ip_header[8:12])
        TTL = line3[0]
        # 协议
        protocol = line3[1]
        # 首部校验和
        iph_checksum = line3[2]

        # 第四行 第13~16字节，源IP地址，格式化字节串
        line4 = struct.unpack('4s', ip_header[12:16])
        src_ip = socket.inet_ntoa(line4[0])

        # 第五行 第17~20字节，目的IP地址，格式化字节串
        line5 = struct.unpack('4s', ip_header[16:20])
        dst_ip = socket.inet_ntoa(line5[0])
        return {
            'ip_version': ip_version,
            # 头部长度
            'iph_length': iph_length,
            # 包长度
            'packet_length': packet_length,
            'TTL': TTL,
            # IP报文具体协议，TCP、UDP
            'protocol': protocol,
            # 校验和
            'iph_checksum': iph_checksum,
            # 源地址
            'src_ip': src_ip,
            # 目的地址
            'dst_ip': dst_ip
        }

    @classmethod
    def parse(cls, packet):
        ip_header = packet[:20]
        return cls.parse_ip_header(ip_header)
