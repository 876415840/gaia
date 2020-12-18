#! _*_ encoding=utf-8 _*_


import uuid


# 基本任务对象
class Task:

    def __init__(self, func, *args, **kwargs):
        # 任务的具体逻辑，通过函数引用传递进来
        self.callable = func
        self.id = uuid.uuid4()
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'Task id: ' + str(self.id)


def my_function():
    print('this is a task test function.')


if __name__ == '__main__':
    task = Task(func=my_function)
    print(task)
