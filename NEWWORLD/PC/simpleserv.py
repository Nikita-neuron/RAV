import PCServer
import queue
import cv2

from Sound import SoundPlayThread, SoundRecordThread
from PlayRaspberryVideo import PlayRaspberryVideo

def get_data(queueData, name):
  try:
    return queueData[name].get_nowait()
  except queue.Empty:
    return None

def main():

  queueData = {
    "frames":           queue.Queue(20),
    "soundsRaspberry":  queue.Queue(20),
    "systemData":       queue.Queue(20)
  }

  pcServerRaspberry = PCServer.PCServer(queueData)
  pcServerRaspberry.start()

  soundRecordThread = SoundRecordThread.SoundRecordThread()
  soundPlayThread = SoundPlayThread.SoundPlayThread()

  soundRecordThread.start()
  soundPlayThread.start()
  
  playRaspberryVideo = PlayRaspberryVideo()
  playRaspberryVideo.start()

  pult = cv2.imread(r"newworld\pc\pult.jpg")
  pult = cv2.resize(pult, (500, 500))
  cv2.imshow("pult", pult)

  while True:
    sys_data = get_data(queueData, "systemData")
    frame = get_data(queueData, "frames")
    sounds_raspberry = get_data(queueData, "soundsRaspberry")

    motors = [0, 0]
    # key = "k"

    key = cv2.waitKey(100)

    if key == ord("w"):
      motors = [80, 80]

    if key == ord("s"):
      motors = [-80, -80]

    if key == ord("d"):
      motors = [-80, 80]

    if key == ord("a"):
      motors = [80, -80]

    # print(motors)

    pcServerRaspberry.send_motors_raspberry({
      "type": "motorsSpeed", 
      "data": motors
    })
    
    if sounds_raspberry is not None:
      soundPlayThread.add_sound(sounds_raspberry)

    sounds_pc = soundRecordThread.get_sound()
    if sounds_pc is not None:
      pcServerRaspberry.send_motors_raspberry({
        "type": "soundsPC", 
        "data": sounds_pc
      })
    
    if frame is not None:
      # print("res")
      playRaspberryVideo.add_frame(frame)

    # if sys_data is not None:
      # print(sys_data)
if __name__ == '__main__':
  main()
