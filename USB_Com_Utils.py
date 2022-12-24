import USB_Com as USB
import time


def Home():
    MoveMade=False
    print("Homing...")
    USB.sendData("h")
    USB.WaitForCallback()

def Grab():
    USB.sendData("G\n")
    USB.WaitForCallback()

def UnGrab():
    USB.sendData("g\n")
    USB.WaitForCallback()

def Goto(Square):
    USB.sendData(str(Square[0])+","+str(Square[1])+"\n")
    USB.WaitForCallback()

def MakeMove(Square1, Square2):
    data = 'Z'+str(Square1[0])+','+str(Square1[1])+','+ str(Square2[0])+','+str(Square2[1])+";"#Eg Z120,120,120,240;
    print(data)
    USB.sendData(data)
    USB.WaitForCallback()


def CPMove(path):
    path = str(path)
    path = path.replace("(",";")
    path = path.replace(")",";")
    path = path.replace(" ","")
    path = path.replace("[","")
    path = path.replace("]","")
    path = path.replace(";,;",";")
    data = path
    data = data.replace("(","k")
    data = data.replace(");",";")
    data = data.replace(" ","")
    #replace the inital semicolon in the data with 'k'
    data = data.replace(";","k", 1)

    #remove the final semicolon
    USB.sendData(data+"\n")
    # print(data)
    USB.WaitForCallback()

def Capture(Square1, Path):
    path = str(Path)
    path = path.replace("(",";")
    path = path.replace(")",";")
    path = path.replace(" ","")
    path = path.replace("[","")
    path = path.replace("]","")
    path = path.replace(";,;",";")
    data = str(Square1)+path
    data = data.replace("(","c")
    data = data.replace(");",";")
    data = data.replace(" ","")
    #remove the final semicolon
    USB.sendData(data+"\n")
    USB.WaitForCallback()