import threading
import queue
import socket

from socketsMessagesProtocol import MessagesProtocol

class ServerThread(threading.Thread):
  def __init__(self, server):
    super().__init__()

    self.server = server
    self.ultrasonic_data = queue.Queue(2)
    self._stopped = False

    self.sys_data = queue.Queue(2)

    self.messagesProtocol = MessagesProtocol(server)
    
  def run(self):
    while not self._stopped:
            
      self.messagesProtocol.send_message("OK")

      ultrasonic_data = self.get_ultrasonic_data()

      print(ultrasonic_data)

      self.messagesProtocol.send_message(ultrasonic_data)

      sys_data = self.get_sys_data()

      self.messagesProtocol.send_message(sys_data)
            
  def add_ultrasonic_data(self, ultrasonic_data):
    # добавление скорости моторов в очередь
    try:
      self.ultrasonic_data.put(ultrasonic_data, block=False)
    except queue.Full:
      pass

  def get_ultrasonic_data(self):
    # получение скорости моторов из очереди
    try:
      return self.ultrasonic_data.get_nowait()
    except queue.Empty:
      return "No sensors data"

  def add_sys_data(self, sys_data):
    try:
      self.sys_data.put(sys_data, block=False)
    except queue.Full:
      pass

  def get_sys_data(self):
    sys_data = "No system data"
    try:
      sys_data = self.sys_data.get_nowait()
    except queue.Empty:
      pass
    return sys_data

  def stop(self):
    self._stopped = True
