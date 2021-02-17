from twisted.internet import protocol
import cv2
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

# sudo apt-get install telnetd

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
    try:
      self.queueData[name].put_nowait(data)
    except queue.Full:
      pass
