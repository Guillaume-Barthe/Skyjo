## Compare solo/multiplayer agents on n_games ##
import os
import gym
import numpy as np
import matplotlib.pyplot as plt
import random
import time

from stable_baselines3 import A2C,PPO
from stable_baselines3.common.monitor import Monitor
from Classes.card import Card
from Classes.player import player
from Classes.skyjo import SkyjoEnv
from Classes.skyjobis import SkyjoEnv2
from tkinter import *
from plotting.save_model import SaveOnBestTrainingRewardCallback,plot_results2,plot_results
from plotting.compare_2_agents import compare_on_n_games,multi_compare_on_n_games
from tkinter import messagebox,simpledialog

## NECESSARY FOR MAC USERS
#os.environ['KMP_DUPLICATE_LIB_OK']='True'

gamma = 0.99


#Create the files for training logs

log_dir = "./trained_models/"
os.makedirs(log_dir, exist_ok=True)
log_dir2= "./trained_models/"
os.makedirs(log_dir, exist_ok=True)

########################### Script to play games against a trained agent ###########################

players = [player(True),player(False)]
env = SkyjoEnv(players,human_mode = True)
env.testing = True
model = PPO.load((os.path.join(log_dir, 'PPO_1M_multi')))

n_games = 5
compteur = 0


while compteur < n_games:
    compteur+=1
    obs = env.reset()
    env.display()
    env.canvas.pack()
    env.root.update()
    n_steps = 170
    for step in range(n_steps):
      time.sleep(1)
      action1, _ = model.predict(obs, deterministic=True)
      actions = [action1]
      for action in actions:

         if step % 2 == 0 :
              if action[0]:
                 text = "CPU : I saw a " + str(obs[0])+ " on the discard pile and I decided to take it "
                 print(text)
                 env.canvas.create_text(500, 200, text = text, font=("Purisa", 16))
              else:
                 text = "CPU : I saw a " + str(obs[0])+ " on the discard pile and I decided to draw"
                 print(text)
                 env.canvas.create_text(500, 200, text = text, font=("Purisa", 16))
         else:
              if action[1]==12:
                 text = "CPU : I decided to throw the "+str(obs[2])+ " and discover a new card"
                 print(text)
                 env.canvas.create_text(500, 200, text = text, font=("Purisa", 16))
              else:
                 text = "CPU : I put the "+ str(obs[2])+ " at position " + str(action[1])
                 print(text)
                 env.canvas.create_text(500, 200, text = text, font=("Purisa", 16))
      env.display()
      env.root.update()
      time.sleep(1)
      env.canvas.create_rectangle(180, 180, 800, 210, fill='white',outline="white")
      obs, reward, done, info = env.step(action1)
      if done:
        computer_score = info['computer_score']
        player_score = info['player_score']
        if computer_score < player_score:
            answer= messagebox.askyesno("Question","Sorry.. you lost "+str(computer_score)+" to "+str(player_score)+" :( "+" next game ?")
        elif computer_score > player_score:
            answer= messagebox.askyesno("Question","Well done ! you won "+str(player_score)+" to "+str(computer_score)+" :D "+" next game ?")
        else:
            answer= messagebox.askyesno("Question","It's a draw ! "+str(player_score)+" to "+str(computer_score)+" :) "+" next game ?")
        if answer:
            pass
        else:
            compteur = n_games
        break

########################### Script to train an agent on 1-player env and plot the learning curves ###########################

#players = [player(True)]
#env = SkyjoEnv(players)
#env = Monitor(env, log_dir)
#callback = SaveOnBestTrainingRewardCallback(check_freq=1000,name = 'your_model_name', log_dir=log_dir)
#model = PPO('MlpPolicy', env, verbose=0, gamma = gamma)
#model.learn(total_timesteps=int(5e3), callback=callback)
#plot_results(log_dir,log_dir2)

########################### Script to train an agent on multi-player env and plot the learning curves ###########################

#players = [player(True),player(False)]
#env2 = SkyjoEnv(players)
#env2 = Monitor(env2, log_dir2)
#callback2 = SaveOnBestTrainingRewardCallback(check_freq=1000,name = "your_model_name2", log_dir=log_dir2)
#model2 = PPO('MlpPolicy', env2, verbose=0, gamma = gamma)
#model2.learn(total_timesteps=int(5e3), callback=callback2)


########################### Script to compare two agents on 1-player env and plot the comparison ###########################

#players = [player(True)]
#env = SkyjoEnv(players)
#model= PPO.load(os.path.join(log_dir, 'PPO_1M_solo'))
#env2 = SkyjoEnv(players)
#model2= PPO.load(os.path.join(log_dir2, 'PPO_100K_solo'))
#compare_on_n_games(model,model2,env,env2,n_games=10)

########################### Script to compare two agents on 1-player env and plot the comparison ###########################

#players = [player(True),player(False)]
#env = SkyjoEnv(players)
#model= PPO.load(os.path.join(log_dir, 'PPO_1M_multi'))
#env2 = SkyjoEnv(players)
#model2= PPO.load(os.path.join(log_dir, 'A2C_1M_multi'))
#multi_compare_on_n_games(model,model2,env,env2,n_games=10)
