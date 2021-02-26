import sys
import serial
# import pyaudio
sys.path.append("..")
from ctypes import *
import queue
import msgpack

from systemData import SystemData
# from raspberryVideo import RaspberryVideo
from raspberryTwisted import raspberryPIClient

# from Sound import soundPlayThread, soundRecordThread

def get_server_ip_port():
  return sys.argv[1], sys.argv[2]

def connect_arduino():
  ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
  ser.baudrate = 9600

  return ser

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


class MotorsStructure(Structure):
  _pack_ = 1
  _fields_ = [("r", c_int8), ("l", c_int8), ("p", c_int8)]

def get_data(queueData, name):
  try:
    return queueData[name].get_nowait()
  except queue.Empty:
    return None

def main():
  systemData = SystemData()

  queueData = {
    "soundsPC":     queue.Queue(20),
    "motorsSpeed":  queue.Queue(20)
  }
  name = "raspberryPIMotors"
  server_ip, server_port = get_server_ip_port()

  # get_sound_device()

  arduino = connect_arduino()

  raspberryPIMotorsServer = raspberryPIClient.RaspberryPIClient(
    server_ip,
    int(server_port), 
    queueData, 
    name
  )

  # soundRecord = soundRecordThread.SoundRecordThread(INDEX=2, CHANNELS=1, RATE=48000, 
  # DELAY_SECONDS=2, server=raspberryPIMotorsServer)
  # soundPlay = soundPlayThread.SoundPlayThread(CHANNELS=1, DELAY_SECONDS=2, server=raspberryPIMotorsServer,
  # INDEX=11)

  # soundRecord.start()
  # soundPlay.start()

  # raspberryVideo = RaspberryVideo(raspberryPIMotorsServer)
  # raspberryVideo.start()

  raspberryPIMotorsServer.start()

  i = 0

  while True:

    if i%10000 == 0:
      system_data = systemData.get_system_data()

      raspberryPIMotorsServer.send_message({
        "type": "systemData", 
        "data": system_data
      })
    i += 1

    # print("get frame")
    # frame = raspberryVideo.get_video_frames()
    # print("hhh")
    # print("send")
    # if frame is not None:
    #   raspberryPIMotorsServer.send_message({
    #     "type": "frames",
    #     "data": frame
    #   })
    # print("done")

    
    # sound = soundRecord.get_sound()
    # if sound is not None:
    #   # print(sound)
    #   soundPlay.add_sound(sound)
      # raspberryPIMotorsServer.send_message({
      #   "type": "soundsRaspberry", 
      #   "data": sound
      # })

    # sound_pc = get_data(queueData, "soundsPC")
    # if sound_pc is not None:
    #   # print(sound_pc)
    #   soundPlay.add_sound(sound_pc)
    
    motors = get_data(queueData, "motorsSpeed")
    if motors is not None:
      print("from raspberry: ", motors)

      motors_arduino = MotorsStructure(motors[0], motors[1], motors[2])

      arduino.write(string_at(byref(motors_arduino), sizeof(motors_arduino)))


if __name__ == '__main__':
  main()
