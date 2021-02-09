import socket
import cv2
import time
import queue
import threading

from ServerConnect import ServerConnect
from RaspberryVideo import RaspberryVideo

# https://rtcbot.readthedocs.io/en/latest/arduino.html

# https://habr.com/ru/post/513966/
# https://webdevblog.ru/logging-v-python/


def main():
	video_frames = queue.Queue(4)
	serverThread = ServerConnect(video_frames)
	serverThread.start()

	raspberryVideo = RaspberryVideo(video_frames)
	raspberryVideo.start()

	while True:
		time.sleep(1)
		# command = input("Command: ")

		# sys_data = serverThread.get_sys_data()

		# if sys_data is not None:
		#     print("CPU: " + str(sys_data["cpu"]))
		#     print("Memory: " + str(sys_data["memory"]))
		#     print("Disk: " + str(sys_data["disk"]))
		#     print("Temperatyre: " + str(sys_data["temperature"]))

		data = serverThread.get_ultrasonic_data()
		# print(data)

		command = "100 100"
		
		if command == "end":
			serverThread.stop()
			break

		try:
			r, l = map(int, command.split())
			motors = [r, l]
			serverThread.set_motors_speed(motors)
		except:
			print("Your command is incorrect")
			print("Exemple (r, l): 50 50")

if __name__ == "__main__":
	main()
