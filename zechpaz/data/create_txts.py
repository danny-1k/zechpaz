import chess.pgn
import os
from tqdm import tqdm
from . import data_utils

num = 0
iter = 0

path = '../chessdata/splitted'
to = '../chessdata/txts'

pgn_dataf = open(f'{to}/pgn_data_{iter}.txt', 'w')

count_per_file = 200_000

for f in tqdm(os.listdir(path)):
    if f.endswith('.pgn'):
        pgn = open(os.path.join(path, f))
        game = chess.pgn.read_game(pgn)
        result = game.headers['Result']
        outcome = '1' if result == '1-0' else '0' if result == '0-1' else None if result == '1/2-1/2' else None
        
        board = game.board()
        for move in game.mainline_moves():
            try:
                if outcome == None:
                    continue
                pgn_dataf.write(str(data_utils.b_to_array(board).tolist()))
                pgn_dataf.write(';')
                pgn_dataf.write(outcome)
                pgn_dataf.write('\n')
                board.push(move)
                num+=2
                # info = f'{one_hot_board(board)}_{outcome}_'
                # info = f'{one_hot_board(board.fen().split(" ")[0])}_outcome_{outcome}'
                # print(info)
                if num == count_per_file:
                    pgn_dataf.close()
                    pgn_dataf = open(f'{to}/pgn_data_{iter}.txt', 'w')
                    num = 0
                    iter+=1

            except Exception as e:
                print(e)
                continue

pgn_dataf.close()
