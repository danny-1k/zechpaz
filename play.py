import os
import time
import chess
import argparse
from zechpaz.common.models import FC
from zechpaz.common.utils import search_positions,eval_pos,print_board

parser = argparse.ArgumentParser()
parser.add_argument('--color',help="color to play as. w or b ")

args = parser.parse_args()
if args.color == 'b':
    is_white = False
else:
    is_white  = True

def clear():
    if os.system('cls')==1:
        os.system('clear')

net = FC()
net.load_('zechpaz/trained_models/FC.pt')
net.eval()

board = chess.Board()

clear()

while not board.is_game_over():
    print_board(board)
    if is_white:
        while True:
            move = input('Move >_ ')
            legal_moves = [board.san(i) for i in list(board.legal_moves)]
            if move in legal_moves:
                board.push_san(move)
                break
            print(legal_moves)

        lms = [board.san(i) for i in list(board.legal_moves)]
        
        
        clear()
        print_board(board)
        input('Press Enter for AI move')
        clear()

        poss = search_positions(board)
        try:
            board.push_san(lms[eval_pos(poss[-1],net,mode='min')])
        except IndexError:
            if board.is_checkmate():
                print('Checkmate by ',end='')
                print('AI' if board.turn() == is_white else 'You')
            else:
                print('Jeu terminé')

            print(f'{"Checkmate by " if board.ischeckmate() else "Game Over"}')

    else:
        lms = [board.san(i) for i in list(board.legal_moves)]
        print_board_ = lambda :print_board(board,True)
        clear()
        print_board_()
        input('Press Enter for AI move')
        clear()

        poss = search_positions(board)

        try:
            board.push_san(lms[eval_pos(poss[-1],net,mode='min')])
        except IndexError:
            if board.is_checkmate():
                print('Checkmate by ',end='')
                print('AI' if board.turn() == is_white else 'You')
            else:
                print('Jeu terminé')

            print(f'{"Checkmate by " if board.ischeckmate() else "Game Over"}')
            
        board.push_san(lms[eval_pos(poss[-1],net,mode='max')])

        clear()
        print_board_()
        while True:
            move = input('Move >_ ')
            legal_moves = [board.san(i) for i in list(board.legal_moves)]
            if move in legal_moves:
                board.push_san(move)
                break
            print(legal_moves)
        clear()
        print_board_()