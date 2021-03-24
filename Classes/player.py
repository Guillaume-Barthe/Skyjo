### This is the implementation of the player class. ###


import numpy as np
import random
from Classes.card import Card
import matplotlib.pyplot as plt
from tkinter import *
from stable_baselines3 import A2C,PPO
import os


class player:
    '''
    A player object describes the player and his board. The player can either be a is_machine
    or a human and has a board of size 3*4.

    The repr method enables the print(card) command and tells the user the values
    of each attribute of the card
     '''

    def __init__(self, is_machine,is_trained = False,model_name = ''):
        self.line = 3
        self.column = 4
        self.board = [[]]
        self.is_machine = is_machine
        self.is_trained = is_trained
        self.model_name = model_name
        self.score = -99

    def init_board(self):
        '''
        Returns
        -------
        None.
        init_board just inits the player board randomly when starting the game

        '''
        coord = random.sample([i for i in range(12)], 2)
        for co in coord:
            self.board[int(co/self.column)][co%self.column].hidden = False


    def get_board_as_int(self,mean_value):
        '''
        Parameters
        ----------
        mean_value : Float
            Takes the mean_value of unknown cards remaining in the deck as input,
            most of the time we kept it to 5.

        Returns
        -------
        TYPE : numpy array
            Returns a numpy array with the same size of player's board (3x4)
            This array contains card values (int) for 'not_hidden' cards.
            Hidden cards values are represented by 5, which is the mean of all
            card values in the game.

        '''
        board_int = []
        board_bool = []
        for row in self.board:
            for card in row:
                if card.hidden:
                    # Represent card value to 5
                    board_int.append(round(mean_value,2))
                    board_bool.append(0)
                else:
                    board_int.append(card.value)
                    board_bool.append(1)

        return np.array(board_int),np.array(board_bool)

    def undiscovered_tiles(self):
        '''
        Returns
        -------
        TYPE : list
            Returns a list of coordinates corresponding to the tiles that are still
            hidden.
        '''

        tiles = []
        compteur = 0
        for row in self.board:
            for card in row:
                if card.hidden:
                    tiles.append(compteur)
                compteur+=1
        return tiles

    def max_tile(self):
        '''
        Returns
        -------
        TYPE : int
            Returns the maximum value of the cards in a player's board
        '''
        max = -2
        for row in self.board:
            for card in row:
                if card.value > max:
                    max = card.value
        return max


    def count_vis_cards(self):
        '''
        Returns
        -------
        compt : INT
            Returns the number of visible cards in a player's board

        '''
        compt = 0
        for row in self.board:
            for card in row:
                if not(card.hidden):
                    compt+=1
        return compt

    def compute_score(self,average):
        '''
        Returns
        -------
        score : INT
            The sum of all card's value of a player's board. If card is hidden
            we suppose the value of the card is 5, which the mean of all card
            values in the game

        '''
        score = 0
        for row in self.board:
            for card in row:
                if card.hidden:
                    score += average    #When the card hidden we add the average which is 5
                else:
                    score += card.value
        return score

    def compute_score2(self):
        '''
        Returns
        -------
        score : INT
            The sum of all card's value of a player's board even if some cards are hidden

        '''
        score = 0
        for row in self.board:
            for card in row:
                score += card.value
        return score

    def play_turn(self,deck,observation,defausse,players,human_value = 3):
        '''
        Parameters
        ----------
        deck : Object
            Takes the deck as input

        observation : numpy array
            Takes the actual observation as input

        defausse :
            Takes the discard pile as input

        players :
            Takes the players of the game as input

        Returns
        -------
        TYPE : None

        This function does not return anything, it modifies the actual player's board,
        this method enables a player to play againt the computer. During training phase,
        this functions implements a human-made policy or let an already trained model to play.

        '''

        if self.is_machine:
            return
        else:
            if self.is_trained:
                model = PPO.load(os.path.join("./gym/", self.model_name))
                board_int,board_bool = self.get_board_as_int(5)
                observation = np.concatenate((np.array([observation[0],observation[1],5]),board_int))
                observation = np.concatenate((observation,board_bool))
                score = players[0].compute_score(5)
                tiles = len(players[0].undiscovered_tiles())
                observation = np.concatenate((observation,np.array([score,tiles])))
                action, _ = model.predict(observation, deterministic=True)
                if action[0] == 0:
                    if len(deck)==0:
                        deck=defausse.copy()
                        defausse=[]
                    card = random.choice(deck)
                    deck.remove(card)
                    drew = True

                elif action[0] == 1:
                    card = defausse[-1]
                    defausse.remove(card)
                    drew = False
                observation = np.concatenate((np.array([defausse[-1].value,observation[1],card.value]),board_int))
                observation = np.concatenate((observation,board_bool))
                observation = np.concatenate((observation,np.array([score,tiles])))
                action2, _ = model.predict(observation, deterministic=True)
                act = action2[1]
                if drew:
                    if act<12:
                        ## PLACE DREW CARD ##
                        card_in = card
                        x = int(int(act)/4)
                        y = int(act)%4
                        card_out = self.board[x][y]
                        defausse.append(card_out)
                        self.board[x][y] = card_in
                        self.board[x][y].hidden = False

                    else:
                        ## DISCOVER CARDS ##
                        card_out = card
                        possible_tiles = self.undiscovered_tiles()
                        tile = random.choice(possible_tiles)
                        x = int(int(tile)/4)
                        y = int(tile)%4
                        card_in = self.board[x][y]
                        defausse.append(card_out)
                        self.board[x][y] = card_in
                        self.board[x][y].hidden = False
                else:
                    if act<12:
                        card_in = card
                        x = int(int(act)/4)
                        y = int(act)%4
                        card_out = self.board[x][y]
                        defausse.append(card_out)
                        self.board[x][y] = card_in
                        self.board[x][y].hidden = False

                    else:
                        defausse.append(card)
                        reward = -100
                return
            else:
                discard = defausse[-1]
                #print()
                board = list(self.get_board_as_int(5))[0]
                max = -2
                imax = 0
                for i in range(len(board)):
                    if board[i]>max:
                        max = board[i]
                        imax = i
                if discard.value <= human_value :
                    card = defausse[-1]
                    defausse.remove(card)
                    card_in = card
                    x = int(int(imax)/4)
                    y = int(imax)%4
                    card_out = self.board[x][y]
                    defausse.append(card_out)
                    self.board[x][y] = card_in
                    self.board[x][y].hidden = False
                else:
                    if len(deck)==0:
                        deck=defausse.copy()
                        defausse=[]
                    card = random.choice(deck)
                    deck.remove(card)
                    if card.value <= human_value :
                        card_in = card
                        x = int(int(imax)/4)
                        y = int(imax)%4
                        card_out = self.board[x][y]
                        defausse.append(card_out)
                        self.board[x][y] = card_in
                        self.board[x][y].hidden = False
                    else:
                        if card.value < max:
                            card_in = card
                            x = int(int(imax)/4)
                            y = int(imax)%4
                            card_out = self.board[x][y]
                            defausse.append(card_out)
                            self.board[x][y] = card_in
                            self.board[x][y].hidden = False
                        else :
                            card_out = card
                            possible_tiles = self.undiscovered_tiles()
                            tile = random.choice(possible_tiles)
                            x = int(int(tile)/4)
                            y = int(tile)%4
                            card_in = self.board[x][y]
                            defausse.append(card_out)
                            self.board[x][y] = card_in
                            self.board[x][y].hidden = False



    def display_board(self, canvas, x_s, y_s):
        '''
        Parameters
        ----------
        canvas : Tkinter canvas
            Canvas from tkinter librabry enabling us to display elements
        x_s : INT
            The x coordinate where the player board (top-left corner) should be
            positionned
        y_s : INT
            The y coordinate where the player board (top-left corner) should be
            positionned

        Returns
        -------
        None.

        '''
        for i in range(self.line):
            for j in range(self.column):
                # Creating series of rectangle and adding it to canvas
                # This will be the cards
                canvas.create_rectangle(x_s + (j * 60), y_s + i*100,
                                        x_s + (j * 60) + 50 , y_s + i*100 + 90, outline="#fb0")

                mycard = self.board[i][j]
                if not mycard.hidden:
                    # Adding the value of cards, on cards, if cards not hidden
                    canvas.create_rectangle(x_s + (j * 60), y_s + i*100,
                                        x_s + (j * 60) + 50 , y_s + i*100 + 90, fill = 'white')
                    canvas.create_text((x_s + (j * 60) + 25, y_s + i*100 + 45),
                                        text = str(mycard.value), font=("Purisa", 18))
                else:
                    canvas.create_rectangle(x_s + (j * 60), y_s + i*100,
                                        x_s + (j * 60) + 50 , y_s + i*100 + 90, fill = 'white')

    def __repr__(self):
        '''
        The repr method enables to print the whole board of a player.

        Returns
        -------
        String : repr method needs string as output

        '''
        for row in self.board:
            for card in row:
                print(card)
        return ""
