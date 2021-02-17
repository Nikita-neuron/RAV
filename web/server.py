
import sys
import importlib.util
# sys.path.append('..')
# import config
spec = importlib.util.spec_from_file_location('config', 'C:\\Users\\undeg\\Documents\\RAV\\config.py')
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

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
import numpy as np

async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)



class ImageDisplayThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.img_queue = queue.Queue(100)
    def run(self):
        last_display = 0
        while True:
            last_display = time.time()
            spf, img = self.img_queue.get()
            current_time = time.time()
            cv2.imshow('img', img)
            time_delta = current_time - last_display
            print('SPF', spf, time_delta-spf)
            # cv2.waitKey(max(1, int(1000*(
            #     time_delta - spf
            # ))))
            cv2.waitKey(1)

        # image_number = 0
        # total_time = 0
        # time_start = time.time()
        # self.sleep_ms = 1
        # self.waiting = False
        # while True:
        #     time_start = time.time()
        #     img = self.img_queue.get()
        #     cv2.imshow('img', img)
        #     delta_time = time.time() - time_start

        #     delta_time = min(0.5, delta_time)

        #     total_time += delta_time
        #     image_number += 1
        #     average_time = total_time/image_number
        #     print('delta time', delta_time, average_time)

        #     cv2.waitKey(int(1000*average_time)+30)
    def display(self, spf, img):
        try:
            self.img_queue.put_nowait((spf, img))
        except queue.Full:
            print('full')

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
    # {'type': 'image', }
    def dataReceived(self, data):
        print('recv', self.i, len(data))
        self.unpacker.feed(data)
        for msg in self.unpacker:
            if msg['type'] == 'camera':
                print('img', self.i, msg['spf'])
                self.i += 1
                self.img_display.display(msg['spf'], cv2.imdecode(msg['image'], cv2.IMREAD_COLOR))
                # _, encoded = 
                # socketio.emit('image', {'data': cv2.})


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

@socketio.on('connect')
def handle_connect():
    print('WEBSOCKET CONNECT')

def keys_to_motors(keys: dict):
    speeds = np.array([0, 0])
    if keys['w']:
        speeds += [50, 50]
    if keys['s']:
        speeds += [-50, -50]
    if keys['a']:
        speeds += [25, -25]
    if keys['d']:
        speeds += [-25, 25]
    return list(speeds)

@socketio.on('keys')
def handle_keys(keys):
    print('KEYS', keys)
    pc_client.sendMsg('motors', {'data': keys_to_motors(keys)})

def run_webserver():
    print('Starting webserver on port', config.WEBSERVER_PORT)
    socketio.run(app, port=config.WEBSERVER_PORT, debug=False)

pc_client = PcClientFactory()

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