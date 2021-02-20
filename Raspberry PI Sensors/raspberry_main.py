import ctypes
import sys
import serial
# import pyaudio
sys.path.append("..")
from ctypes import *
import queue
import msgpack

from systemData import SystemData
from raspberryTwisted import raspberryPIClient

# from Sound import soundPlayThread, soundRecordThread

def get_server_ip_port():
  return sys.argv[1], sys.argv[2]

def connect_arduino():
  ser = serial.Serial("/dev/ttyACM0", 9600)  # ls /dev/tty*
  ser.baudrate = 9600

  return ser

# def get_sound_device():
#   p = pyaudio.PyAudio()
#   print("----------------------default record device list---------------------")
#   print(p.get_default_input_device_info())
#   print(p.get_default_output_device_info())
#   print("---------------------------------------------------------------------")
#   print("----------------------record device list---------------------")
#   info = p.get_host_api_info_by_index(0)
#   numdevices = info.get('deviceCount')
#   for i in range(0, numdevices):
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#       print("Input Device id ", i, " - ", 
#       p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", 
#       p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'), 
#       "RATE: ", p.get_device_info_by_host_api_device_index(0, i).get('defaultSampleRate'))

#   print("-------------------------------------------------------------")
#   p.terminate()


class UltrasonicStructure(Structure):
	_pack_ = 1
	_fields_ = [
		("dis1", c_int16), ("dis2", c_int16), 
		("dis3", c_int16), ("dis4", c_int16), 
		("dis5", c_int16)
	]

def get_data(queueData, name):
  try:
    return queueData[name].get_nowait()
  except queue.Empty:
    return None

def main():
	systemData = SystemData()

	queueData = {
		"soundsPC":     queue.Queue(2),
		"ultrasonic":  queue.Queue(2)
	}
	name = "raspberryPISensors"
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

	raspberryPIMotorsServer.start()

	i = 0


	while True:

		if i%10000 == 0:
			system_data = systemData.get_system_data()

			# raspberryPIMotorsServer.send_message({
			#   "type": "systemData", 
			#   "data": system_data
			# })
			i += 1

		# print("get frame")
		# frame = raspberryVideo.get_video_frames()
		# print("hhh")
		# # print("send")
		# if frame is not None:
		#   raspberryPIMotorsServer.send_message({
		#     "type": "frames",
		#     "data": frame
		#   })
		# print("done")

		
		# sound = soundRecord.get_sound()
		# if sound is not None:
		# # print(sound)
		# 	soundPlay.add_sound(sound)
		# raspberryPIMotorsServer.send_message({
		#   "type": "soundsRaspberry", 
		#   "data": sound
		# })

		# sound_pc = get_data(queueData, "soundsPC")
		# if sound_pc is not None:
		#   # print(sound_pc)
		#   soundPlay.add_sound(sound_pc)

		serial_data = arduino.read(10)

		ultrasonicData = UltrasonicStructure.from_buffer_copy(serial_data)

		ultrasonicData = [
			ultrasonicData.dis1,
			ultrasonicData.dis2,
			ultrasonicData.dis3,
			ultrasonicData.dis4,
			ultrasonicData.dis5,
		]
		print(ultrasonicData)

		raspberryPIMotorsServer.send_message({
		  "type": "ultrasonic", 
		  "data": ultrasonicData
		})
main()
