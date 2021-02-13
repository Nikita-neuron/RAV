import threading
import queue
import cv2

class PlayRaspberryVideo(threading.Thread):
  def __init__(self):
    super().__init__()

    self.frames = queue.Queue(2)

    self._stopped = False

  def run(self):
    while not self._stopped:
      frame = self.get_frame()

      if frame is not None:
        cv2.imshow("frame", frame)

        cv2.waitKey(1)

  def add_frame(self, frame):
    try:
      self.frames.put(frame, block=False)
    except queue.Full:
      pass

  def get_frame(self):
    try:
      self.frames.get_nowait()
    except queue.Empty:
      return None