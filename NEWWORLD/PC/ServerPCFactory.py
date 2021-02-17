from twisted.internet import protocol
import queue

import PCMotorsProtocol

class ServerPCFactory(protocol.Factory):
    def __init__(self, queueData):
        self.raspberryPIMotorsProtocol = PCMotorsProtocol.PCMotorsProtocol(queueData)

    def get_data(self, name):
        return self.raspberryPIMotorsProtocol.get_data(name)

    def send_motors_raspberry(self, data):
        self.raspberryPIMotorsProtocol.sendMessage(data)

    def buildProtocol(self, addr):
        if addr.host == "192.168.1.60":
            return self.raspberryPIMotorsProtocol
