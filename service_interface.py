
import multiprocessing as mp
# from services import ServiceManager, Service

class StreamDummy:
    pass
class Pipe(StreamDummy):
    def __init__(self, duplex=True):
        pass

service: 'Service'
# manager: 'ServiceManager'
# this_root: dict
root: 'ServicesRootManager'

