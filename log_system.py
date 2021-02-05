
import sys
import multiprocessing
import threading
import queue

class LogSystem:
    def __init__(self, file=sys.stdout):
        self.file = file
        self.queue = multiprocessing.Queue()
        self.loggers = []

        self._maintainer_thread = threading.Thread(
            target=self._maintainer,
            name='LogSystem._maintainer',
            daemon=True
        )
        self._stopped = False
        self._maintainer_thread.start()
    def _maintainer(self):
        # last_logger = None
        while not self._stopped:
            try:
                msg = self.queue.get(block=False)
            except queue.Empty:
                continue
            print(msg, file=self.file)
    def create_logger(self, prefix):
        writer = Logger(prefix, self)
        self.loggers.append(writer)
        return writer
    def stop(self):
        self._stopped = True
    def __getstate__(self):
        '''
        Почему-то pickle выдает ошибку "EOFError: Ran out of input"
        без этих двух функций (__[get/set]state__)
        '''
        # print('getstate')
        pass
    def __setstate__(self, state):
        # print('setstate', state)
        pass


class Logger:
    def __init__(self, prefix, log_system):
        self.prefix = prefix
        self.log_system = log_system
        self.queue = multiprocessing.Queue() # Для склейки сообщений print'а
    def write(self, data):
        s = f'[{self.prefix}] {data}'
        self.queue.put(s)
        return len(s)
    def flush(self):
        self.log_system.queue.write()
