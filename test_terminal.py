

import traceback
import threading
import queue
import time
import sys
import multiprocessing as mp
from blessed import Terminal

import platform
if platform.system() == 'Windows':
    import ctypes
    from ctypes.wintypes import DWORD

    kernel32 = ctypes.windll.kernel32
    # Terminal.get_location зависает при input()+потоках на Windows
    from colorama.win32 import GetConsoleScreenBufferInfo, _GetStdHandle
    def __patch_terminal_get_location(self) -> '(y, x)':
        pos = GetConsoleScreenBufferInfo().dwCursorPosition
        return pos.Y, pos.X
    Terminal.get_location = __patch_terminal_get_location
    
    def peek_console_input():
        buf = ctypes.create_string_buffer(128)
        n_read = DWORD()
        success = kernel32.PeekConsoleInputA(_GetStdHandle(-10), buf, 128, ctypes.byref(n_read))
        print('Read', n_read)
        if not success:
            raise ValueError('Ашыбка')
        return buf.value


# print(peek_console_input())
# raise 1

term = Terminal()


'''
1) start
    ab>>> 
2) print 'cd'
    abcd>>
'''
def lag(s):
    f = open('test_terminal.txt', 'w')
    f.write(s)
    f.close()

class StdoutWrapper:
    def __init__(self, prompt, stdout):
        self.prompt = prompt
        self.stdout = stdout
        self.stdout_lock = mp.Lock()
        with self.stdout_lock:
            self._print_prompt()
    def _print_prompt(self):
        # self.prompt_begin = get_cursor_pos()
        self.prompt_begin = term.get_location()
        lag(f'{self.prompt_begin}\n')
        self.stdout.write(self.prompt)
    def write(self, data):
        with self.stdout_lock:
            # move to beginning of prompt, clear, print data
            self.stdout.write(
                term.move_yx(*self.prompt_begin)+
                term.clear_eos+
                data)
            self.stdout.flush()
            # print prompt
            self._print_prompt()
            self.stdout.flush()
    def flush(self):
        self.stdout.flush()
wr = sys.stdout = StdoutWrapper('>>> ', sys.stdout)
print('dffgg')

def f():
    while True:
        time.sleep(1)
        print('thread')

thread = threading.Thread(target=f)
thread.start()

# class InputReader(threading.Thread):
#     def __init__(self, term):
#         super().__init__()
#         self.term = term
#         self.current_input = []
#         self.inputs = queue.Queue()
#     def run(self):
#         term = self.term
#         with term.cbreak():
#             while True:
#                 c = term.inkey()
#                 if not c.is_sequence:
#                     self.current_input.append(c)
#                 elif c.name == 'KEY_BACKSPACE'
#                     self.current_input.pop(-1)
#                 elif c.name == 'KEY_'

# InputReader(term).start()
print(input())
