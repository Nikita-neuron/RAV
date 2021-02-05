import sys
import multiprocessing
from multiprocessing import Process
import threading
import queue
import io

from log_system import LogSystem, Logger

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
    print('LOH')

class Task(Process):
    def __init__(self, target, log_system):
        super().__init__(
            target=target,
            name=target.__name__,
        )
        self.logger = log_system.create_logger(self.name)
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
        self.log_system = LogSystem()
        for fun in tasks_functions:
            name = fun.__name__
            # process = Process(
            #     target=fun,
            #     name=f'{name}_task',
            #     args=(None, self.logger.create_writer(name),)
            # )
            self.tasks[name] = Task(fun, self.log_system)
    def serve(self):
        for _, task in self.tasks.items():
            task.start()
        for _, task in self.tasks.items():
            task.join()
        self.log_system.stop()

if __name__ == '__main__':
    manager = TaskManager([webserver, loh])
    manager.serve()
