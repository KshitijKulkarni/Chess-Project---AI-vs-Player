from multiprocessing import Event
import string
import time
from cv2 import circle
import numpy as np
import cv2 as cv
import os

cap = cv.VideoCapture(0)

#Make window resizable
cv.namedWindow("Window", cv.WINDOW_NORMAL)
global counter
counter = 0
plainmat = np.zeros((384, 836), np.float32)

def WriteLocation(index, x, y):
    file = open("Data.txt", "a")
    file.write("\n"+str(int(x/2))+","+str(int(y/2)))
    file.close()

def AddPoint(event, x, y, flags, param):
    global counter
    if event == cv.EVENT_LBUTTONDBLCLK:
        WriteLocation(counter, x, y)
        counter +=1

cv.setMouseCallback('Window',AddPoint)

while counter < 4:
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    frame = cv.resize(frame,(2*width, 2*height), interpolation = cv.INTER_LINEAR)
    cv.imshow("Window", frame)
    if cv.waitKey(1) == ord('q'):
        time.sleep(1)
        break


cv.destroyAllWindows()