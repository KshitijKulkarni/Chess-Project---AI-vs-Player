from Pathfinder import FindPath
from cv2 import waitKey
import USB_Com_Utils as USB
import time
import ImageRecognitionHelper as IR
import chess
import Knight
import PhysicalValues as PV

PhysicalLocations = PV.GetAllLocations()
print (PhysicalLocations)

def UpdatePhysicalLocations():
    global PhysicalLocations
    PhysicalLocations = PV.GetAllLocations()

def SqCoord2SqID(x, y):
    return (x*8)+y


def UCI2Coord(move: str):
    print(type(move))
    listofchars = list(move)
    #Convert a letter to a number
    def LetterToNum(letter):
        return ((ord(letter)-96)-1)

    return PhysicalLocations[LetterToNum(listofchars[0])*8+int(listofchars[1])-1]

def UCISingleSquare2Motor(SquareNo: int):
    SquareNo = SquareNo - 1
    print (SquareNo)
    USB.Goto(PhysicalLocations[SquareNo])
    return PhysicalLocations[SquareNo]

def returnPhysicalPos(SquareNo: int):
    return PhysicalLocations[SquareNo]

def UCI2Motor(move):
    def UCIToArrayVal(val):
        #split the string into half
        def SplitString(string):
            return string[0:len(string)//2],string[len(string)//2:]

        #split the first half into x and y
        def SplitHalf(string):
            return (string[0],string[1])

        sq1 = SplitHalf(SplitString(val)[0])
        sq2 = SplitHalf(SplitString(val)[1])
        return sq1[0], sq1[1], sq2[0], sq2[1]
    
    #Convert a letter to a number
    def LetterToNum(letter):
        return ((ord(letter)-96)-1)

    X1, Y1, X2, Y2 = UCIToArrayVal(move)

    Sq1 = SqCoord2SqID(LetterToNum(X1), int(Y1)-1)
    Sq2 = SqCoord2SqID(LetterToNum(X2), int(Y2)-1)
    
    ActualSquare1 = PhysicalLocations[Sq1]
    ActualSquare2 = PhysicalLocations[Sq2]
    USB.MakeMove(ActualSquare1, ActualSquare2)
    waitKey(1)
    IR.GetRefFrame()
    
def UCI2Motor_knight (move, ChessBoard: chess.Board): #this is an unmodified function. Integrate pathfinding later. The arduino accepts z as a command for the knight.
    def UCIToArrayVal(val):
        #split the string into half
        def SplitString(string):
            return string[0:len(string)//2],string[len(string)//2:]

        #split the first half into x and y
        def SplitHalf(string):
            return (string[0],string[1])

        sq1 = SplitHalf(SplitString(val)[0])
        sq2 = SplitHalf(SplitString(val)[1])
        return sq1[0], sq1[1], sq2[0], sq2[1]
    
    #Convert a letter to a number
    def LetterToNum(letter):
        return ((ord(letter)-96)-1)

    X1, Y1, X2, Y2 = UCIToArrayVal(move)

    Sq1 = (LetterToNum(X1), int(Y1)-1)
    Sq2 = (LetterToNum(X2), int(Y2)-1)
    
    Knight.MakeMove(Sq1, Sq2, ChessBoard, USB, PhysicalLocations)
    waitKey(1)
    IR.GetRefFrame()
    
def Ind2UCI(move, chessboard: chess.Board):
    Square1 = move[0]
    Square2 = move[1]
    #Convert a number to a letter
    def NumToLetter(num):
        return chr(num+97)
    

    Square1 = (NumToLetter(Square1[0]), 9-(Square1[1]+1))
    Square2 = (NumToLetter(Square2[0]), 9-(Square2[1]+1))
    if Square1[0] == 'j' or Square2[0] == 'j':
        # print("Invalid Move")
        return 0, chess.Move.null(), "No Move Was Captured"
    Square1UCI = (Square1[0])+str(Square1[1])
    Square2UCI = (Square2[0])+str(Square2[1])

    if len(Square1UCI+Square2UCI) > 4 or len(Square1UCI+Square2UCI) < 4:
        return 0, chess.Move.null(), "MoveTooBig"

    #if Square1UCI is occupied
    if (not chessboard.is_legal(chess.Move.from_uci(Square1UCI+Square2UCI))):
        temp = Square1UCI
        Square1UCI = Square2UCI
        Square2UCI = temp

    if not chessboard.is_legal(chess.Move.from_uci(Square1UCI+Square2UCI)):
        return 0, chess.Move.null(), Square1UCI+Square2UCI

    move = chess.Move.from_uci(Square1UCI+Square2UCI)
    return 1, move, Square1UCI+Square2UCI

def Capture(move: str, ChessBoard: chess.Board):
    #region Functions
    def UCIToArrayVal(val):
        #split the string into half
        def SplitString(string):
            return string[0:len(string)//2],string[len(string)//2:]

        #split the first half into x and y
        def SplitHalf(string):
            return (string[0],string[1])

        sq1 = SplitHalf(SplitString(val)[0])
        sq2 = SplitHalf(SplitString(val)[1])
        return sq1[0], sq1[1], sq2[0], sq2[1]
    
    #Convert a letter to a number
    def LetterToNum(letter):
        return ((ord(letter)-96)-1)

    def ComputeRealValues(Path):
        newPath = Path
        for i in range(len(Path)):
            newPath[i] = PhysicalLocations[SqCoord2SqID(Path[i][0], Path[i][1])]
            # print(PhysicalLocations[Path[i][0]][Path[i][1]])
        return newPath
            


    #endregion    

    X1, Y1, X2, Y2 = UCIToArrayVal(move)

    Sq1 = (LetterToNum(X1), int(Y1)-1)
    Sq2 = (LetterToNum(X2), int(Y2)-1)
    
    # print(Sq1, Sq2)
    ActualSquare1 = PhysicalLocations[SqCoord2SqID(Sq1[0],Sq1[1])]

    Path = FindPath(Sq2, ChessBoard, chess.Move.from_uci(move))

    RealPath = ComputeRealValues(Path)
    USB.Capture(ActualSquare1, RealPath)
    print("Captured!")
    IR.GetRefFrame()
    waitKey(1)

def CaptureKnight(move: str, ChessBoard: chess.Board):
    #region Functions
    def UCIToArrayVal(val):
        #split the string into half
        def SplitString(string):
            return string[0:len(string)//2],string[len(string)//2:]

        #split the first half into x and y
        def SplitHalf(string):
            return (string[0],string[1])

        sq1 = SplitHalf(SplitString(val)[0])
        sq2 = SplitHalf(SplitString(val)[1])
        return sq1[0], sq1[1], sq2[0], sq2[1]
    
    #Convert a letter to a number
    def LetterToNum(letter):
        return ((ord(letter)-96)-1)

    def ComputeRealValues(Path):
        newPath = Path
        for i in range(len(Path)):
            newPath[i] = PhysicalLocations[SqCoord2SqID(Path[i][0], Path[i][1])]
            # print(PhysicalLocations[Path[i][0]][Path[i][1]])
        return newPath
            


    #endregion    

    X1, Y1, X2, Y2 = UCIToArrayVal(move)

    Sq1 = (LetterToNum(X1), int(Y1)-1)
    Sq2 = (LetterToNum(X2), int(Y2)-1)
    
    # print(Sq1, Sq2)
    ActualSquare1 = PhysicalLocations[SqCoord2SqID(Sq1[0], Sq1[1])]

    Path = FindPath(Sq2, ChessBoard)

    RealPath = ComputeRealValues(Path)
    USB.CPMove(RealPath)
    Knight.MakeMove(Sq1, Sq2, ChessBoard, USB, PhysicalLocations)
    print("Captured!")
    IR.GetRefFrame()
    waitKey(1)

