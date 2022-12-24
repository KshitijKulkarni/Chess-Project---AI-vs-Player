import ImageRecognition as IR
import cv2 as cv
import numpy as np

cv.namedWindow("Window", cv.WINDOW_NORMAL)

def OnTrackbarPosChange():
    print("Trackbar Position Changed")
#create 2 cv sliders
cv.createTrackbar("X", "Window", 30, 50, OnTrackbarPosChange)
cv.createTrackbar("Y", "Window", 30, 50, OnTrackbarPosChange)

while True:
    cv.imshow("Window", IR.GetCirclesInImage(cv.getTrackbarPos("X", "Window"), cv.getTrackbarPos("Y", "Window")))
    if cv.waitKey(1) == ord('q'):
        break