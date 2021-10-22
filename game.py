import os
import time
import torch
from zechpaz.common.utils import b_to_array,print_board,eval_pos,search_positions

class Game:
    def __init__(self,board,net,color='white',depth=2):
        if color not in ['white','black']:
            raise ValueError('color must be black or white')
        self.board = board
        self.net = net
        self.color = color
        self.ai_mode = 'max' if self.color == 'black' else 'min'
        self.depth = depth

    def make_move_ai(self):
        if self.board.turn == (self.color == 'black'):

            legal_moves = [self.board.san(i) for i in list(self.board.legal_moves)]

            poss = search_positions(self.board,depth=self.depth)

            try:
                self.board.push_san(legal_moves[eval_pos(poss[-1],self.net,mode=self.ai_mode)])
            
            except IndexError:

                if self.board.is_checkmate():
                    print('AI checkmate')

                else:
                    print('Jeu terminé')

            return self.board.is_game_over()

    def make_move_human(self):
        if self.board.turn == (self.color == 'white'):
            legal_moves = [self.board.san(i) for i in list(self.board.legal_moves)]
            while True:
                move = input('Move >_ ')
                if move in legal_moves:
                    self.board.push_san(move)
                    break

                print(legal_moves)

            if self.board.is_checkmate():
                print('AI checkmate')
            
            elif self.board.is_game_over():
                print('Jeu terminé')

            
            return self.board.is_game_over()

    
    def print_board(self):
        if os.system('cls') == 1:
            os.system('clear')

        print_board(self.board,self.color=='black')