import os

dirs = os.listdir('.')

if 'plots' not in dirs:
    os.makedir('plots')

if 'trained_models' not in dirs:
    os.makedir('trained_models')