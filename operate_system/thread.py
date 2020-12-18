#! _*_ encoding=utf-8 _*_

import threading

from operate_system.task import Task
from operate_system.asyncTask import AsyncTask


# 任务处理线程
class ProcessThread(threading.Thread):

    def __init__(self, task_queue, *args, **kwargs):
        # 父类构造
        threading.Thread.__init__(self, *args, **kwargs)
        # 线程停止的标记
        self.dismiss_flag = threading.Event()
        # 任务队列(处理线程不断从队列取出元素处理)
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            # 执行task实际逻辑(是通过函数调用引进来的)
            result = task.callable(*task.args, **task.kwargs)

            # 异步任务
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()

