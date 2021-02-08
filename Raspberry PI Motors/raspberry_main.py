import serial
import cv2
import socket
import pickle
import struct
import threading
import queue
import time
import psutil
from ctypes import *

from gpiozero import CPUTemperature

from ServerRaspberryThread import ServerThread

# C:\Users\undeg\AppData\Local\Microsoft\WindowsApps

def get_cmd_args():
    import argparse
    parser = argparse.ArgumentParser('Raspberry server')
    parser.add_argument('pc_ip')
    return parser.parse_args()

def cpu():
    return psutil.cpu_percent()

def memory():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    # available = round(memory.available/1024.0/1024.0,1)
    # total = round(memory.total/1024.0/1024.0,1)

    # all data in Bytes

    return {
        "memoryFree": memory.available,
        "memoryTotal": memory.total,
        "memoryPercent": memory.percent
    }

def disk():
    disk = psutil.disk_usage('/')
    # all data in Bytes
    # Divide from Bytes -> KB -> MB -> GB
    # free = round(disk.free/1024.0/1024.0/1024.0,1)
    # total = round(disk.total/1024.0/1024.0/1024.0,1)
    # return str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )
    return {
        "diskFree": disk.free,
        "diskTotal": disk.total,
        "diskPercent": disk.percent
    }

def temperature():
    cpu = CPUTemperature()
    return cpu.temperature

def connect_server():
    client = socket.socket()
    ip_pc = get_cmd_args().pc_ip
    print(ip_pc)
    client.connect((ip_pc, 1080))
    print('connected!')
    return client

def get_system_data():
    cpuData = cpu()
    memoryData = memory()
    diskData = disk()
    temperatureData = temperature()

    return {
        "cpu": cpuData,
        "memory": memoryData,
        "disk": diskData,
        "temperature": temperatureData
    }



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

    system_data = get_system_data()

    serverThread.add_sys_data(system_data)

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