
import sys
import pyfiglet
import importlib.util
# sys.path.append('..')
# import config
spec = importlib.util.spec_from_file_location('config', r'config.py')
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

import flask
from flask import Flask, Response, render_template
from flask_socketio import SocketIO
# import livereload

import time
from twisted.internet import protocol, reactor
import myproto
from myproto import PcClientProtocolFactory
import threading
import queue
# import msgpack
# import msgpack_numpy
# msgpack_numpy.patch()
import cv2
import numpy as np
import traceback

from engineio.payload import Payload

Payload.max_decode_packets = 50


old_print = print
def spy_print(*args, **kwargs):
    frame = traceback.extract_stack()[-2]
    old_print(f'[{frame.name}]', *args, **kwargs)
print = spy_print

async_mode = None
app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
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



@app.route('/')
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)
    # return Response(update_index())

@app.route('/<path:filename>')
def file_route(filename):
    mimetype = 'text/javascript' if filename.endswith('.js') else None
    
    # for _ in range(1000):
    #     print('ROUTE', filename, mimetype)
    return flask.send_from_directory(app.static_folder, filename, mimetype=mimetype)

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
    sticks = joystick['sticks']
    buttons = joystick['buttons']
    left_stick_y = sticks['left'][1]
    right_stick_y = sticks['right'][1]
    lb = buttons['lb']
    rb = buttons['rb']
    
    motors = np.int8(100*np.array([right_stick_y, left_stick_y])).clip(-100, 100)
    platform = 30*lb['pressed'] - 30*rb['pressed']
    print('Send', motors)
    pc_client.sendMsg('motorsSpeed', [*motors, platform])

@socketio.on("gyroscopeData")
def gyroscope_data(gyroscopeData):
    x = round(gyroscopeData['alpha'], 1)
    y = round(gyroscopeData['gamma'], 1)
    if y > 0: y -= 90
    else: y += 90
    gyroscope = [x, y]
    print(gyroscope)
    pc_client.sendMsg('gyroscope', gyroscope)


def run_webserver():
    print('Starting webserver on port', config.WEBSERVER_PORT)
    import webbrowser 
    new = 2 # open in a new tab, if possible

    # open a public URL, in this case, the webbrowser docs
    url = "http://localhost:" + str(config.WEBSERVER_PORT)
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url,new=new)
    socketio.run(app, port=config.WEBSERVER_PORT, debug=False, host="0.0.0.0")


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
pc_client = PcClientProtocolFactory(PcClientProtocol)


def main():
    # app.debug = True
    # livereload.Server(app.wsgi_app).serve(port=5500)
    # app.run(host='localhost'    , port=5500)
    main_pc_ip= config.MAIN_PC_IP
    main_pc_port = config.MAIN_PC_PORT

    result = pyfiglet.figlet_format("R A V")
    print(result)

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
