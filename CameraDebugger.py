from cv2 import VideoCapture
import ImageRecognition as IR
import cv2 as cv
from time import sleep

counter = 0
images: list = []
while True:
    cap = VideoCapture(0)
    ret, frame = cap.read()
    images.append(frame)
    cap.release()
    counter += 1
    print(counter)
    sleep(0.1)
