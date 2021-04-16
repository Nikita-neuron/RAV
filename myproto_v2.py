
import myproto
import threading
from twisted.internet import reactor
import time

class PcClientProtocol(myproto.Protocol):
    def __init__(self, name, factory):
        super().__init__()
        self.name = name
        self.factory = factory
    def connectionMade(self):
        super().connectionMade()
        self.i = 0
        # self.img_display = ImageDisplayThread()
        # self.img_display.start()
        self.sendMsg('client_connect', self.name)
    def on_image(self, img):
        print('img', self.i)
        self.i += 1
    def on_systemData(self, data):
        # print('RECV SYSTEM', self.name, data)
        socketio.emit('systemData', data)
    def on_ultrasonic(self, data):
        print("RECV ULTRASONIC", self.name, data)
        socketio.emit('ultrasonic', data)


server_protocol = myproto.PcServerProtocolFactory()
reactor.listenTCP(54321, server_protocol)

client_protocol = myproto.PcClientProtocolFactory(PcClientProtocol)
reactor.connectTCP('localhost', 54321, client_protocol)

reactor.run()
