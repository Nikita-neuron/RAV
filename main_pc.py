import sys
import multiprocessing
from multiprocessing import Process
import threading
import queue
import io
import time
import logging
# from log_system import LogSystem, Logger

# import web.server

# web.server.run()

# args: out, log



    # sys.stdout = stdout
    # print('WEB', file=open(fileno, 'w'))
    # import web.server
    # web.server.run()



def webserver():
    print('WEBSERVER')

def loh():
    print(print)
    raise 1
    print('vALENTIN-LOH')

class Task(Process):
    def __init__(self, target):
        super().__init__(
            target=target,
            name=target.__name__,
        )
        self.logger = multiprocessing.log_to_stderr(logging.INFO)
        self.logger.handlers[0].level = logging.INFO

        
        raise 1
    @staticmethod
    def _custom_print(*args, **kwargs):
        kwargs.setdefault('flush', True)
        __builtins__['print'](*args, **kwargs)
    def run(self):
        sys.stdout = self.logger
        globals()['print'] = self._custom_print
        try:
            super().run()
        except Exception as e:
            print('TASK CRASH', e)

class TaskManager:
    def __init__(self, tasks_functions):
        self.tasks_functions = tasks_functions
        self.tasks = {}
        for fun in tasks_functions:
            name = fun.__name__
            # process = Process(
            #     target=fun,
            #     name=f'{name}_task',
            #     args=(None, self.logger.create_writer(name),)
            # )
            self.tasks[name] = Task(fun)
    def serve(self):
        for _, task in self.tasks.items():
            task.start()
        for _, task in self.tasks.items():
            task.join()
        self.log_system.stop()

if __name__ == '__main__':
    manager = TaskManager([webserver, loh])
    manager.serve()
