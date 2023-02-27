from time import sleep
import USB_Com
import USB_Com_Utils
import MoveTranslator as MT
import ImageRecognitionHelper as IR
import chess
import chess.pgn
import chess.engine
import cv2 as cv
import numpy
import os
from datetime import datetime

def Start():
    global chessboard, engine
    #reset the chessboard
    chessboard = chess.Board()
    #calibrate the reference frame
    IR.Start()
    #Connect
    USB_Com.Connect()
    sleep(1)
    #Home
    USB_Com_Utils.Home()
    print("Homed")

    ClearFile()
    WriteMoveToFile("Game: "+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # gui.app.button_1.configure(command=lambda: OnUserConfirmMove())
    # gui.app.button_2.configure(command=lambda: ReTakePicture())


def Close():
    IR.Close()

def ReTakePicture():
    IR.GetRefFrame()

def OnUserPlayed():
    global userPlayed, chessboard

    Squares = IR.CompFrameDebug()
    result, move, uciName = MT.Ind2UCI(Squares, chessboard)
    if result == 1:
        print("Valid Move: " + uciName)
        WriteMoveToFile(move.uci())
        chessboard.push(move)
        Checked = MoveAI()
        IR.GetRefFrame()
        if(chessboard.is_game_over()):
            return 2#Game Over
        elif Checked == 1:
            return 3
        else:
            return 0
    elif result == 0:
        print('Invalid Move'+uciName)
        return 1 # error

def OnGameOver():
    game = chess.pgn.Game()
    game.from_board(chessboard)
    with open("game.pgn", "w") as f:
        f.write(game)

def WriteToFile():
    #write pgn file
    game = chess.pgn.Game()
    game.from_board(chessboard)
    with open("game.pgn", "w") as f:
        # f.write(game.builder)
        print("Game Saved")

def WriteMoveToFile(move):
    with open("game.txt", "a") as f:
        f.write(move+"\n")

def ClearFile():
    os.remove("game.txt")

def MoveAI():
    global chessboard, engine
    result = chess.Move.from_uci(engine.play(chessboard, chess.engine.Limit(time=1)).move.uci())
    isUnderCheck = False
    #Check if the move is capture
    if chessboard.is_capture(result):
        #get the position of the captured piece
        print(result.uci())
        MT.Capture(result.uci(), chessboard)
    elif chessboard.is_checkmate():
        print("Check Mate!")
        MT.UCI2Motor(result.uci())
        OnGameOver()
    elif chessboard.is_into_check(result):
        isUnderCheck = True
        MT.UCI2Motor(result.uci())
    elif chessboard.is_into_check(result) and chessboard.is_capture(result):
        isUnderCheck = True
        print(result.uci())
        MT.Capture(result.uci(), chessboard)
    elif chessboard.is_castling(result):
        print("Castle")
        MT.UCI2Motor(result.uci())
        input("Please keep the rook in place and click enter")
    elif (chessboard.piece_at(result.from_square).piece_type == chess.PAWN and chess.square_rank(result.to_square) in [0, 7]):#chess does not have a built in member for detecting promotion. This code was from this site: https://github.com/niklasf/python-chess/issues/67
        print("Promotion")
        MT.UCI2Motor(result.uci())
        input("This pawn is being promoted. Please replace it with a "+chess.piece_name(result.promotion)+" and click enter")
    elif (chessboard.piece_at(result.from_square).piece_type == chess.PAWN and chess.square_rank(result.to_square) in [0, 7]) and chessboard.is_capture(result):#chess does not have a built in member for detecting promotion. This code was from this site: https://github.com/niklasf/python-chess/issues/67
        print("Promotion")
        MT.Capture(result.uci()[2:4], result.uci())
        input("This pawn is being promoted. Please replace it with a "+chess.piece_name(result.promotion)+" and click enter")
    elif chessboard.piece_at(result.from_square).piece_type == chess.KNIGHT:
        print("Knight Move")
        MT.UCI2Motor_knight(result.uci(), chessboard)
    elif chessboard.piece_at(result.from_square).piece_type == chess.KNIGHT and chessboard.is_capture(result):
        print("Knight Move")
        MT.CaptureKnight(result.uci(), chessboard)
    else:
        print(result.uci())
        MT.UCI2Motor(result.uci())
    chessboard.push(result)
    WriteMoveToFile(result.uci())
    print(chessboard.fen())
    sleep(1)
    if isUnderCheck:
        return 1
    else: 
        return 0
