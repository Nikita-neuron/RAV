from twisted.internet import protocol
import cv2
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class RaspberryPIProtocol(protocol.Protocol):

  def __init__(self, queueData, name):
    self.unpacker = msgpack.Unpacker()
    self.queueData = queueData
    self.name = name

  def connectionMade(self):
    print("Connect")

    hello = {
      "type": "client_connect",
      "name": self.name
    }

    self.send_message(hello)

  def send_message(self, data):
    if self.transport is not None:
      msgpack.pack(data, self.transport)
    
  def dataReceived(self, data):
    self.unpacker.feed(data)
    for msg in self.unpacker:
      self.add_data(msg["type"], msg["data"])
    
  def connectionLost(self, reason):
    print("connection lost")

  def add_data(self, name, data):
    # print("put")
    # print(data)
    # self.queueData[name] = data
    # print("done")
    try:
      # print("put")
      # print(self.queueData[name].full())
      # if self.queueData[name].qsize() < 20:
        # self.queueData[name].put_nowait(data)
      # print("put done")
      self.queueData[name].put_nowait(data)
      # print("done")
    except queue.Full:
      pass
  
  def get_data(self, name):
    try:
      return self.queueData[name].get_nowait()
    except queue.Empty:
      return None