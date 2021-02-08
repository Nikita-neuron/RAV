import threading
import queue
import socket
import cv2

from RaspberryPIMotorsThread import RaspberryPIMotorsThread
from socketsMessagesProtocol import MessagesProtocol


class ServerConnect(threading.Thread):
  def __init__(self, video_frames):
    super().__init__()

    self.sock = None
    self._stopped = False

    self.video_frames = video_frames

    self._IP_RASPBERRY_MOTORS = "192.168.1.60"
    self.raspberryPIMotorsThread = None

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
    
    if self.raspberryPIMotorsThread is not None:
      self.raspberryPIMotorsThread.stop()
    
    self.sock.close()
    self.print("Server is closed")
    
  def start_connect(self):
    # создание сокета
    self.sock = socket.socket()
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(('', 1080))

  def set_motors_speed(self, motors):
    # установление скорости моторов
    if self.raspberryPIMotorsThread is not None:
      self.raspberryPIMotorsThread.add_motors_speed(motors)
    else:
      self.print("RASPBERRY PI MOTORS is not connect")

  def get_sys_data(self):
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