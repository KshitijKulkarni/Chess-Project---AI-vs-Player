import sys
import cv2 as cv
import numpy
from cv2 import imshow, waitKey
from VideoCaptureThread import VideoCapture


def UpdateGUI(mat: cv.Mat):
    # imshow("MainWindow", mat)
    # cv.waitKey(1)
    print("GUI Updated")




PointsFilePath = "Data.txt"
#region Companion Functions

def SetContrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

#read lines from a file into a list
def ReadLines(filePath):
    with open(filePath) as f:
        content = f.readlines()
    return content

#get comma seperated values from a list of strings as a list of int tuples
def GetCSV(lines):
    CSV = []
    for line in lines:
        CSV.append(tuple(map(int, line.split(","))))
    return numpy.float32(CSV)
#endregion
perstool = cv.getPerspectiveTransform(GetCSV(ReadLines(PointsFilePath)), numpy.float32([(0, 0), (0, 300), (300, 0), (300, 300)]))

#region Companion Functions
points = [
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
    [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    ]

rgbValues = [
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
]

xZero, xDistance, yZero, yDistance = 0,38,0,37
for x in range(9):
    for y in range(9):
        points[x][y] = ((xZero+(x*xDistance)),(yZero+(y*yDistance)))

def GetAvgColor(image):

    for x in range(8):
        for y in range(8):
            p1x = points[x][y][0]
            p1y = points[x][y][1]
            p2x = points[x+1][y+1][0]
            p2y = points[x+1][y+1][1]
            roi = image[p1y:p2y, p1x:p2x]
            rgbValues[x][y] = roi.mean(axis=0).mean(axis=0)
            image = cv.rectangle(image, (p1x,p1y), (p2x,p2y), rgbValues[x][y], cv.FILLED)
        

    return image

cap = VideoCapture(cv.CAP_V4L2)

def GetRawInput():
    global cap
    frame = cap.read()
    return frame

def StoreRefFrame():
    global cap
    frame = cap.read()
    cv.waitKey(1)
    UpdateGUI(frame)
    # frame = SetContrast(frame, -50,50)
    frame = cv.warpPerspective(frame, perstool, (300,300))
    frame = GetAvgColor(frame)
    cv.waitKey(1)
    UpdateGUI(frame)
    return frame
    # return frame

#region Companion Functions
def SubtractImages(image1, image2):
    #convert each image to grayscale
    image1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    image2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)
    diff = cv.absdiff(image1, image2)
    return diff

def FindDifference(image):
    #get the dimensions of image
    height, width = image.shape[:2]

    Square1 = (9,9)
    Square2 = (9,9)
    loop1Break = False;
    #loop over every pixel
    for x in range(0, width):
        for y in range(0, height):
            #get the current pixel value
            px = image[y, x]
            #if the pixel is not white
            if px > 10:
                Square1=(x,y)
                loop1Break = True
                break
        if loop1Break:
            break
    
    loop2Break = False;
    for x in range(0,width):
        for y in range(0,height):
            px = image[y,x]
            if px > 10 and (x,y) != Square1:
                Square2=(x,y)
                loop2Break = True
                break
        if loop2Break:
            break   
    return (Square1, Square2)


#endregion
def OnUserPlayed(OldFrame):
    global cap
    frame = cap.read()
    # frame = SetContrast(frame, -50,50)
    frame = cv.warpPerspective(frame, perstool, (300,300))
    frame = GetAvgColor(frame)
    newRefFrame = frame.copy()
    UpdateGUI(newRefFrame)
    frame = SubtractImages(frame, OldFrame)
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv.flip(frame, 1)
    ret, frame = cv.threshold(frame, 10, 255, cv.THRESH_BINARY)
    waitKey(1)
    frame = cv.resize(frame, (8,8))
    return newRefFrame, FindDifference(frame)
