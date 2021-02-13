from twisted.internet import reactor, protocol
import threading

import RaspberryPIMotorsFactory

class RaspberryPIMotorsServer(threading.Thread):
  def __init__(self, server_ip):
    super().__init__()

    self.server_ip = server_ip

    self.raspberryPIMotorsFactory = RaspberryPIMotorsFactory.RaspberryPIMotorsFactory()

  def run(self):
    reactor.connectTCP(self.server_ip, 8000, self.raspberryPIMotorsFactory)
    reactor.run(installSignalHandlers=False)

  def get_data(self, name):
    return self.raspberryPIMotorsFactory.get_data(name)

  def send_message(self, data):
    self.raspberryPIMotorsFactory.send_message(data)
