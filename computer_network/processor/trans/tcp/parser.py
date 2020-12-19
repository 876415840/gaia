#! _*_ encoding=utf-8 _*_


import struct


class TCPParser:
    # IP协议前20个字节为头部(不包含 选项options)
    IP_HEADER_LENGTH = 20
    TCP_HEADER_LENGTH = 20

    @classmethod
    def parse_tcp_header(cls, tcp_header):
        """
        TCP协议 头部结构
        1. 16位源端口号 16位目的端口号
        2. 32位序号
        3. 32位确认号
        4. 4位数据偏移 6位保留字段 6位TCP标记 16位窗口大小
        5. 16位校验和 16位紧急指针
        """
        # 前4个字节，按2:2格式化；分别是：源端口号、目的端口号
        line1 = struct.unpack('>HH', tcp_header[:4])
        src_port = line1[0]
        dst_port = line1[1]

        # 第5~8字节，序号，格式化4字节大小的整数
        line2 = struct.unpack('>L', tcp_header[4:8])
        seq_num = line2[0]

        # 第9~12字节，确认号，格式化4字节大小的整数
        line3 = struct.unpack('>L', tcp_header[8:12])
        ack_num = line3[0]

        # 第13~16字节，按1:1:2格式化；分别是：(数据偏移、保留字段、TCP标记)、窗口大小
        line4 = struct.unpack('>BBH', tcp_header[12:16])
        data_offset = line4[0] >> 4
        flags = line4[1] & int('00111111', 2)
        URG = flags >> 5
        ACK = (flags >> 4) & 1
        PSH = (flags >> 3) & 1
        RST = (flags >> 2) & 1
        SYN = (flags >> 1) & 1
        FIN = flags & 1
        win_size = line4[2]

        # 第17~20字节，按2:2格式化；分别是：校验和、紧急指针
        line5 = struct.unpack('>HH', tcp_header[16:20])
        tcp_checksum = line5[0]
        urg_port = line5[1]
        return {
            'src_port': src_port,
            'dst_port': dst_port,
            'seq_num': seq_num,
            'ack_num': ack_num,
            'data_offset': data_offset,
            'flag': {
                'URG': URG,
                'ACK': ACK,
                'PSH': PSH,
                'RST': RST,
                'SYN': SYN,
                'FIN': FIN
            },
            'win_size': win_size,
            'tcp_checksum': tcp_checksum,
            'urg_port': urg_port
        }

    @classmethod
    def parse(cls, packet):
        # TCP协议头部为20个字节，需要先偏移IP协议头部长度
        tcp_header = packet[cls.IP_HEADER_LENGTH: cls.IP_HEADER_LENGTH + cls.TCP_HEADER_LENGTH]
        return cls.parse_tcp_header(tcp_header)
