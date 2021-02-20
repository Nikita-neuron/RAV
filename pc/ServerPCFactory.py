from twisted.internet import protocol
import queue

import PCMotorsProtocol
import PCSensorsProtocol

class ServerPCFactory(protocol.Factory):
    def __init__(self, queueDataMotors, queueDataSensors, ip_raspberry_motors, ip_raspberry_sensors):
        self.ip_raspberry_motors = ip_raspberry_motors
        self.ip_raspberry_sensors = ip_raspberry_sensors
        self.raspberryPIMotorsProtocol = PCMotorsProtocol.PCMotorsProtocol(queueDataMotors)
        self.raspberryPISensorsProtocol = PCSensorsProtocol.PCSensorsProtocol(queueDataSensors)

    def send_motors_raspberry(self, data):
        self.raspberryPIMotorsProtocol.sendMessage(data)

    def buildProtocol(self, addr):
        if addr.host == self.ip_raspberry_motors:
            return self.raspberryPIMotorsProtocol

        if addr.host == self.ip_raspberry_sensors:
            return self.raspberryPISensorsProtocol
