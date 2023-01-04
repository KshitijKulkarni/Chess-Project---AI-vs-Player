from time import sleep
import USB_Com
import USB_Com_Utils
import MoveTranslator as MT
import chess
import chess.pgn
import chess.engine
import cv2 as cv
import numpy

def Start(skill):
    global chessboard, engine
    #setup stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("/home/admin/Stockfish-sf_15/src/stockfish")
    #set engine's skill level
    engine.configure({"Skill Level": skill})
    #reset the chessboard
    chessboard = chess.Board()
    #calibrate the reference frame
    #Connect

    USB_Com.Connect()
    sleep(1)
    #Home
    USB_Com_Utils.Home()
    print("Homed")

    # gui.app.button_1.configure(command=lambda: OnUserConfirmMove())
    # gui.app.button_2.configure(command=lambda: ReTakePicture())

    MoveAI()

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
        print("Continuing")
    chessboard.push(result)
    print(chessboard.fen())
    MoveAI()







Start(20)