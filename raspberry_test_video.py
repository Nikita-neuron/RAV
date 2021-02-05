import serial
import cv2
import socket
import pickle
import struct
import threading
import time
from ctypes import *

from socketsMessagesProtocol import MessagesProtocol

# C:\Users\undeg\AppData\Local\Microsoft\WindowsApps

class ServerThread(threading.Thread):
    def __init__(self, server):
        super().__init__()

        self.server = server
        self._stopped = False

        self.messagesProtocol = MessagesProtocol(server)
        self.cam = cv2.VideoCapture(0)

    def get_video(self):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        ret, frame = self.cam.read()

        if ret is True:
            frame = cv2.resize(frame, (320, 240))
            result, frame = cv2.imencode('.jpg', frame, encode_param)

            return frame
        else:
            return 'end'
    
    def run(self):
        while self._stopped:
            frame = self.get_video()

            if frame == 'end':
                self.messagesProtocol.send_message('end')
                print('end')
                break
            
            self.messagesProtocol.send_message("OK")
            self.messagesProtocol.send_message(frame)


            message = self.messagesProtocol.receive_message(16)

            if message != 'OK':
                break

    def stop(self):
        self._stopped = True






def get_cmd_args():
    import argparse
    parser = argparse.ArgumentParser('Raspberry server')
    parser.add_argument('pc_ip')
    return parser.parse_args()


def connect_server():
    client = socket.socket()
    ip_pc = get_cmd_args().pc_ip
    print(ip_pc)
    client.connect((ip_pc, 1080))
    print('connected!')
    return client


def connect_arduino():
    ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
    ser.baudrate = 9600

    return ser


def Pack(ctype_instance):
    buf = string_at(byref(ctype_instance), sizeof(ctype_instance))
    return buf


client = connect_server()

serverThread = ServerThread(client)

serverThread.start()

ser = connect_arduino()


class controlMessage(Structure):
    _pack_ = 1
    _fields_ = [("value1", c_int8),
         ("value2", c_int8)]

s1 = controlMessage(-60, 50)

motors_move = False

time.sleep(0.1)

while True:

    data = pickle.dumps(s1, 0)
    size = len(data)

    # print("send: " + str(Pack(s1)))

    ser.write(Pack(s1))

    while True:
        serial_data = ser.read(2)
    # messSize = struct.unpack("B", messSize)[0]

        print('Serial:', serial_data)
        print('Ass:', controlMessage.from_buffer_copy(serial_data))
    
    # data = b''

    # if messSize > 0:

    #     while len(data) < 5:
    #         data += ser.read()

    #     # data = struct.unpack("HH", data)
        
    #     print("arduino: " + str(data.decode()))

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
client.close()