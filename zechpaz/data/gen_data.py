import os
import numpy as np
from tqdm import tqdm

import argparse

import random
'''
Converts the pgn_data.txt file into arrays and
ensures a balanced dataset
'''

parser = argparse.ArgumentParser(description='Script for downloading data')
parser.add_argument('--num_data', type=int, default=1_000_000,help="Number of datapoints to generate.")
parser.add_argument('--per_array', type=int, default=100_000,help="Number of datapoints to generate at a time")
args = parser.parse_args()

count_per_array = int(args.per_array)
idx = 0
iter_ = 0
num = 1
ix = 1
b = 0
w = 0
B = []
W = []

txt_dir = '../chessdata/txts/'

bs = 0
ws = 0

for file in os.listdir(txt_dir):
    print(file)
    f = open(os.path.join(txt_dir,file), 'r').read().split('\n')[:-1]

    for item in tqdm(f):
        if idx == int(args.num_data):
            print('Num of datapoints reached')
            break

        bb,label = item.split(';')

        if label == '0': #black
            bs+=1
            
            B.append((eval(bb),eval(label)))

        if label == '1': #white
            ws+=1

            W.append((eval(bb),eval(label)))

        idx+=1
        
        
        if idx % count_per_array == 0:
            if bs > ws:
                random.shuffle(B)
                B = B[:ws]
                bs = ws

            elif ws > bs:
                random.shuffle(W)
                W = W[:bs]
                ws = bs

            data = B+W
            random.shuffle(data)

            X,Y = zip(*data)

            np.save(f'../chessdata/processed/X_{num}', np.array(X))
            np.save(f'../chessdata/processed/Y_{num}', np.array(Y))

            num+=1
            X = []
            Y = []
            B = []
            W = []
            b = 0
            w = 0

if len(B) != 0 and len(W) != 0:

    if bs > ws:
        random.shuffle(B)
        B = B[:ws]
        bs = ws

    elif ws > bs:
        random.shuffle(W)
        W = W[:bs]
        ws = bs
        
    data = B+W
    random.shuffle(data)

    X,Y = zip(*data)

    np.save(f'../chessdata/processed/X_{num}', np.array(X))
    np.save(f'../chessdata/processed/Y_{num}', np.array(Y))