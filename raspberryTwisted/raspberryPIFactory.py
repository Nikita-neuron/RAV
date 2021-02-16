from twisted.internet import reactor, protocol

from raspberryTwisted.raspberryPIProtocol import RaspberryPIProtocol

class RaspberryPIFactory(protocol.ClientFactory):

  def __init__(self, queueData, name):
    self.raspberryPIProtocol = RaspberryPIProtocol(queueData, name)

  def buildProtocol(self, addr):
    return self.raspberryPIProtocol

  def send_message(self, data):
    self.raspberryPIProtocol.send_message(data)
  
  def get_data(self, name):
    return self.raspberryPIProtocol.get_data(name)

  def clientConnectionFailed(self, connector, reason):
    print("Connection failed, ", reason)
    
  def clientConnectionLost(self, connector, reason):
    print("Connection lost ", reason)