import serial
import cv2
import socket
import pickle
import struct
import threading
import queue
import time
from ctypes import *

from ServerRaspberryThread import ServerThread

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


server = connect_server()

serverThread = ServerThread(server)
serverThread.start()

arduino = connect_arduino()


class MotorsStructure(Structure):
    _pack_ = 1
    _fields_ = [("r", c_int8), ("l", c_int8)]

while True:

    motors = serverThread.get_motors_speed()

    motors_arduino = MotorsStructure(motors[0], motors[1])

    arduino.write(string_at(byref(motors_arduino), sizeof(motors_arduino)))

    serial_data = arduino.read(2)

    motors_from_arduino = MotorsStructure.from_buffer_copy(serial_data)
    print(motors_from_arduino.r)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
server.close()