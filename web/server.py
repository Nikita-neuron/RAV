
import sys
sys.path.append('..')
import config

from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import livereload

import time
from twisted.internet import protocol, reactor
import threading
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()
import cv2

async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)



class ImageDisplayThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.img_queue = queue.Queue(20)
    def run(self):
        image_number = 0
        total_time = 0
        time_start = time.time()
        self.sleep_ms = 1
        self.waiting = False
        while True:
            time_start = time.time()
            img = None
            try:
                img = self.img_queue.get_nowait()
            except queue.Empty:
                if not self.waiting:
                    self.sleep_ms += 1
                    self.waiting = True
                continue
            else:
                self.waiting = False
            self.sleep_ms = min(500, self.sleep_ms)

            cv2.imshow('img', img)
            delta_time = time.time() - time_start

            delta_time = min(0.5, delta_time)

            total_time += delta_time
            image_number += 1
            average_time = total_time/image_number
            print('delta time', delta_time, average_time)

            # cv2.waitKey(int(1000*average_time)+1)
            print('MS', self.sleep_ms)
            cv2.waitKey(self.sleep_ms)
    def display(self, img):
        try:
            self.img_queue.put_nowait(img)
        except queue.Full:
            print('full')
            self.sleep_ms = min(1, self.sleep_ms-1)
            pass

# class SocketThread(threading.Thread):
#     def __init__(self, socket: socket.socket):
#         super().__init__(daemon=True)
#         self.socket = socket
#         self.buffer_size = 2048
#         self.buffer = bytearray(self.buffer_size)
#     def run(self):
#         while True:
#             self.socket.recv_into()

class PcClientProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.unpacker = msgpack.Unpacker()
    def sendMsg(self, type_, msg):
        msg['type'] = type_
        msgpack.pack(msg, self.transport)
    def connectionMade(self):
        self.i = 0
        self.img_display = ImageDisplayThread()
        self.img_display.start()
        self.sendMsg('client_connect', {'name': 'webserver'})
        
    def dataReceived(self, data):
        print('recv', self.i, len(data))
        # self.i += 1
        self.unpacker.feed(data)
        for msg in self.unpacker:
            if msg['type'] == 'data':
                print('img', self.i)
                self.i += 1
                self.img_display.display(msg['image'])


class PcClientFactory(protocol.ClientFactory):
    retry_delay = 1.0
    retry_after_connection_loss = True
    retry_after_connection_failure = True
    def __init__(self):
        self.client = None
        self.connection_tries = 0
    def startedConnecting(self, connector):
        print(f'Connecting to {connector.host}:{connector.port}' if self.connection_tries==0 else '.', end='', flush=True)
    def buildProtocol(self, addr):
        self.connection_tries = 0
        print(f'\nConnected to main server ({addr.host}:{addr.port})!')
        self.client = PcClientProtocol(self)
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

@app.route('/')
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)
    # return Response(update_index())

pc_client = PcClientFactory()

@socketio.on('connect')
def handle_connect():
    print('WEBSOCKET CONNECT')

@socketio.on('keys')
def handle_keys(data):
    print('KEYS', data)
    pc_client.sendMsg('motors', data)

def run_webserver():
    print('Starting webserver on port', config.WEBSERVER_PORT)
    socketio.run(app, port=config.WEBSERVER_PORT, debug=False)

def main():
    # app.debug = True
    # livereload.Server(app.wsgi_app).serve(port=5500)
    # app.run(host='localhost'    , port=5500)
    main_pc_ip= config.MAIN_PC_IP
    main_pc_port = config.MAIN_PC_PORT

    webserver_thread = threading.Thread(target=run_webserver, daemon=True)
    webserver_thread.start()
    reactor.connectTCP(main_pc_ip, main_pc_port, pc_client)
    reactor.run()
    print('\nexiting!')


if __name__ == '__main__':
    main() 


# def service_main():
#     import service_interface as interface
#     from service_interface import root
#     import time


#     keyboard_stream = root.setup_interface({
#         'keyboard': interface.Pipe
#     })[0]

#     print('out', keyboard_stream)
#     print('in', root['webserver'])
#     print('WEBSERVER', interface.root)
#     # while True:
#     #     keyboard_stream.send('Hello, PC!')
#     #     time.sleep(1)
#     SocketIOEvents(keyboard_stream)
#     socketio.run(app, host='localhost', port=rav.config.WEBSERVER_PORT)