from twisted.internet import reactor, protocol
import queue


class RaspberryMotors(protocol.Protocol):
    def __init__(self):
        super().__init__()

        self._stopped = False

        self.video_frames = queue.Queue(2)
        self.motors_speed = queue.Queue(2)

        self.sounds_raspberry = queue.Queue(2)
        self.sounds_pc = queue.Queue(2)

        self.system_data = queue.Queue(2)

    def send(self, data):
        self.transport.write()

    def connectionMade(self):
        self.transport.write(b"Hello")
    
    def dataReceived(self, data):
        print("from raspberry: ", data)

    def sendMessage(self, msg):
        self.transport.write(msg)

    def add_video_frames(self, frame):
        # добавление кадров в очередь
        try:
            self.video_frames.put(frame, block=False)
        except queue.Full:
            pass

    def get_video_frames(self):
        # получение кадров из очереди
        try:
            frame = self.video_frames.get_nowait()
            return frame
        except queue.Empty:
            return None

    def add_motors_speed(self, motors):
        # добавдение скорости моторов в очередь
        try:
            self.motors_speed.put(motors, block=False)
        except queue.Full:
            pass

    def get_motors_speed(self):
        # получение скорости моторов из очереди
        motors = [0, 0]
        try:
            motors = self.motors_speed.get_nowait()
        except queue.Empty:
            pass

        return motors

    def add_system_data(self, system_data):
        try:
            self.system_data.put(system_data)
        except queue.Full:
            pass

    def get_sys_data(self):
        try:
            return self.system_data.get_nowait()
        except queue.Empty:
            return None

    def get_sound_raspberry(self):
        try:
            return self.sounds_raspberry.get_nowait()
        except:
            return None

    def add_sound_pc(self, sound):
        try:
            self.sounds_pc.put(sound)
        except queue.Full:
            pass

    def print(self, data):
        print("")
        print("[RASPBERRY PI MOTORS]: "+ str(data))

    def stop(self):
        self._stopped = True

class Factory(protocol.Factory):
    def buildProtocol(self, addr):
        if addr.host == "192.168.1.60":
            self.motors = RaspberryMotors()
            return self.motors


def main():
    factory = Factory()
    factory.protocol = 
    print("listen...")
    reactor.listenTCP(8000, factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
