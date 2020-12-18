#! _*_ encoding=utf-8 _*_


import struct

# 八个字节
bin_str = b'ABCD1234'
print(bin_str)
# '>'是大端字节序
result = struct.unpack('>BBBBBBBB', bin_str)
print(result)

# H:2个字节转换一个整数，所以4个H转换8个字节
result = struct.unpack('>HHHH', bin_str)
# 打印的值分别是 A、B   C、D   1、2   3、4
print(result)

# L:4个字节转换一个整数，所以2个L转换8个字节
result = struct.unpack('>LL', bin_str)
print(result)

# s:字符，指定个数
result = struct.unpack('>8s', bin_str)
print(result)

# 混合使用
result = struct.unpack('>BBHL', bin_str)
print(result)
