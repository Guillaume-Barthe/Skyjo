import numpy as np
import random
import matplotlib.pyplot as plt
from tkinter import *
import gym

from Classes.card import Card

class SkyjoEnv(gym.Env):

        def __init__(self,players):
            "Initialize the board, the deck of cards, create a visible_board seen by the algo and the actual board to know what cards were drawn out of the deck "
            self.players = players
            self.action_space = ["take_0","take_1","take_2","take_3","take_4","take_5","take_6","take_7","take_8","take_9","take_10","take_11"]
            self.action_space += ["draw_0","draw_1","draw_2","draw_3","draw_4","draw_5","draw_6","draw_7","draw_8","draw_9","draw_10","draw_11"]
            self.action_space += ["throw_0","throw_1","throw_2","throw_3","throw_4","throw_5","throw_6","throw_7","throw_8","throw_9","throw_10","throw_11"]
            self.action_space = np.array(self.action_space)
            self.defausse = []
            self.history = []
            self.reward = 5
            self.state = 0
            de = [-2]*5 + [-1]*10 + [0]*15 + [i for i in range(1,13) for j in range(10)]
            self.deck=[]
            for u in de:
                self.deck.append(Card(u))

            self.setup()
            self.observations = np.array([card.value for card in self.defausse] + [self.state] +\
                [player.get_board_as_int() for player in self.players])

            # Display

            self.root = Tk()
            self.canvas = Canvas(self.root, bg="white", height=650, width=1000)

        def id_to_coord(self,id):
            x = int(int(id)/4)
            y = int(id)%4
            return x,y

        def reset(self):
            self.defausse = []
            self.history = []
            self.state = 0
            de = [-2]*5 + [-1]*10 + [0]*15 + [i for i in range(1,13) for j in range(10)]
            self.deck=[]
            for u in de:
                self.deck.append(Card(u))

            self.setup()
            self.observations = np.array([card.value for card in self.defausse] + [self.state] +\
                [player.get_board_as_int() for player in self.players])

            return self.observations


        def setup(self):
            for player in self.players:
                cards = random.sample(self.deck,12)    #Choose 12 cards from the deck
                for num in cards:
                    self.deck.remove(num)         #Remove them from the deck
                u = np.array(cards)
                board = np.reshape(u,(3,4))    #Initialize the board of the algorithm
                player.board = board
                player.init_board()
            card = self.draw_card()
            self.defausse.append(card)


        def draw_card(self):
            card = random.choice(self.deck)
            self.deck.remove(card)
            return card

        def step(self, action):
            #["take_0","take_1","take2","take3","take4","take5","take6","take7","take8","take9","take10","take11"]
            #test = ["draw0","draw1","draw2","draw3","draw4","draw5","draw6","draw7","draw8","draw9","draw10","draw11"]
            #test2 = ["throw0","throw1","throw2","throw3","throw4","throw5","throw6","throw7","throw8","throw9","throw10","throw11"]

            action = action.split('_')
            end_digit = action[1]
            action_word = action[0]
            if action_word == "take":
                card_in = self.defausse[-1]
                x,y = self.id_to_coord(end_digit)
                card_out = self.players[0].board[x][y]
                self.replace_card(self.players[0],card_in,card_out,x,y)
            elif action_word == "draw":
                card_in = self.draw_card()
                x,y = self.id_to_coord(end_digit)
                card_out = self.players[0].board[x][y]
                self.replace_card(self.players[0],card_in,card_out,x,y)
            elif action_word == "throw":
                card_out = self.draw_card()
                x,y = self.id_to_coord(end_digit)
                card_in = self.players[0].board[x][y]
                self.replace_card(self.players[0],card_in,card_out,x,y)

            done = self.check_end()

            if done :
                score = self.players[0].compute_score()
                print('The game has ended, player_score = ' +str(score)+' and it took '+str(self.state)+ ' turns')
                self.reward += (5-score)**3
                print('reward is '+ str(self.reward))
                self.reset()
            else:
                self.reward -=0.5

            self.state+=1
            self.observations = np.array([card.value for card in self.defausse] + [self.state] +\
                        [player.get_board_as_int() for player in self.players])

            return self.observations,self.reward,done,{}

        def human_step(self, state, action):
            self.state+=1
            self.history.append({"turn":self.state , "player_score":self.players[0].compute_score()})
            print(self.history)
            if action == "draw":
                card = self.draw_card()
                print("The card drawn is :"+str(card.value))
                use = input("keep or throw ?")
                if use == "keep":
                    x = input("what x to put it ?")
                    y = input("what y to put it ?")
                    card_in = card
                    card_out = self.players[0].board[int(x)][int(y)]
                else:
                    x = input("what x to discover ?")
                    y = input("what y to discover ?")
                    card_in = self.players[0].board[int(x)][int(y)]
                    card_out = card
            else:
                card_in = self.defausse[-1]
                x = input("what x to put it ?")
                y = input("what y to put it ?")
                card_out = self.players[0].board[int(x)][int(y)]
            return card_in,card_out,x,y

        def replace_card(self,player,card_in,card_out,x,y):
            self.defausse.append(card_out)
            player.board[x][y] = card_in
            player.board[x][y].hidden = False

        def erase_column(self,player):
            for i in range(4):
                if player.board[0][i].value == player.board[1][i].value == player.board[2][i].value:
                    if player.board[0][i].hidden == player.board[1][i].hidden == player.board[2][i].hidden and not(player.board[2][i].hidden):
                        player.board[0][i].value,player.board[1][i].value,player.board[2][i].value = 0,0,0
                        self.defausse.append(player.board[0][i])
                        self.defausse.append(player.board[1][i])
                        self.defausse.append(player.board[2][i])


        def check_end(self):
            end = False
            for player in self.players:
                board_full = True
                for rows in player.board:
                    for card in rows:
                        if card.hidden == True:
                            board_full = False
                if board_full:
                    end = True
            #print("check_end = "+str(end))
            return end

        def display(self):

            #Deck
            self.canvas.create_rectangle(400, 50, 470, 150, outline="#fb0")

            #Discard pile
            self.canvas.create_rectangle(530, 50, 600, 150, fill='white')
            self.canvas.create_rectangle(530, 50, 600, 150, outline="#fb0")
            self.canvas.create_text(565, 100, text = str(self.defausse[-1].value), font=("Purisa", 18))


            for player in self.players:
                player.display_board(self.canvas, 385, 300)
