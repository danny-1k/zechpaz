import os 
import torch
import zipfile
import requests
import numpy as np
import matplotlib.pyplot as plt
from data_utils import b_to_array

unicode_pieces = {
    'P': u'\u2659',
    'N': u'\u2658',
    'B': u'\u2657',
    'R': u'\u2656',
    'Q': u'\u2655',
    'K': u'\u2654',
    'p': u'\u265F',
    'n': u'\u265E',
    'b': u'\u265D',
    'r': u'\u265C',
    'q': u'\u265B',
    'k': u'\u265A',
    'b.': u'\u25FB',
    'w.': u'\u25FC',


}

row_to_idx = {
    0: 8,
    1: 7,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1,
}

col_to_char = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
}

def print_board(board, flip=False):
    fen = board.fen().split(' ')[0]
    bb = []
    for i in range(1, 9):
        fen = fen.replace(str(i), '.'*i)

    for row, line in enumerate(fen.split('/')):
        r = []
        for col, char in enumerate(line):
            if char != '.':
                r.append(unicode_pieces[char])
            else:
                if ord(str(row_to_idx[row])) % 2 == ord(col_to_char[col]) % 2:
                    r.append(unicode_pieces['b.'])
                else:
                    r.append(unicode_pieces['w.'])

        bb.append(r)

    if flip:
        bb = np.flip(np.array(bb)).tolist()
        print('\n'.join([str(idx+1)+' ' + (' '.join(i)) for idx,i in enumerate(bb)])+'\n  '+' '.join(['a','b','c','d','e','f','g','h'][::-1]))
    else:
        print('\n'.join([str(8-idx)+' ' + (' '.join(i)) for idx,i in enumerate(bb)])+'\n  '+' '.join(['a','b','c','d','e','f','g','h']))


def search_positions(board, depth=2):
    depth_list = []
    def flatten(l): return [item for sublist in l for item in sublist]
    for i in range(depth+1):
        depth_list.append([])

    depth_list[0].append(board)
    for layer in depth_list:
        layer_set = []

        try:
            stet = flatten(layer)
        except:
            stet = layer

        for i in range(len(stet)):
            legal_moves = [stet[i].san(j) for j in list(stet[i].legal_moves)]
            legal_moveset = []
            for move in legal_moves:
                neo_board = stet[i].copy()
                neo_board.push_san(move)
                legal_moveset.append(neo_board)
            layer_set.append(legal_moveset)

        if depth_list.index(layer) + 1 == len(depth_list):
            break
        depth_list[depth_list.index(layer) + 1] = layer_set
    return depth_list


def eval_pos(lst, net,mode='min'):
    for i in range(len(lst)):
        try:
            x = b_to_array(lst[i]).reshape(1, -1)
            y = net(torch.from_numpy(x).float())
            lst[i] = y[0].item()

        except:
            eval_pos(lst[i], net,mode=mode)

    if mode == 'min':
        min = float('inf')
        for term in lst:
            if np.mean(term) < min:
                min = np.mean(term)
                index = lst.index(term)
        try:
            return index
        except:
            return len(lst)-1
    
    if mode == 'max':
        max = float('-inf')
        for term in lst:
            if np.mean(term) > max:
                max = np.mean(term)
                index = lst.index(term)
        try:
            return index
        except:
            return len(lst)-1

def unzip_file(f,dir,remove=False):
    with zipfile.ZipFile(f,'r') as zipf:
        zipf.extractall(dir)
    if remove:
        os.remove(f)

def download_from_url(url,dir):
    r = requests.get(url,allow_redirects=True).content
    filename = os.path.join(dir,url.rsplit('/', 1)[1])
    f = open(filename,'wb')
    f.write(r)
    f.close()


def eval(board,net,depth,w=True):

    if depth == 0:
        val = float('-inf') if w==True else float('inf')
        ev = 0
        for idx,move in enumerate(list(board.legal_moves)):
            board.push(move)
            x = torch.from_numpy(b_to_array(board)).view(-1).float()
            y = net(x)

            if w == True:
                if y > val:
                    val = idx
                    ev = y

            else:
                if y<val:
                    val = idx
                    ev = y


            board.pop()

    else:
        val = float('-inf') if w==True else float('inf')
        ev = 0
        legal_moves = list(board.legal_moves)
        for idx,move in enumerate(legal_moves):
            board.push(move)

            x = torch.from_numpy(b_to_array(board)).view(-1).float()
            y = net(x)

            if w == True:
                if y > val:
                    val = idx
                    ev = y

            else:
                if y<val:
                    val = idx
                    ev = y

            board.pop()

        board.push(legal_moves[val])
        ev,val = eval(board,net,depth=depth-1,w=bool(1-w))
        board.pop()
        w = bool(1-w)
        

    return (ev,val)