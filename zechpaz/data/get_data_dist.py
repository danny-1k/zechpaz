import os

import numpy as np
import matplotlib.pyplot as plt
path = '../chessdata/processed'

w,d,b = 0,0,0
total = 0

for f in [i for i in os.listdir(path) if 'Y' in i]:
    arr = np.load(os.path.join(path,f))
    for i in arr:
        if i == 1:
            w+=1
        if i == 0:
            b+=1
        if i == -1:
            d+=1
        total+=1

print(f'WHITE => {w}')
print(f'      => {w/total * 100 :.1f}%')
print(f'BLACK => {b}')
print(f'      => {b/total * 100 :.1f}%')
print(f'DRAW  => {d}')
print(f'      => {d/total * 100 :.1f}%')

plt.bar(['White','Black','Draw'],[w,b,d])
plt.show()