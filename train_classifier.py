import os
import sys

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,ConcatDataset
from sklearn.model_selection import train_test_split

from common.models import FC

from training.data import ChessData

torch.manual_seed(42)

all_xys = os.listdir('chessdata/processed')

all_xys = list(zip([i for i in all_xys if 'X' in i],[i for i in all_xys if 'Y' in i]))

train,test = train_test_split(all_xys,train_size=.6,random_state=42)

train = ConcatDataset([ChessData(x,y) for x,y in train])
test = ConcatDataset([ChessData(x,y) for x,y in test])

trainloader = DataLoader(train, batch_size=128, shuffle=True)
testloader = DataLoader(test, batch_size=128, shuffle=True)

print('Go\'en the da\'a')


net = FC()

optimizer = optim.Adam(net.parameters(), lr=1e-4)
lossfn = nn.MSELoss()

net.train_(
    optimizer=optimizer,
    lossfn=lossfn,
    train_loader=trainloader,
    test_loader=testloader,
    epochs=500,
    checkpoint_dir='trained_models',
    plot_dir='plots'
)

