
import service_interface as interface
import multiprocessing as mp
import multiprocessing.managers as mp_managers

# class ConnectionWrapper():
#     def __init__(self, connection):
#         self.connection = connection
#     def recv(self):
#         # try:
#         return self.connection.recv()
#         # except EOFError:
#         #     print('Connection closed.')
#     def send(self, *args, **kwargs):
#         return self.connection.send


class ServicesRootManager(mp_managers.SyncManager):
    def __init__(self, services):
        super().__init__()
        self.start()
        self.root = self.dict()
        for service in services:
            name = service.raw_name
            self.root[name] = self.dict()
    def __getstate__(self):
        return self.root
    def __setstate__(self, root):
        super().__init__()
        self.root = root
    def setup_interface(self, schema: dict):
        caller_name = interface.service.raw_name
        caller_root = self.root[caller_name]
        pipes_for_caller = []
        for name, obj in schema.items():
            if issubclass(obj, interface.StreamDummy):
                obj = obj()
            if type(obj) == interface.Pipe:
                pipe_recv, pipe_send = mp.Pipe()
                obj = pipe_recv
                pipes_for_caller.append(pipe_send)
            caller_root[name] = obj
        return pipes_for_caller
    def __getitem__(self, module_name):
        return self.root[module_name]
