import string
from time import sleep
import serial
import USB_Com_Utils as USB

#Set up a serial port
def Connect():
    global ser
    ser = serial.Serial("/dev/ttyACM0", 9600)
    ser.flushInput()
    if(not ser.isOpen):
        ser.open()
    print("Connected")

#set up a function to send data
def sendData(data):
    print(data);
    ser.write(data.encode())
    print(data.encode().decode())



def WaitForCallback():
    while (ser.readline().decode().strip()) != "Done":
        sleep(1)
    print("Motor Movement Completed")
    return
    

