import serial
import socket
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


class UltrasonicStructure(Structure):
    _pack_ = 1
    _fields_ = [
        ("dis1", c_int8), ("dis2", c_int8), 
        ("dis3", c_int8), ("dis4", c_int8), 
        ("dis5", c_int8), ("dis6", c_int8)
    ]

while True:

    system_data = get_system_data()

    serverThread.add_sys_data(system_data)

    serial_data = arduino.read(6)

    ultrasonicData = UltrasonicStructure.from_buffer_copy(serial_data)
    # print(ultrasonicData.dis1)

    serverThread.add_ultrasonic_data([
        ultrasonicData.dis1,
        ultrasonicData.dis2,
        ultrasonicData.dis3,
        ultrasonicData.dis4,
        ultrasonicData.dis5,
        ultrasonicData.dis6
    ])

server.close()
