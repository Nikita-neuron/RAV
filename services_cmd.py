
import cmd2
import threading
import traceback
import time

class ServiceManagerCmd(cmd2.Cmd):
    def __init__(self, manager):
        super().__init__()
        self.prompt = '(ServiceManager) '
        self.manager = manager
        def f():
            while True:
                time.sleep(1)
                print('thread')
                self.async_update_prompt('fff')
        threading.Thread(target=f).start()
    def do_restart(self, service):
        '''restart [service]
        Перезагружает сервис.
        '''
        pass
    # def complete_restart(self, text, line, begidx, endidx):
    #     print([text, line, begidx, endidx])
    #     return [s for s in ['aa', 'ab', 'ccc'] if s.startswith(text)]
    # def default(self, line):
    #     try:
    #         val = eval(line)
    #         if val is not None:
    #             print(val)
    #     except Exception:
    #         traceback.print_exc(chain=False)
    def do_exit(self, args):
        return True



if __name__ == '__main__':
    smcmd = ServiceManagerCmd(123)
    smcmd.cmdloop()
