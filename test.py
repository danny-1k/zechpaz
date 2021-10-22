from utils import eval
import chess
from models import FC

from game import AI

fc = FC()

ai = AI(fc)

board = chess.Board()

ai.play(board)
