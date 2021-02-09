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
    i = 0
    while not self._stopped:
            
      self.messagesProtocol.send_message("OK")

      mess = self.messagesProtocol.receive_message(16)

      if mess != "OK":
        break

      ultrasonic_data = self.get_ultrasonic_data()
      print('GAVNO', i)
      i += 1

      # if ultrasonic_data != "No sensors data":
        # print("t: " + str(ultrasonic_data))
      self.messagesProtocol.send_message(ultrasonic_data)

      sys_data = self.get_sys_data()
      self.messagesProtocol.send_message(sys_data)
            
  def add_ultrasonic_data(self, ultrasonic_data):
    # добавление данных датчиков в очередь
    try:
      self.ultrasonic_data.put(ultrasonic_data, block=False)
      print("t: " + str(ultrasonic_data))
    except queue.Full:
      print('FULL')
      pass

  def get_ultrasonic_data(self):
    # получение данных датчиков из очереди
    try:
      return self.ultrasonic_data.get_nowait()
    except queue.Empty:
      return "No sensors data"

  def add_sys_data(self, sys_data):
    # добавление системных данных в очередь
    try:
      self.sys_data.put(sys_data, block=False)
    except queue.Full:
      pass

  def get_sys_data(self):
    # получение системных данных из очереди
    sys_data = "No system data"
    try:
      sys_data = self.sys_data.get_nowait()
    except queue.Empty:
      pass
    return sys_data

  def stop(self):
    self._stopped = True
