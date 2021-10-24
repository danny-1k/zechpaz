import os

dirs = os.listdir('zechpaz')

if 'plots' not in dirs:
    os.makedir('plots')

if 'trained_models' not in dirs:
    os.makedirs('zechpaz/trained_models')

if 'chessdata' not in dirs:
    os.makedirs('zechpaz/chessdata')