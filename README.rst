**Status:** Maintenance (expect minor updates)

Skyjo
**********

This repository presents the implementation of a reinforcement learning agent capable of playing **the card game Skyjo.**

Installation
======

In order to run the code you will need the following libraries : gym , numpy , random, tkinter , stable_baselines3
To install them, please use the following commands :

- pip install gym
- pip install tkinter
- pip install stable_baselines3[extra]


How it works
======

Our code is divided in multiple .py files that represent each class of our environment. We created 3 different classes, the **player** class is written in player.py and described each player in the game. The **card** class is written in card.py and described each card of the deck. The **skyjo** class in skyjo.py is the most important one where the environment is written. Those three classes are in the classes file. In the trained_agents file you can find multiple trained agents that you can load on the main.py file and use them without having to wait for training.

The Environment
======

We implemented an environment that fits the Gym implementation of environments. Therefore, we created the following methods : **reset()** , **step()** 
We did not implement the render method but we do have a display() method that uses tkinter windows but only works for human play at the moment and is not used during training. Some of the parameters we used in the environment are not fixed and you are welcome to play with them.

Main file
======

In order to run training and play with the agent, you can use the main.py file. In there we imported an agent from stable_baseline3 (PPO) and used it for training. As it is right now, all the code for training agents is commented and running the main.py file will let you play some games against an already trained agents.

Please note that the most important lines to initialize our environment are : 

players = [player(True)]   
env = SkyjoEnv(players) 

We also implemented a 2-player environment that is initialized by specifying 2 players in input : 

players = [player(True),player(False]   
env = SkyjoEnv(players) 

Play with parameters
======

In the main.py file you can play with the different parameters that are used for both training and testing. We mainly used 1.000.000 time_steps but you can change this to the value that suits you best.
