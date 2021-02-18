import cv2

camera = cv2.VideoCapture(0)
while camera.isOpened():
    _, img = camera.read()
    print('img', _)
    # cv2.imshow('img', img)
    # cv2.waitKey(1)
print('Camera closed!')
# cv2.destroyAllWindows()
camera.release()
