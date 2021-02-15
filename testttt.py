
import threading
import time

class GavnoThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.i = 0
    def run(self):
        while True:
            print(self.i)
            time.sleep(1)

thread = GavnoThread()
thread.start()
thread.i = 1
