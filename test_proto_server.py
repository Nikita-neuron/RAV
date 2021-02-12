
from twisted.internet import protocol, reactor, endpoints

class Protocol(protocol.Protocol):
    def dataReceived(self, data):
        print('Recv')
        self.transport.write(b'Hello, World!')

class ProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Protocol()

endpoints.serverFromString(reactor, "tcp:54321").listen(ProtocolFactory())
reactor.run()
