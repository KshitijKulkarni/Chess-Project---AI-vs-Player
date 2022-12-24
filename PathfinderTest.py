import chess
import MoveTranslator
import USB_Com as USB
import USB_Com_Utils as USBU
from time import sleep

chessboard = chess.Board()
move = "g1h35"

USB.Connect()
sleep(1)
USBU.Home()
sleep(1)
MoveTranslator.AssignValues()
MoveTranslator.UCI2Motor_knight(move, chessboard)