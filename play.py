import chess
import argparse
from game import Game
from zechpaz.common.models import FC

parser = argparse.ArgumentParser()
parser.add_argument('--color',help="color to play as. white or black ")
args = parser.parse_args()

color = args.color
color = color if color in ['black','white'] else 'white'

net = FC()
net.load_('zechpaz/trained_models/FC.pt')
net.eval()

board = chess.Board()

game = Game(board,net,color)

while True:
    game.print_board()
    
    if game.make_move_human():
        break

    game.print_board()

    if game.make_move_ai():
        break