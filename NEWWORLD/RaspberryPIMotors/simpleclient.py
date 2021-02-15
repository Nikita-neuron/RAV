import RaspberryPIMotorsServer
import sys
import serial
# import pyaudio
from ctypes import *

from SystemData import SystemData
from RaspberryVideo import RaspberryVideo

# from Sound import SoundPlayThread, SoundRecordThread

def get_server_ip():
  return sys.argv[1]

def connect_arduino():
  ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
  ser.baudrate = 9600

  return ser
'''
def get_sound_device():
  p = pyaudio.PyAudio()
  print("----------------------record device list---------------------")
  info = p.get_host_api_info_by_index(0)
  numdevices = info.get('deviceCount')
  for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
      print("Input Device id ", i, " - ", 
        p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", 
        p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'), " RATE: ", 
        p.get_device_info_by_host_api_device_index(0, i).get('defaultSampleRate')
      )

  print("-------------------------------------------------------------")
  p.terminate()
'''

def main():
  systemData = SystemData()

  # get_sound_device()

  # arduino = connect_arduino()

  # soundRecordThread = SoundRecordThread.SoundRecordThread()
  # soundPlayThread = SoundPlayThread.SoundPlayThread()

  # soundRecordThread.start()
  # soundPlayThread.start()

  raspberryVideo = RaspberryVideo()
  raspberryVideo.start()

  raspberryPIMotorsServer = RaspberryPIMotorsServer.RaspberryPIMotorsServer(get_server_ip())
  raspberryPIMotorsServer.start()

  class MotorsStructure(Structure):
    _pack_ = 1
    _fields_ = [("r", c_int8), ("l", c_int8)]

  while True:
    system_data = systemData.get_system_data()

    # raspberryPIMotorsServer.send_message(["systemData", system_data])

    frame = raspberryVideo.get_video_frames()
    if frame is not None:
      raspberryPIMotorsServer.send_message(["frames", frame])

    '''
    sound = soundRecordThread.get_sound()
    if sound is not None:
      raspberryPIMotorsServer.send_message(["soundsRaspberry", system_data])

    sound_pc = raspberryPIMotorsServer.get_data("soundsPC")
    if sound_pc is not None:
      soundPlayThread.add_sound(sound_pc)
    '''
    motors = raspberryPIMotorsServer.get_data("motorsSpeed")
    if motors is not None:
      print(motors)

    # motors_arduino = MotorsStructure(motors[0], motors[1])

    # arduino.write(string_at(byref(motors_arduino), sizeof(motors_arduino)))

    # serial_data = arduino.read(2)

    # motors_from_arduino = MotorsStructure.from_buffer_copy(serial_data)
    # print(motors_from_arduino.r)


if __name__ == '__main__':
  main()
