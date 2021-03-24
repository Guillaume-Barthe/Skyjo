from Classes.card import Card
from Classes.player import player
from Classes.skyjo import SkyjoEnv
from tkinter import *
import random
import time


#random.seed(15)
players = [player(True)]
game = SkyjoEnv(players)
print(game.id_to_coord(8))

for p in game.players:              #Print the cards of the players to see if it works
    p.score = p.compute_score()
    print(p.get_board_as_int())
    print(p.score)
    print(p)


game.display()
game.canvas.pack()
game.root.update()


while not(game.check_end()):
    for player1 in players:

        state = game.state
        print("Turn : " + str(state+1))
        action = input("take or draw ?")
        card_in,card_out,x,y = game.human_step(state,action)
        print(type(card_in))
        game.replace_card(players[0],card_in,card_out,int(x),int(y))
        game.erase_column(player1)
        #print(game.defausse)
        next_card = game.draw_card()
        game.defausse.append(next_card)
        game.display()
        game.root.update()

print('The game has ended, your score is : '+str(player1.compute_score()))


game.root.mainloop()
