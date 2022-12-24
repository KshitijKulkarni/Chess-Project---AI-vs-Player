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

Square = input("Enter the starting square: ")
xOffset = 0
yOffset = 0
#get the starting square's letter and number
SquareNumber = LetterToNum(Square[0])*8+int(Square[1])
for i in range(SquareNumber, 65):
    MT.UpdatePhysicalLocations()
    sqPos = MT.UCISingleSquare2Motor(i)
    while input("Is the piece in the center") == 'n':
        xOffset = int(input("Enter the x offset: "))
        yOffset = int(input("Enter the y offset: "))
        sqPos = (sqPos[0]+xOffset, sqPos[1]+yOffset)
        USB_Com_Utils.Goto(sqPos)
    for j in range(i-1, 64):
        print("Setting forward values")
        tempsq = MT.returnPhysicalPos(j)
        tempsqPos = (tempsq[0]+xOffset, tempsq[1]+yOffset)
        PhysicalValues.SetLocation(j, tempsqPos)

#loop through letters a to h
# for i in range(0,8):

