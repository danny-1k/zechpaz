import torch
from torch.utils.data import Dataset

import numpy as np

import chess

from data_utils import b_to_array

class AEData(Dataset):
    def __init__(self, x_dir):
        self.x = np.load(x_dir)

    def __len__(self):
        return self.x.shape[0]

    def __getitem__(self, idx):
        return (torch.Tensor(self.x[idx]).view(1,-1), torch.Tensor(self.x[idx]).view(1,-1))



class CaturData(Dataset):
    def __init__(self, df):
        self.x = df['X']
        self.y = df['Y']

    def __len__(self):
        return self.y.shape[0]

    def __getitem__(self, idx):
        x = b_to_array(chess.Board(self.x.iloc[idx]))
        y = [float(''.join([i for i in self.y.iloc[idx] if i.isdigit() or i in ['+','-']]))/100]
        y = np.arctan(y)
        return (torch.from_numpy(x).view(-1),torch.Tensor(y))