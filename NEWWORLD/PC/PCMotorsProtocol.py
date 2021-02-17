from twisted.internet import protocol
import queue
import msgpack
import msgpack_numpy
import time
msgpack_numpy.patch()


class PCMotorsProtocol(protocol.Protocol):
  def __init__(self, queueDta):

    self.unpacker = msgpack.Unpacker()

    self.queueData = queueDta

  def connectionMade(self):
    print("Connect")
    
  def dataReceived(self, data):
    # получение сообщений от распберри
    self.unpacker.feed(data)
    for msg in self.unpacker:
      # print("data recv")
      if msg["type"] == "client_connect":
        print("connect to raspberry")
      else:
        self.add_data(msg["type"], msg["data"])
      # print("done")

  def sendMessage(self, data):
    # отправка сообщений на распберри
    if self.transport is not None:
      # print("sending")
      msgpack.pack(data, self.transport)
      # print("done")

  def add_data(self, name, data):
    try:
      self.queueData[name].put(data, block=False)
    except queue.Full:
      pass

  def get_data(self, name):
    try:
      return self.queueData[name].get_nowait()
    except queue.Empty:
      return None
  
  def print(self, data):
    print("")
    print("[RASPBERRY PI MOTORS]: ", data)
