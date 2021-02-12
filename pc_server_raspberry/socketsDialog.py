import socket

class SocketsDialog:
    def __init__(self, socket):
        self.socket = socket
        self._stopped = False

    def receive_message(self):
        data = self.socket.recv(1024)
        req = b''
        self.socket.settimeout(0.1)
        while data:
            req += data
            try:
                data = self.socket.recv(1024)
            except socket.error:
                break

        return req

    def send_message(self, data):
        self.socket.send(data)
