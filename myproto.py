
from twisted.internet import protocol, reactor
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class Protocol(protocol.Protocol):
    def __init__(self):
        self._unpacker = msgpack.Unpacker()
    def connectionMade(self):
        self.client_address = self.transport.getPeer()
        self.client_name = None
        print(f'[{self.name}] Connected to {self.client_address.host}:{self.client_address.port}')
    def sendMsg(self, type_, data):
        msg = {'type': type_, 'data': data}
        b = msgpack.packb(msg)
        self.transport.write(b)
        return len(b)
    def dataReceived(self, data):
        self._unpacker.feed(data)
        for msg in self._unpacker:
            # print(msg)
            msg_type = msg['type']
            callback_name = 'on_'+msg_type
            if hasattr(self, callback_name):
                getattr(self, callback_name)(msg['data'])
                continue
            print(f'{self}: Unknown message type "{msg_type}"')





class PcClientProtocolFactory(protocol.ClientFactory):
    name = 'webserver'
    retry_delay = 1.0
    retry_after_connection_loss = True
    retry_after_connection_failure = True
    def __init__(self, protocol):
        self.client = None
        self.connection_tries = 0
        self.protocol = protocol
    def startedConnecting(self, connector):
        print(f'Connecting to {connector.host}:{connector.port}' if self.connection_tries==0 else '.', end='', flush=True)
    def buildProtocol(self, addr):
        self.connection_tries = 0
        print(f'\nConnected to main server ({addr.host}:{addr.port})!')
        self.client = self.protocol(self.name, self)
        return self.client
    def retryConnection(self, connector):
        # print('.', end='', flush=True)
        def retry():
            connector.connect()
        reactor.callLater(self.retry_delay, retry)
    def clientConnectionLost(self, connector, reason):
        self.connection_tries = 0
        print('Connection to main server lost!', connector, reason)
        if self.retry_after_connection_loss:
            self.retryConnection(connector)
    def clientConnectionFailed(self, connector, reason):
        if self.retry_after_connection_failure:
            self.connection_tries += 1
            self.retryConnection(connector)
    def sendMsg(self, type_: str, msg):
        if self.client is not None:
            print('send message', type_, msg, self.client)
            self.client.sendMsg(type_, msg)
    def on_joystick(self, msg):
        print(msg)


class PcServerProtocolFactory(protocol.Factory):
    def __init__(self):
        self.clients = {}
    def buildProtocol(self, addr):
        return PcServerProtocol(self)
    def _on_client_connect(self, protocol):
        self.clients[protocol.name] = protocol
    def sendMsg(self, client_name, type_, data):
        try:
            client = self.clients[client_name]
        except KeyError:
            return None
        return client.sendMsg(type_, data)


class PcServerProtocol(Protocol):
    def __init__(self, factory: 'PcServerProtocolFactory'):
        super().__init__()
        self.factory = factory
        self.name = None
    def on_client_connect(self, name):
        self.name = name
        print(f'"{self.name}" connected')
        self.factory._on_client_connect(self)
    def on_motorsSpeed(self, data):
        print('recv motors', data)
        self.factory.sendMsg('raspberryPIMotors', 'motorsSpeed', data)
    def on_gyroscope(self, data):
        print(data)
        self.factory.sendMsg('raspberryPIMotors', 'gyroscope', data)
    def on_systemData(self, data):
        self.factory.sendMsg('webserver', 'systemData', {'name': self.name, **data})
    def on_ultrasonic(self, data):
        self.factory.sendMsg('webserver', 'ultrasonic', {'name': self.name, **data})

