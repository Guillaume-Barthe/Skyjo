import gym
from Classes.card import Card
from Classes.player import player
from Classes.skyjo import SkyjoEnv
from tkinter import *
import random
import time

def better_policy(env):
    card = env.defausse[-1]
    board = env.players[0].board
    unknown_cards = []
    for i in range(3):
        for j in range(4):
            if board[i][j].hidden == True:
                unknown_cards.append(i*4+j)


    if card.value < 2:
        action = 'take_'+str(random.choice(unknown_cards))
    else:
        action = 'draw_'+str(random.choice(unknown_cards))

    return action

players = [player(True)]
env = SkyjoEnv(players)
env.reset()
for _ in range(1000):
    #env.render()
    action = better_policy(env)
    env.step(action) # take a random action
env.close()
