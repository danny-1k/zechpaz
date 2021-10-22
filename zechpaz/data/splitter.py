import os
import chess.pgn
from tqdm import tqdm

idx = 0

max_num = 60_000

in_dir = '../chessdata/raw'
out_dir = '../chessdata/splitted'

for i in tqdm(os.listdir(in_dir)):
    if i.endswith('.pgn'):
        pgn = open(os.path.join(in_dir, i), 'r')
        game = chess.pgn.read_game(pgn)
        while game and idx <= max_num:
            try:
                name = f"{game.headers['White']}_vs_{game.headers['Black']}".replace('?', '').replace('<', '').replace('>', '').replace(
                    ':', '').replace('"', '').replace('*', '').replace('|', '').replace(' ', '_').replace(',', '').replace('/', '') #windows shit
                if name in os.listdir('../chessdata/splitted'):
                    continue
                out = open(os.path.join(out_dir, name+'.pgn'), 'w')
                exporter = chess.pgn.FileExporter(out)
                idx += 1
                game.accept(exporter)
                game = chess.pgn.read_game(pgn)
            except Exception as e:
                print(e)
                continue
        pgn.close()
        os.remove(os.path.join(in_dir, i))
