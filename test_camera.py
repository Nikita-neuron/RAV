# import cv2

# camera = cv2.VideoCapture(0)
# while camera.isOpened():
#     _, img = camera.read()
#     cv2.imshow('img', img)
#     cv2.waitKey(1)
# print('Camera closed!')
# cv2.destroyAllWindows()
# camera.release()

def f():
    i = 0
    def g():
        i += 1
    g()
    return i

print(f())
