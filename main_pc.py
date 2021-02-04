import sys
import multiprocessing
from multiprocessing import Process
import threading
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
    def _maintainer(self):
        while not self._stopped:
            msg = self.queue.get(block=True)
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
        print('Write', self.prefix, data)
        self.queue.put(f'[{self.prefix}] {data}')

def webserver(out=None, log=None):
    # print(out, log)
    log.write('WEBSERVER')

def loh(out=None, log=None):
    # print(out, log)
    log.write('LOH')
    # raise 1

if __name__ == '__main__':
    tasks_functions = [webserver, loh]
    tasks = []
    logger = Logger()
    for fun in tasks_functions:
        name = fun.__name__
        process = Process(target=fun, name=f'{name}_task', args=(None, logger.create_writer(name),))
        tasks.append(process)
        process.start()
    for task in tasks:
        print(1)
        task.join()
        print(2)
    logger.stop()
    # process = Process(target=webserver, name='webserver_process')
    # process.start()
    # process.join()

