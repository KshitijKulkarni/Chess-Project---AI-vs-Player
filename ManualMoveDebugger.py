import USB_Com
import USB_Com_Utils
import MoveTranslator as MT

MT.AssignValues()
USB_Com.Connect()

#Home
USB_Com_Utils.Home()

while True:
    move = input("Enter move: ")
    MT.Capture(move[2:4], move)