import threading
import queue
import socket
import cv2

from RaspberryPIMotorsThread import RaspberryPIMotorsThread
from RaspberryPISensorsThread import RaspberryPISensorsThread
from socketsMessagesProtocol import MessagesProtocol


class ServerConnect(threading.Thread):
  def __init__(self, video_frames):
    super().__init__()

    self.sock = None
    self._stopped = False

    self.video_frames = video_frames

    self._IP_RASPBERRY_MOTORS = "192.168.1.60"
    self.raspberryPIMotorsThread = None

    self._IP_RASPBERRY_SENSORS = "192.168.1.3"
    self.raspberryPISensorsThread = None

  def run(self):
    self.start_connect()

    while not self._stopped:
      self.print("listen...")
      self.sock.listen(1)

      try:
        client, adr = self.sock.accept()
      except:
        break

      self.print("connected: " + str(adr[0]) + " " + str(adr[1]))

      if adr[0] == self._IP_RASPBERRY_MOTORS:
        # если подключена распберри с моторами
        self.raspberryPIMotorsThread = RaspberryPIMotorsThread(client, self.video_frames)
        self.raspberryPIMotorsThread.start()

      if adr[0] == self._IP_RASPBERRY_SENSORS:
        # если подключена распберри с сенсорами
        self.raspberryPISensorsThread = RaspberryPISensorsThread(client)
        self.raspberryPISensorsThread.start()
    
    if self.raspberryPIMotorsThread is not None:
      self.raspberryPIMotorsThread.stop()

    if self.raspberryPISensorsThread is not None:
      self.raspberryPISensorsThread.stop()
    
    self.sock.close()
    self.print("Server is closed")
    
  def start_connect(self):
    # создание сокета
    self.sock = socket.socket()
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(('', 1080))

  def set_motors_speed(self, motors):
    # установление скорости моторов
    try:
      self.raspberryPIMotorsThread.add_motors_speed(motors)
    except:
      self.print("RASPBERRY PI MOTORS is not connect")

  def get_ultrasonic_data(self):
    # получение данных сенсоров с распберри
    try:
      return self.raspberryPISensorsThread.get_ultrasonic_data()
    except:
      self.print("RASPBERRY PI SENSORS is not connect")
      return None

  def get_sys_data(self):
    # получение системных данных с распберри
    try:
      return self.raspberryPIMotorsThread.get_sys_data()
    except:
      self.print("RASPBERRY PI MOTORS is not connect")
      return None

  def print(self, data):
    print("")
    print("[SERVER]: "+ str(data))

  def stop(self):
    self._stopped = True
    self.sock.close()