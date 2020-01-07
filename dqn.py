# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense,Convolution2D,Flatten,Conv1D,Conv2D
from keras.optimizers import Adam
import EnvJeu
import matplotlib.pyplot
import copy

EPISODES = 10000
play = False

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        if(play):
            self.epsilon = 0.0
        else:
            self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Conv2D(24, kernel_size=1,input_shape=(3, 3, 1),activation='relu'))
        model.add(Conv2D(24, kernel_size=1,activation='relu'))
        model.add(Conv2D(24, kernel_size=1,activation='relu'))
        model.add(Flatten())
        model.add(Dense(20, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = state + [state]
        act_values = self.model.predict(state)
        if(play):
            print("Reward esperee :" + str(np.max(act_values[0])))
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if(done==False):
                next_state = next_state + [next_state]
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            state = state + [state]
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.train_on_batch(state, target_f)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    #env = gym.make('CartPole-v1')
    env = EnvJeu.EnvJeu()
    state_size = 9#env.observation_space.shape[0]
    action_size = 9#env.action_space.n
    agent = DQNAgent(state_size, action_size)
    #agent.load("./morpion-dqn_vs_self_v2.h5")

    #On enregistre quelques parties
    #for i in range(20):
    #    done = False
    #    listeMove = []
    #    state = env.reset()
    #    listeMove.append(copy.copy(state))
    #    state = np.reshape(state, [1, state_size])
    #    while(done == False):
    #        action = agent.act(state)
    #        next_state, reward, done = env.step(action,True,False)
    #        listeMove.append(copy.copy(next_state))

    #        next_state = env.monMorpion.getListePionJ_DEUX()
    #        next_state = np.reshape(next_state, [1, state_size])
    #        state = next_state

    #        if(reward == -50):
    #            done = True
    #            env.monMorpion.enregistrerPartie(np.asarray(listeMove),'MES_PARTIES_1_vs_self.txt',i)
    #            continue

    #        action = agent.act(state)
    #        next_state, reward, done = env.step(action,False,True)
            

    #        next_state = env.monMorpion.getListePionJ_UN()
    #        listeMove.append(copy.copy(next_state))
    #        next_state = np.reshape(next_state, [1, state_size])
    #        state = next_state

    #        if(reward == -50):
    #            done = True

    #        if done:
    #            env.monMorpion.enregistrerPartie(np.asarray(listeMove),'MES_PARTIES_1_vs_self.txt',i)

    #On joue quelques parties
    if(play):
        for i in range(20):
            done = False
            listeMove = []
            state = env.reset()
            print("Partie n° " + str(i))
            env.render()
            state = np.reshape(state, [1, state_size])
            while(done == False):
                action = agent.act(state)
                next_state, reward, done = env.step(action,True,False)
            
                #On affiche le move de l'IA
                env.render()
                if(reward == env.rewardBadPlay):
                    #L'IA fait un mauvais move
                    print("Mauvais move IA")
                    continue


                #On recup le move user
                action = int(input())
                next_state, reward, done = env.step(action,False,False)
                #On affiche le move de l'IA
                env.render()

                #On get les pieces J1
                next_state = env.monMorpion.getListePionJ_UN()
                next_state = np.reshape(next_state, [1, state_size])
                state = next_state
        
            


    scoreTot = 0
    batch_size = (2 * 81)
    cnt = 0
    moyTemp = 0
    cntVictoireIA_temp = 0
    scoreMoy = []
    cntVictoireIA = []
    

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [3, 3,1])
        nbrTour = -1
        done = False
        moyTemp += scoreTot
        scoreTot = 0
        flagWin = False

        if(cnt == 20):
            cnt = 0

            scoreMoy.append(moyTemp / 20.0)
            cntVictoireIA.append(copy.copy(cntVictoireIA_temp))

            moyTemp = 0
            cntVictoireIA_temp = 0
            try :

                fig, ax1 = matplotlib.pyplot.subplots()
            
                ax2 = ax1.twinx()
                ax1.plot(scoreMoy, 'g-')
                ax2.plot(cntVictoireIA, 'b-')
                ax1.set_xlabel('Epochs')
                ax1.set_ylabel('Moyenne score IA')
                ax2.set_ylabel('Nbr victoire IA')
                #matplotlib.pyplot.grid(True)
                matplotlib.pyplot.savefig('Train__self_v4.png')
                matplotlib.pyplot.close()

            except :
                print("Erreur")


        while(done == False):
            #env.render()
            nbrTour += 1
            action = agent.act(state)
            next_state, reward, done = env.step(action,True,False)
            scoreTot += reward

            if(reward == env.rewardWin):
                flagWin = True

            #reward = copy.copy(scoreTot)
            next_state = np.reshape(next_state, [3, 3,1])
            agent.memorize(copy.copy(state), copy.copy(action), copy.copy(reward), copy.copy(next_state), copy.copy(done))
            state = next_state

            if done:
                cnt +=1
                print("episode: {}/{}, nbr tour: {}, reward: {}, victoireIA : {} e: {:.2}"
                      .format(e, EPISODES, nbrTour, scoreTot, flagWin,agent.epsilon))
                #print("episode : " + str(e) + "/" + str(EPISODES) + " reward : " + str(scoreTot))
                if(flagWin):
                    cntVictoireIA_temp += 1
                    agent.save("./morpion-dqn_vs_self_v4.h5")
                break
            if len(agent.memory) > batch_size:
                #print("DEBUT Replay")
                agent.replay(batch_size)
                #agent.memory.clear()
                #print("FIN Replay")

            if(reward == env.rewardBadPlay):
                done = True
                continue


            #On gère le jeu adverse
            state = env.monMorpion.getListePionJ_DEUX()
            state = np.reshape(state, [3, 3,1])
            epsilonOld = agent.epsilon
            #Permet de changer un peu les move
            agent.epsilon = 0.5
            action = agent.act(state)
            #On remet la valeur save
            agent.epsilon = epsilonOld
            next_state, reward, done = env.step(action,False,False)
            next_state = np.reshape(next_state, [3, 3,1])
            agent.memorize(copy.copy(state), copy.copy(action), copy.copy(reward), copy.copy(next_state), copy.copy(done))

            if(reward == env.rewardBadPlay):
                done = True
                continue

            next_state = env.monMorpion.getListePionJ_UN()
            #conversion du state
            next_state = np.reshape(next_state, [3, 3,1])
            state = next_state

            


        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")