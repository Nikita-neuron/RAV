from twisted.internet.protocol import ReconnectingClientFactory

from raspberryTwisted.raspberryPIProtocol import RaspberryPIProtocol

class RaspberryPIFactory(ReconnectingClientFactory):

  def __init__(self, queueData, name):
    self.raspberryPIProtocol = RaspberryPIProtocol(queueData, name)

  def buildProtocol(self, addr):
    # self.resetDelay()
    return self.raspberryPIProtocol

  def send_message(self, data):
    self.raspberryPIProtocol.send_message(data)

  def clientConnectionFailed(self, connector, reason):
    print("Connection failed, ", reason)
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
    
  def clientConnectionLost(self, connector, reason):
    print("Connection lost ", reason)
    ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)