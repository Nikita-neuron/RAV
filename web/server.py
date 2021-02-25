
import sys
import importlib.util
# sys.path.append('..')
# import config
spec = importlib.util.spec_from_file_location('config', r'D:\Python\RAV\config.py')
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import livereload

import time
from twisted.internet import protocol, reactor
from myproto import PcClientProtocolFactory
import threading
import queue
# import msgpack
# import msgpack_numpy
# msgpack_numpy.patch()
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

# class PcClientProtocol(protocol.Protocol):
#     def __init__(self, factory):
#         self.factory = factory
#         self.unpacker = msgpack.Unpacker()
#     def sendMsg(self, type_, msg):
#         msg['type'] = type_
#         msgpack.pack(msg, self.transport)
#     def connectionMade(self):
#         self.i = 0
#         # self.img_display = ImageDisplayThread()
#         # self.img_display.start()
#         self.sendMsg('client_connect', {'name': 'webserver'})
#     # {'type': 'image', }
#     def dataReceived(self, data):
#         print('recv', self.i, len(data))
#         self.unpacker.feed(data)
#         for msg in self.unpacker:
#             if msg['type'] == 'data':
#                 print('img', self.i)
#                 self.i += 1
#                 # self.img_display.display(msg['image'])
#                 # _, encoded = 
#                 # socketio.emit('image', {'data': cv2.})



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

# @socketio.on('keys')
# def handle_keys(keys):
#     print('KEYS', keys)
#     pc_client.sendMsg('motors', {'data': keys_to_motors(keys)})

@socketio.on('joystick')
def handle_keys(joystick):
    print('JOYSTICK', joystick)
    right_stick = joystick['sticks']['right']
    # right_stick = joystick['sticks']['right']
    
    motors = np.int(100*np.array(right_stick)).clip(-100, 100)
    pc_client.sendMsg('motors', {'data': motors})


def run_webserver():
    print('Starting webserver on port', config.WEBSERVER_PORT)
    socketio.run(app, port=config.WEBSERVER_PORT, debug=False)

pc_client = PcClientProtocolFactory()

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