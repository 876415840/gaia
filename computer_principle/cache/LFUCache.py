#! _*_ encoding=utf-8 _*_

from computer_principle.DoubleLinkedList import DoubleLinkedList, Node


class LFUNode(Node):
    def __init__(self, key, value):
        self.freq = 0
        super(LFUNode, self).__init__(key, value)

    def add_freq(self):
        self.freq += 1
        return self.freq



# 最不经常使用算法 -- 淘汰缓存时，吧使用频率最小的淘汰
class LFUCache(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        # key: 使用频率，value: 频率对应的FIFO双向链表(每个节点使用频率都是当前key,按照FIFO存放)
        self.frep_map = {}
        self.size = 0

    # 更新节点频率
    def __update_freq(self, node):
        freq = node.freq

        # 删除
        node = self.frep_map[freq].remove(node)
        if self.frep_map[freq].size == 0:
            del self.frep_map[freq]

        # 更新
        freq = node.add_freq()
        if freq not in self.frep_map:
            self.frep_map[freq] = DoubleLinkedList()
        self.frep_map[freq].append(node)

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map.get(key)
        self.__update_freq(node)
        return node.value

    def put(self, key, value):
        if self.capacity == 0:
            return

        # 缓存命中
        if key in self.map:
            node = self.map.get(key)
            node.value = value
            self.__update_freq(node)
            return node

        # 缓存没有命中

        if self.capacity == self.size:
            min_freq = min(self.frep_map)
            node = self.frep_map[min_freq].pop()
            del self.map[node.key]
            self.size -= 1
        node = LFUNode(key, value)
        node.freq = 1
        self.map[key] = node
        if node.freq not in self.frep_map:
            self.frep_map[1] = DoubleLinkedList()
        self.frep_map[1].append(node)
        self.size += 1

    def print(self):
        print('*****************************')
        for k, v in self.frep_map.items():
            print('Freq = %d' % k)
            self.frep_map[k].print()
        print('*****************************')
        print()

if __name__ == '__main__':
    cache = LFUCache(2)
    cache.put(1, 1)
    cache.print()
    cache.put(2, 2)
    cache.print()
    print(cache.get(1))
    cache.print()
    cache.put(3, 3)
    cache.print()
    print(cache.get(2))
    cache.print()
    print(cache.get(3))
    cache.print()
    cache.put(4, 4)
    cache.print()
    print(cache.get(1))
    cache.print()
    print(cache.get(3))
    cache.print()
    print(cache.get(4))
    cache.print()

