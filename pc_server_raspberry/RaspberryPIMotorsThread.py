import threading
import queue
import cv2
import socket

from socketsMessagesProtocol import MessagesProtocol

class RaspberryPIMotorsThread(threading.Thread):
  def __init__(self, raspberry, video_frames):
    super().__init__()

    self._stopped = False
    self.raspberry = raspberry

    self.video_frames = video_frames
    self.motors_speed = queue.Queue(2)

    self.system_data = queue.Queue(2)

    self.messagesProtocol = MessagesProtocol(self.raspberry)

  def run(self):
    self.print("Connection successful")
    while not self._stopped:
      try:
        message = self.messagesProtocol.receive_message(16)
      except:
        break

      if message == 'end' or message is None:
        break
    
      # self.get_video()
              
      motors = self.get_motors_speed()

      self.messagesProtocol.send_message(motors)

      # sys_data = self.messagesProtocol.receive_message(16)

      # if sys_data != "No system data":
        # self.add_system_data(sys_data)
      
    self.print("disconnect Raspberry PI Motors")
    self.stop()
    self.raspberry.close()
    cv2.destroyAllWindows()

  def get_video(self):
    # получение видео от распберри
    frame = self.messagesProtocol.receive_message(16384)

    if frame is not None:

      frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
      frame = cv2.resize(frame, (320, 240))

      self.add_video_frames(frame)
    else:
      self.print("No frame")

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

  def print(self, data):
    print("")
    print("[RASPBERRY PI MOTORS]: "+ str(data))

  def stop(self):
    self._stopped = True