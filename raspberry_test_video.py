import serial
import cv2
import socket
import pickle
import struct
from ctypes import *

from socketsMessagesProtocol import MessagesProtocol

# C:\Users\undeg\AppData\Local\Microsoft\WindowsApps

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


def get_video(cam):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    ret, frame = cam.read()

    if ret is True:
        frame = cv2.resize(frame, (320, 240))
        result, frame = cv2.imencode('.jpg', frame, encode_param)

        return frame
    else:
        return 'end'


client = connect_server()
ser = connect_arduino()
messagesProtocol = MessagesProtocol(client)
cam = cv2.VideoCapture(0)


class controlMessage(Structure):
    _fields_ = [("value1", c_int8),
         ("value2", c_int16)]

s1 = controlMessage(50, 50)

motors_move = False

while True:
    frame = get_video(cam)

    if frame == 'end':
        messagesProtocol.send_message('end')
        print('end')
        break
    
    messagesProtocol.send_message("OK")
    messagesProtocol.send_message(frame)


    message = messagesProtocol.receive_message(16)

    if message != 'OK':
        break
    
    ser.write(s1)
    # print('kuku')
    # print(ser.read(1))
    print(ser.readline())

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
client.close()