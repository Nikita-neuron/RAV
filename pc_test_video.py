import socket
import sys
import cv2
import pickle
import numpy as np
import struct

from socketsMessagesProtocol import MessagesProtocol

# https://rtcbot.readthedocs.io/en/latest/arduino.html 

def start_connect():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 1080))
    print("listening...")
    sock.listen(1)
    server, adr = sock.accept()

    print('connected: ', adr)
    return server

def get_video(messagesProtocol):
    frame = messagesProtocol.receive_message(16384)

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame, (320, 240))

    cv2.imshow('frame', frame)


server = start_connect()
messagesProtocol = MessagesProtocol(server)

while True:
    
    message = messagesProtocol.receive_message(16)

    if message == 'end':
        break

    get_video(messagesProtocol)

    messagesProtocol.send_message("OK")

    if cv2.waitKey(1) == ord('q'):
        break
    
server.close()
cv2.destroyAllWindows()
