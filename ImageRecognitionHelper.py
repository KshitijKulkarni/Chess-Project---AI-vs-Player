from chess import Square
from cv2 import imshow
import ImageRecognition as imgutil
import cv2 as cv
import numpy as np
import time

#set refFrame to an empty image of size 300x300
ReferenceFrame = np.zeros((300,300,3), np.uint8)

def ShowRawInput():
    cv.waitKey(1)

def GetRefFrame():
    global ReferenceFrame
    ReferenceFrame = imgutil.StoreRefFrame()
    print("Reference Frame Captured")
    print("-----------------------------------------------------")
    cv.waitKey(1)


def Start():
    GetRefFrame()

def Close():
    imgutil.Close()

def CompFrame(reframe):
    global ReferenceFrame
    newRefFrame, Squares = imgutil.OnUserPlayed(reframe)
    ReferenceFrame = newRefFrame.copy()
    cv.waitKey(1)
    return Squares
    
def CompFrameDebug():
    global ReferenceFrame
    Output = CompFrame(ReferenceFrame)
    cv.waitKey(1)
    # cv.imshow("ImageViewer", ReferenceFrame)
    cv.waitKey(1)
    return Output
