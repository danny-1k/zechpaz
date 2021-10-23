import os

dirs = os.listdir('.')

if 'plots' not in dirs:
    os.makedirs('plots')

if 'trained_models' not in dirs:
    os.makedirs('trained_models')