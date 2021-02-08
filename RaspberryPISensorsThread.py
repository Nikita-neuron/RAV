import threading
import queue
import cv2
import socket

from socketsMessagesProtocol import MessagesProtocol

class RaspberryPISensorsThread(threading.Thread):
  def __init__(self, raspberry):
    super().__init__()

    self._stopped = False
    self.raspberry = raspberry

    self.ultrasonic_data = queue.Queue(2)

    self.system_data = queue.Queue(2)

    self.messagesProtocol = MessagesProtocol(self.raspberry)

  def run(self):
    self.print("Connection successful")
    while not self._stopped:
      try:
        message = self.messagesProtocol.receive_message(16)
      except:
        break

      if message == 'end' or message is None:
        break
    
      ultrasonic_data = self.messagesProtocol.receive_message(4096)
    #   self.print(ultrasonic_data)

      if ultrasonic_data != "No sensors data":
          self.add_ultrasonic_data(ultrasonic_data)

      sys_data = self.messagesProtocol.receive_message(16)

      if sys_data != "No system data":
        self.add_system_data(sys_data)
      
    self.print("disconnect Raspberry PI SENSORS")
    self.stop()
    self.raspberry.close()

  def add_ultrasonic_data(self, ultrasonic_data):
    # добавдение скорости моторов в очередь
    try:
      self.ultrasonic_data.put(ultrasonic_data, block=False)
    except queue.Full:
      pass

  def get_ultrasonic_data(self):
    # получение скорости моторов из очереди
    ultrasonic_data = [0, 0, 0, 0, 0, 0]
    try:
      ultrasonic_data = self.ultrasonic_data.get_nowait()
    except queue.Empty:
      pass

    return ultrasonic_data

  def add_system_data(self, system_data):
    try:
      self.system_data.put(system_data)
    except queue.Full:
      pass

  def get_sys_data(self):
    try:
      return self.system_data.get_nowait()
    except queue.Empty:
      return None

  def print(self, data):
    print("")
    print("[RASPBERRY PI SENSORS]: "+ str(data))

  def stop(self):
    self._stopped = True