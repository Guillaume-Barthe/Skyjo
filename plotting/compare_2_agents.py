from Classes.skyjo import SkyjoEnv
import matplotlib.pyplot as plt
from Classes.player import player
import numpy as np


def compare_on_n_games(model1,model2,env,env2,n_games = 100):
    '''
    Compare the results of 2 trained agents on n_games and plot the results.
    '''
    compteur1 = 0
    compteur2 = 0
    Score1 = []
    Turns1 = []
    Score2 = []
    Turns2 = []
    thrown1 = [0]*15
    thrown2 = [0]*15
    T1 = []
    T2 = []
    X = [i+1 for i in range(n_games)]
    #players = [player(True)]
    #env = SkyjoEnv(players)
    obs = env.reset()
    while compteur1 < n_games:
        obs = env.reset()
        compteur1 +=1
        print("\r" + str(compteur1), end = ' ')
        n_steps = 170
        for step in range(n_steps):
          action, _ = model1.predict(obs, deterministic=True)
          obs, reward, done, info = env.step(action)
          if compteur1 == n_games:
              print(obs,info,reward)
          if done:
            #print("Goal reached!", "reward=", reward)
            Score1.append(info['score'])
            #print(env.players[0].compute_score())
            Turns1.append(info['turns'])
            T1 += info['columns']
            obs = env.reset()
            break


    while compteur2 < n_games:
        obs = env2.reset()
        compteur2 +=1
        print("\r" + str(compteur2), end = ' ')
        n_steps = 170
        for step in range(n_steps):
          action, _ = model2.predict(obs, deterministic=True)
          obs, reward, done, info = env2.step(action)
          if compteur2  == n_games:
              print(obs,info,reward)
          if done:
            #print("Goal reached!", "reward=", reward)
            Score2.append(info['score'])
            Turns2.append(info['turns'])
            T2 += info['columns']
            obs = env2.reset()
            break

    for u in T1:
        thrown1[int(u)+2]+=1
    for u in T2:
        thrown2[int(u)+2]+=1
    print("column1 = ",thrown1,"column2 = ",thrown2)
    mean_score1 = np.mean(Score1)
    mean_score2 = np.mean(Score2)
    print(mean_score1,mean_score2)
    title = 'Comparison of the score of 2 agents on ' +str(n_games)+" games "
    plt.figure()
    plt.scatter(X,Score1,label='With choice (timesteps = 1.000.000)')
    plt.scatter(X,Score2,label='Without choice (timesteps = 1.000.000)')
    plt.plot([X[0],X[-1]],[mean_score1,mean_score1],label='mean_score model 1')
    plt.plot([X[0],X[-1]],[mean_score2,mean_score2],label='mean_score model 2')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.title(title)
    plt.legend()
    plt.show()

    mean_turns1 = np.mean(Turns1)
    mean_turns2 = np.mean(Turns2)
    print(mean_turns1,mean_turns2)
    title = 'Comparison of the number of turns taken by 2 agents on ' +str(n_games)+" games "

    plt.figure()
    plt.scatter(X,Turns1,label='With choice (timesteps = 1.000.000)')
    plt.scatter(X,Turns2,label='Without choice (timesteps = 1.000.000)')
    plt.plot([X[0],X[-1]],[mean_turns1,mean_turns1],label='mean_turns model 1')
    plt.plot([X[0],X[-1]],[mean_turns2,mean_turns2],label='mean_turns model 2')
    plt.xlabel('Number of Games')
    plt.ylabel('Number of turns')
    plt.title(title)
    plt.legend()
    plt.show()

    title = 'Number of columns made on ' +str(n_games)+" games "

    labels = [str(i) for i in range(-2,13)]
    #men_means = [20, 34, 30, 35, 27]
    #women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, thrown1, width, label='Agent with bonus trained on 500K iterations')
    rects2 = ax.bar(x + width/2, thrown2, width, label='Agent without bonus on 500K iterations')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of columns made')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()

def multi_compare_on_n_games(model1,model2,env,env2,n_games = 100):
    '''
    Compare the results of 2 trained multiplayer agents on n_games and plot the results.
    '''
    L = [model1,model2]
    e = [env,env2]
    R1 = []
    R2 = []
    mean_a = []
    mean_cpu = []
    labels=["Against normal human" , "against risky human"]
    for i in range(len(L)):
        model = L[i]
        env = e[i]

        n_steps = 170
        compteur = 0
        V = [0,0,0]
        Score1 = []
        Score2 = []
        while compteur < n_games:
            compteur+=1
            print("\r" + str(compteur), end = ' ')
            obs = env.reset()
            #print(compteur)
            for step in range(n_steps):
              action1, _ = model.predict(obs, deterministic=True)
              obs, reward, done, info = env.step(action1)
              if compteur == n_games:
                  print(obs,info)

              if done:

                computer_score = info['computer_score']
                player_score = info['player_score']
                if computer_score < player_score:
                    V[0]+=1
                elif computer_score > player_score:
                    V[1]+=1
                else:
                    V[2]+=1
                Score1.append(computer_score)
                Score2.append(player_score)
                break

        mean_score1,mean_score2 = np.mean(Score1),np.mean(Score2)
        mean_cpu.append(mean_score1)
        mean_a.append(mean_score2)
        R1.append(V[0])
        R2.append(V[1])

        #labels.append('Model'+str(i))

    title = 'Number of wins against the  human player on ' +str(n_games)+" games "
    x = np.arange(len(labels))  # the label locations
    width = 0.20  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, R1, width, label='Computer wins')
    rects2 = ax.bar(x + width/2, R2, width, label='Player wins')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of wins')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
