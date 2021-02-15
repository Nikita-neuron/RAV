
import config

from twisted.internet import protocol, reactor, defer
# from pakkit.types import Struct

import threading
import cv2
import time
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class PcServerProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.unpacker = msgpack.Unpacker()
        self.factory = factory
    def sendMsg(self, type_, msg):
        if type(msg) != dict:
            raise TypeError('msg должно быть dict')
        msg['type'] = type_
        b = msgpack.packb(msg)
        self.transport.write(b)
        return len(b)
    def connectionMade(self):
        self.client_address = self.transport.getPeer()
        self.client_name = None
        print(f'Connected to {self.client_address.host}:{self.client_address.port}')
    def dataReceived(self, data):
        self.unpacker.feed(data)
        for msg in self.unpacker:
            print('Received message:', msg)
            if msg['type'] == 'client_connect':
                self.client_name = msg['name']
                print(f'"{self.client_name}" connected')
                self.factory._clientConnect(self)
        # self.transport.write(b'Hello, World!')
    
    def connectionLost(self, reason):
        print('Connection lost', reason )

class PcServerProtocolFactory(protocol.Factory):
    def __init__(self):
        self.clients = {}
        self._onClientConnectHandlers = {}
    def buildProtocol(self, addr):
        return PcServerProtocol(self)
    def _clientConnect(self, protocol):
        '''
        Кастомный метод, вызывается в PcServerProtocol при отправке сообщения "connected"
        '''
        client_name = protocol.client_name
        self.clients[client_name] = protocol

        handlers = self._onClientConnectHandlers
        deferred = handlers.get(client_name, defer.Deferred())
        handlers[client_name] = deferred
        deferred.callback(None)
    def onClientConnect(self, client_name):
        '''
        Декоратор. Вызывается когда подключается клиент под именем client_name:
            @pc_protocol.onClientConnect('webserver')
            def handler():
                print('Connected!')
        '''
        def f(handler):
            handlers = self._onClientConnectHandlers
            deferred = handlers.get(client_name, defer.Deferred())
            deferred.addCallback(lambda _: handler())
            handlers[client_name] = deferred
            return handler
        
        return f
    def sendMsg(self, client_name, type_, data):
        return self.clients[client_name].sendMsg(type_, data)

# endpoints.serverFromString(reactor, "tcp:54321").listen(PakkitProtocolFactory())

class CameraThread(threading.Thread):
    def __init__(self, on_image: 'Callable'):
        super().__init__(daemon=True)
        self.callback = on_image
        self.capture = cv2.VideoCapture(0)
    def run(self):
        while self.capture.isOpened():
            _, img = self.capture.read()
            img = cv2.resize(img, (100, 100))
            cv2.imshow('camera', img)
            cv2.waitKey(1)
            self.callback(img)
        print('!!!Video capture closed!!!')

pc_protocol = PcServerProtocolFactory()

# pc_protocol._onClientConnectHandlers['webserver'] = defer.Deferred()

@pc_protocol.onClientConnect('webserver')
def on_webserver_connect():
    i = 0
    def send_img(img):
        nonlocal i
        print('send', i, pc_protocol.sendMsg('webserver', 'data', {'image': img}))
        i += 1
        # time.sleep(0.1)
    camera = CameraThread(send_img)
    camera.start()
    print('Webserver connected!')
    




def main():
    reactor.listenTCP(config.MAIN_PC_PORT, pc_protocol)
    print('listening on port', config.MAIN_PC_PORT)
    reactor.run()
if __name__ == "__main__":
    main()
