import socket
import cv2
import time

from ServerConnect import ServerConnect

# https://rtcbot.readthedocs.io/en/latest/arduino.html

def main():
    serverThread = ServerConnect()
    serverThread.start()
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

        # try:
        #     frame = serverThread.raspberryPIMotorsThread.get_video_frames()

        #     if frame is not None:
        #         cv2.imshow("frame", frame)
        # except:
        #     pass

        cv2.waitKey(1)

if __name__ == "__main__":
    main()
