import threading
from twisted.internet import reactor, protocol

import ServerPCFactory

class PCServer(threading.Thread):
  def __init__(self, queueDataMotors, queueDataSensors):
    super().__init__()

    self.serverPCFactory = ServerPCFactory.ServerPCFactory(queueDataMotors, queueDataSensors)

  def run(self):
    print("listen...")
    reactor.listenTCP(8000, self.serverPCFactory)
    reactor.run(installSignalHandlers=False)

  def send_motors_raspberry(self, data):
    self.serverPCFactory.send_motors_raspberry(data)
