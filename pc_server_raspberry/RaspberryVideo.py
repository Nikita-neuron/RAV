import threading
import queue
import cv2

class RaspberryVideo(threading.Thread):
  def __init__(self, video_frames):
    super().__init__()

    self.video_frames = video_frames

    self._stopped = False

  def run(self):
    while not self._stopped:

        frame = self.get_video_frames()

        if frame is not None:
          cv2.imshow("frame", frame)
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