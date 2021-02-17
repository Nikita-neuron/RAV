from twisted.internet import reactor, protocol
import threading

from raspberryTwisted.raspberryPIFactory import RaspberryPIFactory

class RaspberryPIClient(threading.Thread):
  def __init__(self, server_ip, server_port, queueData, name):
    super().__init__()

    self.server_ip = server_ip
    self.server_port = server_port

    self.raspberryPIFactory = RaspberryPIFactory(queueData, name)

  def run(self):
    print('connecting to', self.server_ip, self.server_port)
    reactor.connectTCP(self.server_ip, self.server_port, self.raspberryPIFactory)
    reactor.run(installSignalHandlers=False)

  def send_message(self, data):
    self.raspberryPIFactory.send_message(data)
