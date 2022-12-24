import cv2 as cv
from cv2 import VideoCapture

cap = VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv.imshow("Camera feed",frame)
    if cv.waitKey(1) == "q":
        break

cap.release()
cv.destroyAllWindows()