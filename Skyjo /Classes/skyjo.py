import numpy as np
import random
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox,simpledialog
import gym
from gym import spaces

from Classes.card import Card

class SkyjoEnv(gym.Env):
        def __init__(self,players,human_mode = False):
            '''
            Parameters
            ----------
            players : List
                List containing player instances

            Returns
            -------
            None.
            Initializes the Skyjo environment

            '''
            self.players = players  # List of players in the game


            self.not_done = False # Boolean, as a player's turn can be composed of 2 actions, True if the player has not done all his actions
            self.drew = False
            self.num_players = len(players) # The number of players
            self.action_space = spaces.MultiDiscrete([2,13])
            self.take = 0 # Int representing a global of an action
            self.draw = 1 # Int representing a global of an action
            self.throw = 2 # Int representing a global of an action
            self.defausse = [] # The discard pile, list containing discarded cards
            self.deck_card = Card(5) # First deck_card
            self.reward = 0 # The reward
            self.state = 0
            self.cards_thrown = []
            self.testing = False
            self.cards_known = []
            self.unfinished = True
            self.human_mode = human_mode
            self.columns_made = []
            self.reward2 = 0


            # Deck card initialized as the real game
            de = [-2]*5 + [-1]*10 + [0]*15 + [i for i in range(1,13) for j in range(10)]
            self.deck=[] # The deck, list of cards composing the deck
            for u in de:
                self.deck.append(Card(u))
            self.deck_copy = self.deck.copy()

            self.setup() # Call set up, initialize the env

            # The observation space, created respecting GYM env
            if self.num_players == 1:
                L = [-2,0,-2]+[-2]*12
                H = [12,100,12]+[12]*12
                self.observation_space = spaces.Box(low=np.array(L),high=np.array(H))
                board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
            elif self.num_players == 2:
                #L = [-2,0,-2]+[-2]*12+[0]*12+[-2]*12+[0]*12
                #H = [12,100,12]+[12]*12+[1]*12+[12]*12+[1]*12
                L = [-2,0,-2]+[-2]*12+[-2]*12
                H = [12,100,12]+[12]*12+[12]*12
                self.observation_space = spaces.Box(low=np.array(L),high=np.array(H))
                board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
                board_int,board_bool = self.players[1].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((self.observation,board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
                #score = self.players[1].compute_score(self.mean_value_deck())
                #tiles = len(self.players[1].undiscovered_tiles())
                #self.observation = np.concatenate((self.observation,np.array([score,tiles])))

            # Display variables from tkinter library
            if self.testing:
                self.root = Tk()
                self.canvas = Canvas(self.root, bg="white", height=650, width=1000)

        def id_to_coord(self,id):
            '''
            Parameters
            ----------
            id : INT
                id of the card in a player board, (first, second, third.. card)

            Returns
            -------
            x : INT
                The corresponding row in the numpy array (coordinate)
            y : INT
                The corresponding column in the numpy array (coordinate)

            '''
            x = int(int(id)/4)
            y = int(id)%4
            return x,y

        def mean_value_deck(self):
            '''
            Returns
            -------
            mean : Float

            Returns the mean_value of the unknown cards. By default, it returns 5
            '''
            compt = 0
            n = len(self.deck_copy)
            mean = 5
            for u in self.deck_copy:
                if u.hidden:
                    compt+=u.value
            #mean = compt/n
            return mean


        def coord_to_idx(self,x,y):
            '''
            Parameters
            ----------
            x : INT
                The corresponding row in the numpy array (coordinate)
            y : INT
                The corresponding column in the numpy array (coordinate)

            Returns
            -------
            INT
                id of the card in a player board, (first, second, third.. card)

            '''
            return x*4 + y


        def reset(self):
            '''
            Returns
            -------
            List
                Observation
            Reset the Skyjo Environment and return an initial observation
            Basically doing the same thing as __init__
            '''
            self.defausse = []
            self.cards_thrown = []
            self.drew = False
            self.history = []
            self.state = 0
            self.reward = 0
            self.not_done = False
            self.unfinished = True
            de = [-2]*5 + [-1]*10 + [0]*15 + [i for i in range(1,13) for j in range(10)]
            self.deck=[]
            self.deck_card = Card(5)
            self.cards_known = []
            self.columns_made = []
            self.reward2 = 0
            for u in de:
                self.deck.append(Card(u))
            self.deck_copy = self.deck.copy()
            self.mean_value_deck()
            self.setup()
            if self.num_players == 1:
                L = [-2,0,-2]+[-2]*12+[0]*12
                H = [12,100,12]+[12]*12+[1]*12
                self.observation_space = spaces.Box(low=np.array(L),high=np.array(H))
                board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
            elif self.num_players == 2:
                #L = [-2,0,-2]+[-2]*12+[0]*12+[-2]*12+[0]*12
                #H = [12,100,12]+[12]*12+[1]*12+[12]*12+[1]*12
                #L = [-2,0,-2]+[-2]*12+[-20,0]                 # only score of the opponent
                #H = [12,100,12]+[12]*12+[150,10]
                L = [-2,0,-2]+[-2]*12+[-2]*12               # board of the opponent without booleans
                H = [12,100,12]+[12]*12+[12]*12
                self.observation_space = spaces.Box(low=np.array(L),high=np.array(H))
                board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
                board_int,board_bool = self.players[1].get_board_as_int(self.mean_value_deck())
                self.observation = np.concatenate((self.observation,board_int))
                #self.observation = np.concatenate((self.observation,board_bool))
                #score = self.players[1].compute_score(self.mean_value_deck())
                #tiles = len(self.players[1].undiscovered_tiles())
                #self.observation = np.concatenate((self.observation,np.array([score,tiles])))


            if self.testing :
                self.root = Tk()
                self.canvas = Canvas(self.root, bg="white", height=650, width=1000)
                self.display()
                print('hey')

            return self.observation


        def setup(self):
            '''
            Returns
            -------
            None.
            Starts the game, give cards to players, put one in the discard pile...
            '''
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


        def read_deck(self):
            '''
            Returns
            -------
            None.
            print the content of the deck
            '''
            dic = {"-2" : 0,"-1" : 0,"0" : 0,"1" : 0,"2" : 0,"3" : 0,"4" : 0,"5" : 0,"6" : 0,"7" : 0,"8" : 0,"9" : 0,"10" : 0,"11" : 0,"12" : 0}
            compt=0
            for u in self.deck:
                compt+=1
                dic[str(u.value)]+=1
            print(dic,compt)


        def draw_card(self):
            '''
            Returns
            -------
            card : Card
            Draw a card from the deck

            '''
            if len(self.deck)==0:
                self.deck=self.defausse.copy()
                self.defausse=[]
            card = random.choice(self.deck)
            self.deck.remove(card)

            return card


        def step(self, action):
            #print(self.defausse,action,self.not_done)
            '''
            Parameters
            ----------
            action : list
                The action to be made by the player

            Returns
            -------
            GYM environment requirements for step function
            Observation
                An environment-specific object representing your observation
            Reward : float
                Amount of reward achieved by the previous action
            done : Boolean
                Whether it’s time to reset the environment agai
            dict
                Diagnostic information (useful for debugging)

            '''
            self.reward = -5
            self.reward2 = 0
            init_score = self.players[0].compute_score(self.mean_value_deck()) # Define an initial score


            # Defining/Making actions and updating environment Draw, Take, Throw
            if self.not_done:
                # This means that the agent has already deicided to take/draw
                act = action[1]
                if self.drew:
                    if act<12:
                        ## PLACE DREW CARD ##
                        card_in = self.deck_card
                        x,y = self.id_to_coord(act)
                        card_out = self.players[0].board[x][y]
                        self.replace_card(self.players[0],card_in,card_out,x,y)
                    else:
                        ## DISCOVER CARDS ##
                        card_out = self.deck_card
                        self.cards_thrown.append(card_out.value)
                        possible_tiles = self.players[0].undiscovered_tiles()
                        tile = random.choice(possible_tiles)
                        x,y = self.id_to_coord(tile)
                        card_in = self.players[0].board[x][y]
                        self.replace_card(self.players[0],card_in,card_out,x,y)
                        self.reward = self.deck_card.value - 5
                        self.reward += 4 # Prise de risque

                else:
                    if act<12:
                        ## Place card from discard pile ##
                        card_in = self.deck_card
                        x,y = self.id_to_coord(act)
                        card_out = self.players[0].board[x][y]
                        self.replace_card(self.players[0],card_in,card_out,x,y)
                    else:
                        ## throw the card from discard pile : FORBIDDEN MOVE ##
                        self.defausse.append(self.deck_card)
                        self.reward = -100

                self.not_done = False

            else:
                # draw
                if action[0] == 0:
                    self.deck_card = self.draw_card()
                    self.drew = True
                #take
                elif action[0] == 1:
                    self.deck_card = self.defausse[-1]
                    self.defausse.remove(self.deck_card)
                    self.drew = False
                self.not_done = True
                self.state+=1

            if self.num_players == 1:
                next_card = self.draw_card()
                self.defausse.append(next_card)


            # Erase column if a column contains the same card values
            before = self.players[0].compute_score(self.mean_value_deck())
            flag = self.erase_column(self.players[0])
            after = self.players[0].compute_score(self.mean_value_deck())
            if flag:
                card_value = (before-after)/3
                if card_value <=0:
                    self.reward2 = -50
                else:
                    self.reward2 = 0
                print("I made a column of "+str(card_value))
                self.columns_made.append(card_value)

            # Compute the scores
            end_score = self.players[0].compute_score(self.mean_value_deck())
            if len(self.players) == 2:
                player_score = self.players[1].compute_score(self.mean_value_deck())

            # Reward is computed looking at the score variation before and after the action
            if self.reward == -5:   ## to check that reward != -100 which means forbidden move
                self.reward = (init_score - end_score) + self.reward2


            if self.num_players == 2:
                ## 2 player GAME ##

                if not(self.not_done):
                    if self.human_mode :
                        self.display()
                        self.root.update()
                        self.human_step()
                    else:
                        self.players[1].play_turn(self.deck,self.observation,self.defausse,self.players)
                    board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                    self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                    #self.observation = np.concatenate((self.observation,board_bool))
                    board_int,board_bool = self.players[1].get_board_as_int(self.mean_value_deck())
                    self.observation = np.concatenate((self.observation,board_int))
                    #score = self.players[1].compute_score(self.mean_value_deck())
                    #tiles = len(self.players[1].undiscovered_tiles())
                    #self.observation = np.concatenate((self.observation,np.array([score,tiles])))
                else:
                    board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                    if len(self.defausse)==0:
                        self.observation = np.concatenate((np.array([15,self.state,self.deck_card.value]),board_int))
                    else:
                        self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                    #self.observation = np.concatenate((self.observation,board_bool))
                    board_int,board_bool = self.players[1].get_board_as_int(self.mean_value_deck())
                    self.observation = np.concatenate((self.observation,board_int))
                    #score = self.players[1].compute_score(self.mean_value_deck())
                    #tiles = len(self.players[1].undiscovered_tiles())
                    #self.observation = np.concatenate((self.observation,np.array([score,tiles])))
            else:
                ## 1 player GAME ##
                board_int,board_bool = self.players[0].get_board_as_int(self.mean_value_deck())
                if len(self.defausse)==0:
                    self.observation = np.concatenate((np.array([15,self.state,self.deck_card.value]),board_int))
                else:
                    self.observation = np.concatenate((np.array([self.defausse[-1].value,self.state,self.deck_card.value]),board_int))
                #self.observation = np.concatenate((self.observation,board_bool))

            # Check if the game has ended (One player's board is fully visible or number of steps reached)
            done = self.check_end()

            if done :
                if self.num_players == 1:
                    score = self.players[0].compute_score(self.mean_value_deck())
                    if self.unfinished:
                        self.reward = -100
                    # Set the final reward depending on the final score
                    else :
                        if score > 50 :
                            self.reward = -35
                        elif 50 >score > 30:
                            self.reward = -5
                        elif 30 >score > 15 :
                            self.reward = 0
                        elif 15 >score > 5 :
                            self.reward = 5
                        elif 5 >score > 0 :
                            self.reward = 20
                        else :
                            self.reward = 50
                    reward = self.reward
                    state = self.state
                    cards_thrown = self.cards_thrown
                    observation = self.observation.copy()
                    columns = self.columns_made.copy()
                    self.reset()
                    return observation,reward,done,{"score":score, "turns":state, "thrown":cards_thrown,"columns":columns}
                elif self.num_players == 2:
                    score1 = self.players[0].compute_score2()
                    score2 = self.players[1].compute_score2()

                    # Set the final reward depending on the outcome of the game
                    if score1 < score2 :
                        self.reward = +100
                    elif score1 == score2:
                        self.reward = 0
                    else :
                        self.reward = -100
                    reward = self.reward
                    state = self.state
                    cards_thrown = self.cards_thrown
                    observation = self.observation.copy()
                    columns = self.columns_made.copy()
                    self.reset()
                    return observation,reward,done,{"computer_score":score1,"player_score":score2, "turns":state, "thrown":cards_thrown,"columns":columns}

            else:
                return self.observation,self.reward,done,{}


        def human_step(self):
            '''

            Returns
            -------
            None.
            Let a human player plays againt the computer by using a tkinter window

            '''

            print("Your board" + str(self.players[1].get_board_as_int(5)[0]))
            print("Discard top card : "+str(self.defausse[-1].value))
            answer= messagebox.askyesno("Question","Do you want to draw a card ?")
            print(answer)
            if answer:
                action = "draw"
            else:
                action = "take"
            #action = input("take or draw ?")
            if action == "draw":
                card = self.draw_card()
                #print("The card drawn is :"+str(card.value))
                answer= messagebox.askyesno("Question","You drew a "+str(card.value)+" do you want to keep it ?")
                if answer:
                    use = "keep"
                else:
                    use = "throw"
                #use = input("keep or throw ?")
                if use == "keep":
                    answer = simpledialog.askinteger("Input", "Where do you want to put it ?",
                                 parent=self.root,
                                 minvalue=0, maxvalue=11)
                    x,y = self.id_to_coord(answer)
                    card_in = card
                    card_out = self.players[1].board[int(x)][int(y)]
                else:
                    answer = simpledialog.askinteger("Input", "What card do you want to discover ?",
                                 parent=self.root,
                                 minvalue=0, maxvalue=11)
                    x,y = self.id_to_coord(answer)
                    card_in = self.players[1].board[int(x)][int(y)]
                    card_out = card
            else:
                card_in = self.defausse[-1]
                answer = simpledialog.askinteger("Input", "Where do you want to put it ?",
                             parent=self.root,
                             minvalue=0, maxvalue=11)
                x,y = self.id_to_coord(answer)
                card_out = self.players[1].board[int(x)][int(y)]

            self.replace_card(self.players[1],card_in,card_out,int(x),int(y))
            flag = self.erase_column(self.players[1])



        def replace_card(self,player,card_in,card_out,x,y):
            '''
            Parameters
            ----------
            player : PLAYER
                player with a replacement in his board
            card_in : CARD
                The card to introduce
            card_out : CARD
                The card to replace
            x : INT
                The corresponding row of the card_out (coordinate)
            y : TYPE
                The corresponding row of the card_in (coordinate)

            Returns
            -------
            None.

            '''
            # Add card_out to the defausse
            self.defausse.append(card_out)
            player.board[x][y] = card_in
            player.board[x][y].hidden = False


        def erase_column(self,player):
            '''
            Parameters
            ----------
            player : PLAYER
                player with a column deletion in his board

            Returns
            -------
            None.
            Removes a column if 3 card values in the same column (not hidden) are equal
            '''
            flag = False
            for i in range(4):
                if player.board[0][i].value == player.board[1][i].value == player.board[2][i].value:
                    if player.board[0][i].hidden == player.board[1][i].hidden == player.board[2][i].hidden and not(player.board[2][i].hidden):
                        if player.board[0][i].value != 0:
                            card1 = Card(player.board[0][i].value)
                            card2 = Card(player.board[0][i].value)
                            card3 = Card(player.board[0][i].value)
                            self.defausse.append(card1)
                            self.defausse.append(card2)
                            self.defausse.append(card3)
                            player.board[0][i].value,player.board[1][i].value,player.board[2][i].value = 0,0,0
                            flag = True
            return flag



        def check_end(self):
            '''
            Returns
            -------
            end : BOOLEAN
                True if game is over, False otherwhise

            '''
            end = False
            for player in self.players:
                board_full = True
                # Chech if all card are visible, if Yes game is over
                for rows in player.board:
                    for card in rows:
                        if card.hidden == True:
                            board_full = False
                if board_full:
                    end = True
                    self.unfinished = False
            if self.state>80:
                end = True

            return end


        def display(self):
            '''
            Returns
            -------
            None.
            Display function of the game
            '''

            #Deck
            self.canvas.create_rectangle(400, 50, 470, 150, outline="#fb0")

            #Discard pile
            self.canvas.create_rectangle(530, 50, 600, 150, fill='white')
            self.canvas.create_rectangle(530, 50, 600, 150, outline="#fb0")
            try:
                self.canvas.create_text(565, 100, text = str(self.defausse[-1].value), font=("Purisa", 18))
            except:
                self.canvas.create_text(565, 100, text = str(self.deck_card.value), font=("Purisa", 18))


            player1 = self.players[0]
            player2 = self.players[1]
            player1.display_board(self.canvas, 150, 300)
            player2.display_board(self.canvas, 650, 300)
            self.canvas.create_text(220, 610, text = 'Computer_board', font=("Purisa", 16))
            self.canvas.create_text(700, 610, text = 'Your board', font=("Purisa", 16))
            self.canvas.create_rectangle(330, 600, 380, 620, fill='white')
            self.canvas.create_rectangle(830, 600, 880, 620, fill='white')
            self.canvas.create_rectangle(330, 600, 380, 620, outline="red")
            self.canvas.create_rectangle(830, 600, 880, 620, outline="red")
            self.canvas.create_text(340, 610, text = str(player1.compute_score(self.mean_value_deck())), font=("Purisa", 12))
            self.canvas.create_text(840, 610, text = str(player2.compute_score(self.mean_value_deck())), font=("Purisa", 12))
