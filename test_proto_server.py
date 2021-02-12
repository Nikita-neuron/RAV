
from twisted.internet import protocol, reactor, endpoints
from pakkit.types import Struct

class PakkitProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print('Recv', data)
        self.transport.write(b'Hello, World!')

class PakkitProtocolFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PakkitProtocol()

endpoints.serverFromString(reactor, "tcp:54321").listen(PakkitProtocolFactory())
reactor.run()
