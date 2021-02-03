import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib

def start_connect():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 1080))
    sock.listen(1)
    server, adr = sock.accept()

    print('connected: ', adr)
    return server



# def setup_gui()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("video.avi", fourcc, 9.0, (320, 240))


server = start_connect()
while True:
    
    mess = client.recv(2)
    print(mess)
    if mess == b'en':
        break
    while len(data) < payload_size:
        data += client.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")  # получение изображения
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame, (320, 240))

    cv2.imshow('frame', frame)
    out.write(frame)

    if cv2.waitKey(1) == ord('q'):
        break
    

    '''
    v = input("Print command: ")
    if v == 'motors':
        v = 'v'
        server.send(v.encode())

    if v == 'w':
        # вперёд
        server.send(v.encode())
    elif v == 's':
        # назад
        server.send(v.encode())
    elif v == 'f':
        # стоп
        server.send(v.encode())
    if v == 'd':
        # вправо
        server.send(v.encode())
    elif v == 'a':
        # налево
        server.send(v.encode())

    if v == "stop":
        server.send('t'.encode())
        break
    '''
server.close()
out.release()
cv2.destroyAllWindows()
