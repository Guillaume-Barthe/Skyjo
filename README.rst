**Status:** Maintenance (expect bug fixes and minor updates)

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

Our code is divided in multiple .py files that represent each class of our environment. We created 3 different classes, the **player** class is written in player.py and described each player in the game. The **card** class is written in card.py and described each card of the deck. The **skyjo** class in skyjo.py is the most important one where the environment is written.

The Environment
======

We implemented an environment that fits the Gym implementation of environments. Therefore, we created the following methods : **reset()** , **step()** 
We did not implement the render method yet but we do have a display() method that uses tkinter windows but only works for human play at the moment and is not used during training.

Main file
======

In order to run training and play with the agent, you can use the main.py file. In there we imported an agent from stable_baseline3 (PPO) and used it for training. Please note that the lines to initialize our environment are : 

players = [player(True)]
env = SkyjoEnv(players)

We are currently working on implementing multiple players but for now the code only runs with one robot player playing alone.

Play with parameters
======

In the main.py file you can play with the different parameters that are used for both training and testing. We mainly used 500.000 time_steps but you can change this to the value that suits you best.
