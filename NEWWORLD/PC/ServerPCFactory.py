from twisted.internet import protocol
import queue

import PCMotorsProtocol

class ServerPCFactory(protocol.Factory):
    def __init__(self):
        self.raspberryPIMotorsProtocol = PCMotorsProtocol.PCMotorsProtocol()

    def get_data(self, name):
        self.raspberryPIMotorsProtocol.get_data(name)

    # def get_video_frames(self):
    #     return self.raspberryPIMotorsProtocol.get_video_frames()

    # def get_sys_data(self):
    #     return self.raspberryPIMotorsProtocol.get_sys_data()

    # def get_sound_raspberry(self):
    #     return self.raspberryPIMotorsProtocol.get_sound_raspberry()

    def send_motors_raspberry(self, data):
        self.raspberryPIMotorsProtocol.sendMessage(data)

    def buildProtocol(self, addr):
        if addr.host == "192.168.1.37":
            return self.raspberryPIMotorsProtocol
