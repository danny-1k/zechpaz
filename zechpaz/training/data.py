import os

import torch
from torch.utils.data import Dataset

import numpy as np

class ChessData(Dataset):
    def __init__(self, xdir,ydir):
        self.x = np.load(os.path.join('zechpaz/chessdata/processed/',xdir),allow_pickle=True)
        self.y = np.load(os.path.join('zechpaz/chessdata/processed/',ydir),allow_pickle=True)

    def __len__(self):
        return self.y.shape[0]

    def __getitem__(self, idx):
        x = self.x[idx]
        y = [self.y[idx]]
        return (torch.from_numpy(x).view(-1),torch.Tensor(y))