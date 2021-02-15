import pc.PCServer

# from Sound import SoundPlayThread, SoundRecordThread
from pc.PlayRaspberryVideo import PlayRaspberryVideo

def main():
  pcServerRaspberry = pc.PCServer.PCServer()
  pcServerRaspberry.start()

  '''
  soundRecordThread = SoundRecordThread.SoundRecordThread()
  soundPlayThread = SoundPlayThread.SoundPlayThread()

  soundRecordThread.start()
  soundPlayThread.start()
  '''
  playRaspberryVideo = PlayRaspberryVideo()
  playRaspberryVideo.start()

  while True:
    sys_data = pcServerRaspberry.get_data("systemData")
    frame = pcServerRaspberry.get_data("frames")
    sounds_raspberry = pcServerRaspberry.get_data("soundsRaspberry")

    motors = [1, 1]
    pcServerRaspberry.send_motors_raspberry(["motorsSpeed", motors])
    '''
    if sounds_raspberry is not None:
      soundPlayThread.add_sound(sounds_raspberry)

    sounds_pc = soundRecordThread.get_sound()
    if sounds_pc is not None:
      pcServerRaspberry.send_massage(["soundsPC", sounds_pc])
    '''
    if frame is not None:
      # print("res")
      playRaspberryVideo.add_frame(frame)

    # if sys_data is not None:
      # print(sys_data)
if __name__ == '__main__':
  main()
