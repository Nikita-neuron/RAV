import socket
import cv2
import time
import queue
import threading

from ServerConnect import ServerConnect
from RaspberryVideo import RaspberryVideo

# https://rtcbot.readthedocs.io/en/latest/arduino.html


def main():
    video_frames = queue.Queue(4)
    serverThread = ServerConnect(video_frames)
    serverThread.start()

    raspberryVideo = RaspberryVideo(video_frames)
    raspberryVideo.start()

    while True:
        time.sleep(1)
        # command = input("Command: ")
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
