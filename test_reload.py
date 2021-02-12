import logging
import time
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer
import importlib
from pathlib import Path

import multiprocessing as mp

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

import test_sub

process = mp.Process(target=test_sub.f)

class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, whitelist, delay=1.0):
        self.delay = delay
        self.whitelist = {Path(path) for path in whitelist}
        self.last_modified = 0
    def on_modified(self, event):
        if event.is_directory or Path(event.src_path) not in self.whitelist:
            return
        now = time.time()
        if now - self.last_modified < self.delay:
            return
        self.last_modified = now
        self.reload_module(event.src_path)
    def reload_module(self, filename):
        global process
        print('reload', filename)
        process.terminate()
        importlib.reload(test_sub)
        process = mp.Process(target=test_sub.f)
        process.start()

if __name__ == "__main__":
    process.start()

    observer = Observer()
    observer.schedule(WatchdogHandler(['test_sub.py']), '.', recursive=False)
    observer.start()
    observer.join()
