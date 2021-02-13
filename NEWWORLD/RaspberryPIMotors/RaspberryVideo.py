import threading
import queue
import cv2

class RaspberryVideo(threading.Thread):
  def __init__(self):
    super().__init__()

    self.video_frames = queue.Queue(2)

    self.cam = cv2.VideoCapture(0)

    self._stopped = False

  def run(self):
    while not self._stopped:
      encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

      ret, frame = self.cam.read()

      if ret is True:
        frame = cv2.resize(frame, (320, 240))
        # print("size: " + str(len(frame)) + " : " + str(len(frame[0])))

        # frame_numpy = np.array(frame)
        # frame_ctype = frame_numpy.ctypes.data_as(POINTER(c_long))
        # print(frame_ctype)

        # print(frame_ctype)

        self.add_video_frames(frame)

        # result, frame = cv2.imencode('.jpg', frame, encode_param)
      cv2.waitKey(1)

  def add_video_frames(self, frame):
    # добавление кадров в очередь
    try:
      self.video_frames.put(frame, block=False)
    except queue.Full:
      pass

  def get_video_frames(self):
    # получение видео с распберри
    try:
      frame = self.video_frames.get_nowait()
      return frame
    except queue.Empty:
      return None