import os

import torch
import torch.nn as nn
from tqdm import tqdm
import matplotlib.pyplot as plt


class Model:
    def save_(self, f):
        torch.save(self.state_dict(), f)

    def load_(self, f):
        self.load_state_dict(torch.load(f))

    def freeze_(self):
        for param in self.parameters():
            param.requires_grad_(False)

    def train_(self, optimizer, lossfn, train_loader,plot_dir,checkpoint_dir, test_loader=None, epochs=5):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.to(device)

        train_loss_over_time = []

        last_loss = float('inf')
        if test_loader:
            test_loss_over_time = []

        for epoch in tqdm(range(epochs)):
            batch_train_loss_over_time = []
            if test_loader:
                batch_test_loss_over_time = []
            self.train()
            for x, y in train_loader:
                x = x.to(device).float()
                y = y.to(device).float()
                optimizer.zero_grad()
                p = self.__call__(x)
                loss = lossfn(p, y)
                loss.backward()
                optimizer.step()
                batch_train_loss_over_time.append(loss.item())

            if test_loader:
                self.eval()
                with torch.no_grad():
                    for x, y in test_loader:
                        x = x.to(device).float()
                        y = y.to(device).float()
                        p = self.__call__(x)
                        loss = lossfn(p,y)
                        batch_test_loss_over_time.append(loss.item())

            train_loss = sum(batch_train_loss_over_time) / \
                len(batch_train_loss_over_time)
            test_loss = sum(batch_test_loss_over_time) / \
                len(batch_test_loss_over_time)

            train_loss_over_time.append(train_loss)
            test_loss_over_time.append(test_loss)

            if test_loader:
                if test_loss_over_time[-1] < last_loss:
                    self.save_(os.path.join(checkpoint_dir,type(self).__name__ + '.pt'))
                    last_loss = test_loss_over_time[-1]

            else:
                if train_loss_over_time[-1] < last_loss:
                    self.save_(os.path.join(checkpoint_dir,type(self).__name__ + '.pt'))
                    last_loss = train_loss_over_time[-1]



            plt.plot(train_loss_over_time, label='train loss')
            if test_loader:
                plt.plot(test_loss_over_time, label='test loss')

            plt.legend()
            plt.savefig(os.path.join(plot_dir, f'{type(self).__name__}_loss.png'))
            plt.close('all')

class FC(nn.Module, Model):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6*8*8,1024),
            nn.Dropout(.7),
            nn.LeakyReLU(),
            nn.Linear(1024,100),
            nn.Dropout(.4),
            nn.LeakyReLU(),
            nn.Linear(100,50),
            nn.LeakyReLU(),
            nn.Linear(50,1),
            nn.Sigmoid()
        )

    
    def forward(self,x):
        x = self.net(x)
        return x
        