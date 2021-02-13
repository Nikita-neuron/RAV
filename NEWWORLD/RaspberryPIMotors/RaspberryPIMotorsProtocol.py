from twisted.internet import protocol
import cv2
import queue

class RaspberryPIMotorsProtocol(protocol.Protocol):

  def __init__(self):
    self.queueData = {
      "soundsPC":     queue.Queue(2),
      "motorsSpeed":  queue.Queue(1)
    }

  def connectionMade(self):
    print("Connect")
    self.transport.write(b"hello, world!")

  def send_message(self, data):
    self.transport.write(data)
    
  def dataReceived(self, data):
    print("Server said:", data)

    # self.add_data(data[0], data[1])
    
  def connectionLost(self, reason):
    print("connection lost")

  def add_data(self, name, data):
    try:
      self.queueData[name].put(data)
    except queue.Full:
      pass
  
  def get_data(self, name):
    try:
      self.queueData[name].get_nowait()
    except queue.Empty:
      return None