import threading
import queue
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
        # print(message)

        if message != "OK":
          break
      except:
        break
      
      try:
        ultrasonic_data = self.messagesProtocol.receive_message(4096)

        if ultrasonic_data == "No connection":
          break
        if ultrasonic_data != "No sensors data":
          self.add_ultrasonic_data(ultrasonic_data)
      except:
        break
      
      try:
        sys_data = self.messagesProtocol.receive_message(16)

        if sys_data == "No connection":
          break
        if sys_data != "No system data":
          self.add_system_data(sys_data)
      except:
        break
      
    self.print("disconnect Raspberry PI SENSORS")
    self.stop()
    self.raspberry.close()

  def add_ultrasonic_data(self, ultrasonic_data):
    # добавдение показаний с датчиков в очередь
    try:
      self.ultrasonic_data.put(ultrasonic_data, block=False)
    except queue.Full:
      pass

  def get_ultrasonic_data(self):
    # получение показаний датчиков из очереди
    ultrasonic_data = None
    try:
      ultrasonic_data = self.ultrasonic_data.get_nowait()
    except queue.Empty:
      pass

    return ultrasonic_data

  def add_system_data(self, system_data):
    # добавление системных данных в очередь
    try:
      self.system_data.put(system_data)
    except queue.Full:
      pass

  def get_sys_data(self):
    # получение системных данных из очереди
    try:
      return self.system_data.get_nowait()
    except queue.Empty:
      return None

  def print(self, data):
    print("")
    print("[RASPBERRY PI SENSORS]: "+ str(data))

  def stop(self):
    self._stopped = True