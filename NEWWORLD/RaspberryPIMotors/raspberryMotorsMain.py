import sys
import serial
import pyaudio
sys.path.append("..")
from ctypes import *
import queue
import msgpack

from systemData import SystemData
from raspberryVideo import RaspberryVideo
from raspberryTwisted import raspberryPIClient

from Sound import soundPlayThread, soundRecordThread

def get_server_ip_port():
  return sys.argv[1], sys.argv[2]

def connect_arduino():
  ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
  ser.baudrate = 9600

  return ser

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


class MotorsStructure(Structure):
  _pack_ = 1
  _fields_ = [("r", c_int8), ("l", c_int8)]

def get_data(queueData, name):
  # print("get")
  # data = queueData[name]
  # print("get done")
  # return data
  try:
    # print("get")
    return queueData[name].get_nowait()
  except queue.Empty:
    return None

def main():
  systemData = SystemData()

  queueData = {
    "soundsPC":     queue.Queue(2),
    "motorsSpeed":  queue.Queue(2)
  }
  name = "raspberryPIMotors"
  server_ip, server_port = get_server_ip_port()

  # get_sound_device()

  arduino = connect_arduino()

  # soundRecordThread = soundRecordThread.SoundRecordThread(INDEX=1, CHANELS=1)
  # soundPlayThread = soundPlayThread.SoundPlayThread()

  # soundRecordThread.start()
  # soundPlayThread.start()

  raspberryVideo = RaspberryVideo()
  raspberryVideo.start()

  raspberryPIMotorsServer = raspberryPIClient.RaspberryPIClient(
    server_ip,
    int(server_port), 
    queueData, 
    name
  )
  raspberryPIMotorsServer.start()

  while True:
    system_data = systemData.get_system_data()

    raspberryPIMotorsServer.send_message({
      "type": "systemData", 
      "data": system_data
    })

    frame = raspberryVideo.get_video_frames()
    if frame is not None:
      raspberryPIMotorsServer.send_message({
        "type": "frames",
        "data": frame
      })

    
    # sound = soundRecordThread.get_sound()
    # if sound is not None:
    #   raspberryPIMotorsServer.send_message({
    #     "type": "soundsRaspberry"ё, 
    #     "data": system_data
    #   })

    # sound_pc = get_data("soundsPC")
    # if sound_pc is not None:
    #   soundPlayThread.add_sound(sound_pc)
    
    motors = get_data(queueData, "motorsSpeed")
    # print("motors: ", motors)
    if motors is not None:
      print("from raspberry: ", motors)

      motors_arduino = MotorsStructure(motors[0], motors[1])

      # msgpack.pack(motors, arduino)
      arduino.write(string_at(byref(motors_arduino), sizeof(motors_arduino)))

      # try:
        # arduino.write(string_at(byref(motors_arduino), sizeof(motors_arduino)))
      # except:
        # pass

      # serial_data = arduino.read(2)

      # motors_from_arduino = MotorsStructure.from_buffer_copy(serial_data)
      # print("from arduino: ",motors_from_arduino.r)


if __name__ == '__main__':
  main()
