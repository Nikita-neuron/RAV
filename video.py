# import serial
import cv2
import socket
import pickle
#import struct

# C:\Users\undeg\AppData\Local\Microsoft\WindowsApps

def get_cmd_args():
    import argparse
    parser = argparse.ArgumentParser('Raspberry server')
    parser.add_argument('pc_ip')
    return parser.parse_args()


client = socket.socket()
client.connect((get_cmd_args().pc_ip, 1080))
print('connected!')

cam = cv2.VideoCapture(0)

# data = b""
# payload_size = struct.calcsize(">L")
# print("payload_size: {}".format(payload_size))

# encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


while True:
    ret, frame = cam.read()
    frame = cv2.resize(frame, (320, 240))

    if frame is not None:
        cv2.imshow('frame', frame)

        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        server.sendall(struct.pack(">L", size) + data)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
client.close()
