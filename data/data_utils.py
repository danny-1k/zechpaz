import numpy as np

def b_to_array(b):
    board = {
        'P': np.zeros((8, 8)),
        'N': np.zeros((8, 8)),
        'B': np.zeros((8, 8)),
        'R': np.zeros((8, 8)),
        'Q': np.zeros((8, 8)),
        'K': np.zeros((8, 8)),

    }

    fen = b.fen().split(' ')[0]
    for i in range(1, 9):
        fen = fen.replace(str(i), '.'*i)
    for row, line in enumerate(fen.split('/')):
        for col, char in enumerate(line):
            if char != '.':
                if char.isupper():
                    board[char][row][col] = 1
                else:
                    board[char.upper()][row][col] = -1
    b = np.array([board[i] for i in board])
    return b