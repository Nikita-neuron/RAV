import PCServer
import queue
import cv2
import pyaudio

from Sound import soundPlayThread, soundRecordThread
from PlayRaspberryVideo import PlayRaspberryVideo

def get_data(queueData, name):
  try:
    return queueData[name].get_nowait()
  except queue.Empty:
    return None

def get_sound_device():
    p = pyaudio.PyAudio()
    print("----------------------default record device list---------------------")
    print(p.get_default_input_device_info())
    print(p.get_default_output_device_info())
    print("---------------------------------------------------------------------")
    print("----------------------record device list---------------------")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", 
            p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", 
            p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'), 
            "RATE: ", p.get_device_info_by_host_api_device_index(0, i).get('defaultSampleRate'))

    print("-------------------------------------------------------------")
    p.terminate()

def main():
  # get_sound_device()

  queueData = {
    "frames":           queue.Queue(20),
    "soundsRaspberry":  queue.Queue(1),
    "systemData":       queue.Queue(20)
  }

  pcServerRaspberry = PCServer.PCServer(queueData)
  pcServerRaspberry.start()

  soundRecord = soundRecordThread.SoundRecordThread(DELAY_SECONDS=1)
  soundPlay = soundPlayThread.SoundPlayThread(CHANNELS=1, DELAY_SECONDS=1)

  soundRecord.start()
  soundPlay.start()
  
  playRaspberryVideo = PlayRaspberryVideo()
  playRaspberryVideo.start()

  pult = cv2.imread(r"pc\pult.jpg")
  pult = cv2.resize(pult, (500, 500))
  cv2.imshow("pult", pult)

  while True:
    sys_data = get_data(queueData, "systemData")
    frame = get_data(queueData, "frames")
    sounds_raspberry = get_data(queueData, "soundsRaspberry")
    # print(sounds_raspberry)

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
      soundPlay.add_sound(sounds_raspberry)

    # sounds_pc = soundRecord.get_sound()
    # if sounds_pc is not None:
    #   # print(sounds_pc)
    #   pcServerRaspberry.send_motors_raspberry({
    #     "type": "soundsPC", 
    #     "data": sounds_pc
    #   })
    
    # if frame is not None:
    #   # print("res")
    #   playRaspberryVideo.add_frame(frame)

    # if sys_data is not None:
      # print(sys_data)
if __name__ == '__main__':
  main()
