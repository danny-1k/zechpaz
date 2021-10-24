import chess
from game import Game
from zechpaz.common.models import FC

net = FC()
net.load_('zechpaz/trained_models/FC.pt')
net.eval()

board = chess.Board()

game = Game(board,net)

while True:
    game.print_board()

    if game.make_move_ai__():
        break

    game.print_board()

    #input('Press Enter for next move')

    if game.make_move_ai__():
        break

    #input('Press Enter for next move')