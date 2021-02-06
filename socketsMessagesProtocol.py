import struct
import socket
import pickle

class MessagesProtocol:
    def __init__(self, socket):
        self.socket = socket
        self.data = b""
        self.payload_size = struct.calcsize(">L")

    def receive_message(self, bytes):

        mess = ""
        while len(self.data) < self.payload_size:
            try:
                mess = self.socket.recv(bytes)
            except:
                return None
            if len(mess) == 0:
                return None
            self.data += mess

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        mess = ""
        while len(self.data) < msg_size:
            try:
                mess = self.socket.recv(bytes)
            except:
                return None
            if len(mess) == 0:
                return None
            self.data += mess
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        
        return frame

    def send_message(self, data):
        data = pickle.dumps(data, 0)
        size = len(data)

        self.socket.sendall(struct.pack(">L", size) + data)