import threading
import queue
import socket
import cv2

from socketsMessagesProtocol import MessagesProtocol

class ServerThread(threading.Thread):
  def __init__(self, server):
    super().__init__()

    self.server = server
    self.motors_speed = queue.Queue(1)
    self._stopped = False

    self.messagesProtocol = MessagesProtocol(server)

    self.cam = cv2.VideoCapture(0)

    self.count_zero_speed = 0

  def get_video(self):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    ret, frame = self.cam.read()

    if ret is True:
      frame = cv2.resize(frame, (320, 240))
      result, frame = cv2.imencode('.jpg', frame, encode_param)

      return frame
    else:
      return None
    
  def run(self):
    while not self._stopped:
      frame = self.get_video()

      if frame is None:
        self.messagesProtocol.send_message('end')
        print('end')
        break
            
      self.messagesProtocol.send_message("OK")
      self.messagesProtocol.send_message(frame)

      motors = self.messagesProtocol.receive_message(16)

      if motors[0] != 0 or motors[1] != 0:
        self.count_zero_speed = 0

      if motors[0] == 0 and motors[1] == 0:
        self.count_zero_speed += 1 

      if motors is not None:
        self.add_motors_speed(motors)
            
  def add_motors_speed(self, motors):
    # добавление скорости моторов в очередь
    try:
      if self.count_zero_speed < 2:
        self.motors_speed.put(motors, block=False)
    except queue.Full:
      pass

  def get_motors_speed(self):
    # получение скорости моторов из очереди
    try:
      motors = self.motors_speed.get_nowait()
      return motors
    except queue.Empty:
      return [0, 0]

  def stop(self):
    self._stopped = True
