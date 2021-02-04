import sys
import multiprocessing
from multiprocessing import Process
import threading
import queue
import io
# import web.server

# web.server.run()

# args: out, log



    # sys.stdout = stdout
    # print('WEB', file=open(fileno, 'w'))
    # import web.server
    # web.server.run()

class Logger:
    def __init__(self, file=sys.stdout):
        self.file = file
        self.queue = multiprocessing.Queue()
        self.writers = []

        self._maintainer_thread = threading.Thread(target=self._maintainer)
        self._stopped = False
        self._maintainer_thread.start()
    def _maintainer(self):
        while not self._stopped:
            try:
                msg = self.queue.get(block=False)
            except queue.Empty:
                continue
            print(msg, file=self.file)
    def create_writer(self, prefix):
        writer = LogWriter(prefix, self.queue)
        self.writers.append(writer)
        return writer
    def stop(self):
        self._stopped = True
class LogWriter:
    def __init__(self, prefix, queue):
        self.prefix = prefix
        # self.logger = logger
        self.queue = queue
    def write(self, data):
        s = f'[{self.prefix}] {data}'
        self.queue.put(s)
        return len(s)
    def flush(self):
        # TODO
        pass

def webserver():
    # print(out, log)
    print('WEBSERVER')

def loh():
    # print(out, log)
    print('LOH')
    # raise 1

class Task(Process):
    def __init__(self, target, logger):
        # print('TASK INIT', target, logger)
        super().__init__(
            target=target,
            name=target.__name__,
        )
        self.log_writer = logger.create_writer(self.name)
        # self.logger = logger.create_writer(self.name)
        # self.process = Process(
        #     target=target,
        #     name=f'{self.name}_task',
        #     args=(None, self.logger.create_writer(self.name),)
        # )
    def run(self):
        sys.stdout = self.log_writer
        super().run()
class TaskManager:
    def __init__(self, tasks_functions):
        self.tasks_functions = tasks_functions
        self.tasks = {}
        self.logger = Logger()
        for fun in tasks_functions:
            name = fun.__name__
            # process = Process(
            #     target=fun,
            #     name=f'{name}_task',
            #     args=(None, self.logger.create_writer(name),)
            # )
            self.tasks[name] = Task(fun, self.logger)
    def serve(self):
        for _, task in self.tasks.items():
            task.start()
        for _, task in self.tasks.items():
            task.join()
        self.logger.stop()

if __name__ == '__main__':
    manager = TaskManager([webserver, loh])
    manager.serve()
