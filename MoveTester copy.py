import PhysicalValues
import MoveTranslator as MT
import USB_Com
import USB_Com_Utils
from time import sleep

USB_Com.Connect()
sleep(1)
    #Home
USB_Com_Utils.Home()
print("Homed")

#create a function that converts a letter to a number
def LetterToNum(letter):
    return ((ord(letter)-96)-1)

def NumToLetter(num):
    return chr(num+97)

for i in range(100):
    USB_Com_Utils.Goto((475, 960))
    USB_Com_Utils.Goto((0,0))

