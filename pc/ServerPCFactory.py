from twisted.internet import protocol
import queue

import PCMotorsProtocol
import PCSensorsProtocol

class ServerPCFactory(protocol.Factory):
    def __init__(self, queueDataMotors, queueDataSensors):
        self.raspberryPIMotorsProtocol = PCMotorsProtocol.PCMotorsProtocol(queueDataMotors)
        self.raspberryPISensorsProtocol = PCSensorsProtocol.PCSensorsProtocol(queueDataSensors)

    def send_motors_raspberry(self, data):
        self.raspberryPIMotorsProtocol.sendMessage(data)

    def buildProtocol(self, addr):
        if addr.host == "172.20.234.161":
            return self.raspberryPIMotorsProtocol

        if addr.host == "172.20.234.171":
            return self.raspberryPISensorsProtocol
