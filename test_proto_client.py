

from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout
import cv2
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class Echo(Protocol):
    def __init__(self):
        self.unpacker = msgpack.Unpacker()
        super().__init__()
    def dataReceived(self, data):
        self.unpacker.feed(data)
        for msg in self.unpacker:
            if 'img' in msg:
                cv2.imshow('img', msg['img'])
                cv2.waitKey()
            elif 'sensors' in msg:
                print('Sensors', msg['sensors'])
    def connectionMade(self):
        print('Connected')
        # self.transport.write(b'Hello, Server!')

class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)

from twisted.internet import reactor
reactor.connectTCP('localhost', 54321, EchoClientFactory())
reactor.run()
