import serial
import cv2
import socket
import pickle
import struct

server = None

#ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
#ser.baudrate = 9600

#motors_move = False

cam = cv2.VideoCapture(0)

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


def start_connect():
    global server
    sock = socket.socket()
    sock.bind(('', 1080))
    sock.listen(1)
    server, adr = sock.accept()

    print('connected: ', adr)


start_connect()
while True:
    ret, frame = cam.read()
    frame = cv2.resize(frame, (320, 240))

    if ret is False:
        server.send('end'.encode())
        print('end')
        break
    else:
        server.send('ok'.encode())
    
    if frame is not None:
        cv2.imshow('frame', frame)

        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        server.sendall(struct.pack(">L", size) + data)

    server_command = server.recv(1024).decode()

    #if motors_move:
        #ser.write(server_command.encode())

    #if server_command == 'v':
        #motors_move = True

    #if server_command == 't':
        #ser.write(server_command.encode())
        #server.close()
        #break
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
