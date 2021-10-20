import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

from ..common.models import FC

from .data import CaturData

torch.manual_seed(42)


df = pd.read_csv('chessData.csv')
df.sample(frac=1)

df.columns = ['X','Y']

train,test = train_test_split(df,train_size=.8,random_state=42)

train = CaturData(train)
test = CaturData(test)

trainloader = DataLoader(train, batch_size=128, shuffle=True)
testloader = DataLoader(test, batch_size=128, shuffle=True)


net = FC()

optimizer = optim.Adam(net.parameters(), lr=1e-4)
lossfn = nn.MSELoss()

net.train_(
    optimizer=optimizer,
    lossfn=lossfn,
    log_name='fc_loss.png',
    train_loader=trainloader,
    test_loader=testloader,
    epochs=500
)

