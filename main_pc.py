
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
            
            if msg['type'] == 'client_connect':
                self.client_name = msg['name']
                print(f'"{self.client_name}" connected')
                self.factory._clientConnect(self)
            elif msg['type'] == 'motors':
                print('Received motors')
                self.factory.sendMsg('raspberryPIMotors', 'motorsSpeed', msg)
            elif msg['type'] == 'systemData':
                pass
            elif msg['type'] == 'frames':
                self.factory.sendMsg('webserver', 'camera', {'spf': 123, 'image': msg['data']})
            else:
                print('Received message:', msg)

        # self.transport.write(b'Hello, World!')
    
    def connectionLost(self, reason):
        print('Connection lost', reason )
        self.factory._clientDisconnect(self)

class PcServerProtocolFactory(protocol.Factory):
    def __init__(self):
        self.clients = {}
        self._onClientConnectHandlers = {}
    def buildProtocol(self, addr):
        return PcServerProtocol(self)
    def get_client(self, name):
        return self.clients.get(name, None)
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
    def _clientDisconnect(self, protocol):
        client_name = protocol.client_name
        del self.clients[client_name]

        handlers = self._onClientConnectHandlers
        deferred = handlers[client_name]
        new_deferred = defer.Deferred()
        new_deferred.callbacks = deferred.callbacks
        handlers[client_name] = new_deferred
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
        client = self.get_client(client_name)
        if client is None:
            return None
        return client.sendMsg(type_, data)

# endpoints.serverFromString(reactor, "tcp:54321").listen(PakkitProtocolFactory())

class CameraThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.daemon = True
        self.capture = cv2.VideoCapture(0)
        self.start_time = None
    def start(self, on_image):
        self.callback = on_image
        super().start()
    def run(self):
        self.start_time = time.time()
        while self.capture.isOpened():
            ret, img = self.capture.read()
            if not ret:
                print('Could not get camera frame')
                continue
            img = cv2.resize(img, (100, 100))
            cv2.imshow('camera', img)
            cv2.waitKey(1)
            self.callback(img)
        print('!!!Video capture closed!!!')

pc_protocol = PcServerProtocolFactory()

# pc_protocol._onClientConnectHandlers['webserver'] = defer.Deferred()
# camera = CameraThread()

@pc_protocol.onClientConnect('webserver')
def on_webserver_connect():
    print('Webserver connected!')
    # image_count = 0
    # def send_img(img):
    #     nonlocal image_count
    #     image_count += 1
    #     current_time = time.time()
    #     spf = (current_time - camera.start_time)/image_count

    #     print('send', image_count, spf, pc_protocol.sendMsg('webserver', 'camera', {'image': img, 'spf': spf}))
    # camera.start(send_img)

@pc_protocol.onClientConnect('raspberryPIMotors')
def on_raspberry_connect():
    print('Raspberry connected!')




def main():
    reactor.listenTCP(config.MAIN_PC_PORT, pc_protocol)
    print('listening on port', config.MAIN_PC_PORT)
    reactor.run()
if __name__ == "__main__":
    main()
