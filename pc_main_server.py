import socket
import cv2
import time
import queue
import numpy as np
import threading

from ServerConnect import ServerConnect
from RaspberryVideo import RaspberryVideo

# https://rtcbot.readthedocs.io/en/latest/arduino.html

# https://habr.com/ru/post/513966/
# https://webdevblog.ru/logging-v-python/

import service_interface as interface


class WebServerReceiver(threading.Thread):
	def __init__(self):
		super().__init__()
		self.key_state = {
			'w': False,
			'a': False,
			's': False,
			'd': False
		}
	def run(self):
		import service_interface as interface
		webserver = interface.root['webserver']
		while 'keyboard' not in webserver:
			pass
		keyboard_stream = webserver['keyboard']
		while True:
			print('RECV')
			self.key_state = keyboard_stream.recv()
	def get_command(self):
		keys = self.key_state
		command = np.array([0, 0])
		if keys['w']:
			command += [75, 75]
		if keys['s']:
			command -= [75, 75]
		return command

def service_main():
	main()

def main():
	video_frames = queue.Queue(4)
	serverThread = ServerConnect(video_frames)
	serverThread.start()

	raspberryVideo = RaspberryVideo(video_frames)
	raspberryVideo.start()

	webserver_receiver = WebServerReceiver()
	webserver_receiver.start()

	while True:
		# time.sleep(1)
		# command = input("Command: ")

		# sys_data = serverThread.get_sys_data()

		# if sys_data is not None:
		#     print("CPU: " + str(sys_data["cpu"]))
		#     print("Memory: " + str(sys_data["memory"]))
		#     print("Disk: " + str(sys_data["disk"]))
		#     print("Temperatyre: " + str(sys_data["temperature"]))

		data = serverThread.get_ultrasonic_data()
		print(data)

		# command = "100 100"
		
		
		# if command == "end":
		# 	serverThread.stop()
		# 	break

		try:
			# r, l = map(int, command.split())
			motors = webserver_receiver.get_command()
			# motors = [1, 1]
			print('MOTORS', motors)
			serverThread.set_motors_speed(motors)
		except:
			print("Your command is incorrect")
			print("Exemple (r, l): 50 50")

if __name__ == "__main__":
	main()
