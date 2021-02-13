from twisted.internet import reactor, protocol

import RaspberryPIMotorsProtocol

class RaspberryPIMotorsFactory(protocol.ClientFactory):

  def __init__(self):
    self.raspberryPIMotorsProtocol = RaspberryPIMotorsProtocol.RaspberryPIMotorsProtocol()

  def buildProtocol(self, addr):
    return self.raspberryPIMotorsProtocol

  def send_message(self, data):
    self.raspberryPIMotorsProtocol.send_message(data)
  
  def get_data(self, name):
    return self.raspberryPIMotorsProtocol.get_data(name)

  def clientConnectionFailed(self, connector, reason):
    print("Connection failed, ", reason)
    
  def clientConnectionLost(self, connector, reason):
    print("Connection lost ", reason)