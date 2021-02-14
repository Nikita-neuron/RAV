
from twisted.internet import protocol, reactor, endpoints
# from pakkit.types import Struct

import cv2
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class PakkitProtocol(protocol.Protocol):
    def connectionMade(self):
        print('Connect')
        msgpack.pack({'img': cv2.imread('AAA.bmp')}, self.transport)
        msgpack.pack({'sensors': [0, 0, 1, 2]}, self.transport)
        
    def dataReceived(self, data):
        print('Recv', data)
        # self.transport.write(b'Hello, World!')

class PakkitProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PakkitProtocol()

endpoints.serverFromString(reactor, "tcp:54321").listen(PakkitProtocolFactory())
reactor.run()
