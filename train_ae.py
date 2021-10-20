import os
import torch
import numpy as np
from models import AE
import torch.nn as nn
from data import AEData
import torch.optim as optim
from torch.utils.data import ConcatDataset, DataLoader

torch.manual_seed(0)

np.random.seed(32)

all_xs = [os.path.join('data/processed', i)
          for i in os.listdir('data/processed') if 'X' in i]

np.random.shuffle(all_xs)

train_ratio = .7
train_len = int(len(all_xs) * train_ratio)
test_len = len(all_xs) - train_len

train = ConcatDataset([AEData(i) for i in all_xs[:train_len]])
test = ConcatDataset([AEData(i) for i in all_xs[train_len:]])

trainloader = DataLoader(train, batch_size=32, shuffle=True)
testloader = DataLoader(test, batch_size=32, shuffle=True)


net = AE()

optimizer = optim.Adam(net.parameters(), lr=0.0001)
lossfn = nn.MSELoss()

net.train_(
    optimizer=optimizer,
    lossfn=lossfn,
    log_name='ae_loss.png',
    train_loader=trainloader,
    test_loader=testloader,
    epochs=100
)
