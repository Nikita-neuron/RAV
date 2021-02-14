from twisted.internet import protocol
import cv2
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class RaspberryPIMotorsProtocol(protocol.Protocol):

  def __init__(self):
    self.unpacker = msgpack.Unpacker()
    self.queueData = {
      "soundsPC":     queue.Queue(2),
      "motorsSpeed":  queue.Queue(1)
    }

  def connectionMade(self):
    print("Connect")
    # self.transport.write(b"hello, world!")

  def send_message(self, data):
    if self.transport is not None:
      # print()
      # self.transport.write(b"ggg")
      print("sending")
      msgpack.pack(data, self.transport)
      print("done")
      # self.transport.write(data)
      # msgpack.pack(["frames", [1,2,3]], self.transport)
    
  def dataReceived(self, data):
    self.unpacker.feed(data)
    for msg in self.unpacker:
      self.add_data(msg[0], msg[1])
    
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