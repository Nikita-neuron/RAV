
import cv2
import time

while True:
    cap = cv2.VideoCapture('gavno.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)

    i = 0
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if i == 0:
            cv2.waitKey(10000)
        
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        i += 1


    cap.release()
    cv2.destroyAllWindows()

