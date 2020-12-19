#! _*_ encoding=utf-8 _*_


import struct


class UDPParser:
    # IP协议前20个字节为头部(不包含 选项options)
    IP_HEADER_LENGTH = 20
    UDP_HEADER_LENGTH = 8

    @classmethod
    def parse_udp_header(cls, udp_header):
        """
        UDP协议 头部结构
        1. 16位源端口号 16位目的端口号
        2. 16位UDP长度 16位UDP校验和
        """
        # 前8个字节，按2:2:2:2格式化；分别是：源端口号、目的端口号、UDP长度、UDP校验和
        udp_header = struct.unpack('>HHHH', udp_header[:8])
        return {
            'src_port': udp_header[0],
            'dst_port': udp_header[1],
            'udp_length': udp_header[2],
            'udp_checksum': udp_header[3]
        }

    @classmethod
    def parse(cls, packet):
        # UDP协议头部为8个字节，需要先偏移IP协议头部长度
        udp_header = packet[cls.IP_HEADER_LENGTH: cls.IP_HEADER_LENGTH + cls.UDP_HEADER_LENGTH]
        return cls.parse_udp_header(udp_header)
