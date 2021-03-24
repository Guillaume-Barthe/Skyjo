import numpy as np
import random
from Classes.card import Card
import matplotlib.pyplot as plt
from tkinter import *

class player:
    def __init__(self, is_machine):
        self.line = 3
        self.column = 4
        self.board = [[]]
        self.is_machine = is_machine
        self.score = -99

    def init_board(self):
        coord = random.sample([i for i in range(12)], 2)
        for co in coord:
            self.board[int(co/self.column)][co%self.column].hidden = False

    def display_board(self, canvas, x_s, y_s):
            for i in range(self.line):
                for j in range(self.column):
                    canvas.create_rectangle(x_s + (j * 60), y_s + i*100,
                                            x_s + (j * 60) + 50 , y_s + i*100 + 90, outline="#fb0")

                    mycard = self.board[i][j]
                    if not mycard.hidden:
                        canvas.create_rectangle(x_s + (j * 60), y_s + i*100,
                                                x_s + (j * 60) + 50 , y_s + i*100 + 90, fill = 'white')
                        canvas.create_text((x_s + (j * 60) + 25, y_s + i*100 + 45),
                                           text = str(mycard.value), font=("Purisa", 18))
                        
    def get_board_as_int(self):
        board_int = np.zeros((self.line, self.column))
        for i in range(self.line):
                for j in range(self.column):
                    if self.board[i][j].hidden:
                        board_int[i][j] = None
                    else:
                        board_int[i][j] = self.board[i][j].value
        return board_int


    def compute_score(self):
        score = 0
        for row in self.board:
            for card in row:
                if card.hidden:
                    score += 5    #When the card hidden we add the average which is 5
                else:
                    score += card.value
        return score

    def __repr__(self):
        for row in self.board:
            for card in row:
                print(card)
        return ""
