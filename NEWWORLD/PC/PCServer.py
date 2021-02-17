import threading
from twisted.internet import reactor, protocol

import ServerPCFactory

class PCServer(threading.Thread):
  def __init__(self, queueData):
    super().__init__()

    self.serverPCFactory = ServerPCFactory.ServerPCFactory(queueData)

  def run(self):
    print("listen...")
    reactor.listenTCP(8000, self.serverPCFactory)
    reactor.run(installSignalHandlers=False)

  def send_motors_raspberry(self, data):
    self.serverPCFactory.send_motors_raspberry(data)

  def get_data(self, name):
    return self.serverPCFactory.get_data(name)
