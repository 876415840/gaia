#! _*_ encoding=utf-8 _*_

import psutil

from operate_system.queue import ThreadSafeQueue
from operate_system.thread import ProcessThread
from operate_system.task import Task


# 线程池
class ThreadPool:

    def __init__(self, size=0):
        if not size:
            # 约定线程池大小为cpu核数的2倍(最佳实践)
            size = psutil.cpu_count() * 2
        # 线程池
        self.pool = ThreadSafeQueue(size)
        # 任务队列
        self.task_queue = ThreadSafeQueue()

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    # 启动线程池
    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程池
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        # 清空线程池
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()

    # 向线程池添加任务
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)

    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    def size(self):
        return self.pool.size()


class TaskTypeErrorException(Exception):
    pass
