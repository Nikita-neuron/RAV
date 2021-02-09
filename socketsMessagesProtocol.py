import struct
import socket
import pickle

class MessagesProtocol:
    def __init__(self, socket):
        self.socket = socket
        self.data = b""
        self.payload_size = struct.calcsize(">L")

    def receive_message(self, bytes):
        # self.data = b""

        mess = ""
        while len(self.data) < self.payload_size:
            try:
                mess = self.socket.recv(bytes)
                self.data += mess
                # print(1)
            except:
                return "No connection"
            if len(mess) == 0:
                return "No connection"

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        mess = ""
        # print("t: " + str(msg_size))
        while len(self.data) < msg_size:
            try:
                mess = self.socket.recv(bytes)
                self.data += mess
                # print(2)
            except:
                return "No connection"
            if len(mess) == 0:
                return "No connection"
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        
        return frame

    def send_message(self, data):
        data = pickle.dumps(data, 0)
        # print("data: " + str(data))
        size = len(data)

        # print("y: " + "gggg")

        # print("size: " + str(size))
        try:
            self.socket.sendall(struct.pack(">L", size) + data)
        except:
            # print(9)
            pass