import chess
import numpy as np
from models import FC

from data_utils import b_to_array
import copy

import torch

class Node:
    def __init__(self,eval,branch=None,color=None):
        self.branch = branch
        self.color = color if branch == None else branch.color
        self.eval = eval

    def mean_eval(self):
        if self.branch != None:
            evals = []
            for i in self.branch.children:
                evals.append(i.eval)

            eval = sum(evals)/len(evals)

            return eval

        else:
            return self.eval

class Branch:
    def __init__(self,parent_node,color):
        self.parent_node = parent_node
        self.color = color
        self.children = []

    def addNode(self,node):
        self.children.append(node)

    def mean_eval(self):
        return self.mean_eval()


class Tree:
    def __init__(self,start_color='w'):
        self.start_color = start_color
        self.branches = []

    def addBranch(self,branch):
        self.branches.append(branch)

    def bestMove(self):
        idx_dict = {}
        for idx,depth in list(reversed(list(enumerate(self.branches)))):
            print([i.eval for i in depth.children ])
            scores = np.array([i.mean_eval() for i in depth.children])
            if self.start_color == 'w':
                if idx%2 == 0:
                    idx = scores.argmax()
                else:
                    idx = scores.argmin()

            else:
                if idx%2 == 0:
                    idx = scores.argmin()
                else:
                    idx = scores.argmax()

            idx_dict[idx] = idx

        
        return idx_dict[0]




class AI:
    def __init__(self,net,f='FC.pt',color='b',depth=2):
        self.net = net
        self.net.load_(f)
        self.color = color
        self.depth = depth


    def play(self,board):
        #boards = [[board.copy()]]

        game_tree = Tree(start_color=self.color)
        eval = self.net(
                torch.from_numpy(
                    b_to_array(board).\
                        reshape(1,-1)).float()\
                            )[0].item()
        start_node = Node(eval,color=self.color)

        start__branch = Branch(start_node,self.color)

        game_tree.addBranch(start__branch)


        def create_branches(board,node,depth):
            branch = Branch(node,color='bw'[board.turn])

            if depth == 0:
                for move in list(board.legal_moves):
                    board.push(move)
                    eval = self.net(
                        torch.from_numpy(
                            b_to_array(board).\
                            reshape(1,-1)).float()\
                                )[0].item()

                    n = Node(eval,branch)
                    branch.addNode(n)
                    board.pop()
            else:
                for move in list(board.legal_moves):
                    board.push(move)
                    eval = self.net(
                        torch.from_numpy(
                            b_to_array(board).\
                            reshape(1,-1)).float()\
                                )[0].item()

                    n = Node(eval,branch)
                    b = create_branches(board,n,depth-1)
                    n = Node(eval,b)
                    branch.addNode(n)

                    board.pop()


            return branch


        
        game_tree.addBranch(create_branches(board,start_node,self.depth))

        print(game_tree.bestMove())
        print(game_tree.branches)