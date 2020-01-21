import gym
from gym import spaces
import numpy as np

import Morpion

class MorpionEnv(gym.Env):
    """description of class"""

    monMorpion = Morpion.Morpion()
    actionIASimulee = np.ndarray(shape=(9, 1),
                    dtype=np.float32)

    def __init__(self):
        #On init le morpion
        self.monMorpion.initPartie()
        #On a 9 actions possibles 
        self.action_space = spaces.Discrete(9)
        #On décrit ce que voit l'agent
        self.observation_space = spaces.Box(low=self.monMorpion.valeurAucunPion,
                                            high=self.monMorpion.valeurPionJ2,
                                            shape=(9,1),
                                            dtype=np.int16)
        self.reward_range = (-200, 200)

        self.current_episode = 0
        self.success_episode = []



    def reset(self):
        self.current_player = 1
        # P means the game is playable, W means somenone wins, L someone lose
        self.state = 'P'
        self.current_step = 0
        self.max_step = 10
        #On init le morpion
        self.monMorpion.initPartie()
        self.world = np.reshape(self.monMorpion.getListePionJ_UN(),[9,1])

        return self._next_observation()

    def _next_observation(self):
        obs = self.world

        #obs = np.append(obs, [[self.current_player, 0, 0, 0]], axis=0)

        return obs

    def _take_action(self, action):

        result = 0
        #On clear les anciens choix
        self.actionIASimulee = np.zeros(9)
        self.actionIASimulee[action] = 1.0

        #On gère les actions suivant le tour du joueur
        if self.current_player == 1:
            result = self.monMorpion.tourJ_UN(self.actionIASimulee)
            #On passe en observation le plateau du joueur suivant
            self.world = np.reshape(self.monMorpion.getListePionJ_DEUX(),[9,1])
        else:
            result = self.monMorpion.tourJ_DEUX(self.actionIASimulee)
            #On passe en observation le plateau du joueur suivant
            self.world = np.reshape(self.monMorpion.getListePionJ_UN(),[9,1])
        
            #On indique si le joueur a perdu ou gagner
            if result == 1:
                #Victoire
                self.state = 'W'
            elif ((result == -2) | (result == -3)) :
                #Position interdite
                self.state = 'L'
            else:
                #On joue
                self.state = 'P'


    def step(self, action):
        self._take_action(action)
        self.current_step += 1
        #print(self.world)

        if self.state == "W":
            print('Player {self.current_player} won')
            reward = 200
            done = True
        elif self.state == 'L':
            print('Player {self.current_player} lost')
            reward = -200
            done = True
        elif self.state == 'P':
            reward = -1
            done = False

        if self.current_step >= self.max_step:
            done = True

        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

        if done:
            self.render_episode(self.state)
            self.current_episode += 1

        obs = self._next_observation()

        return obs, reward, done, {}


    def render_episode(self, win_or_lose):
        self.success_episode.append(
            'Success' if win_or_lose == 'W' else 'Failure')

        file = open('./render.txt', 'a')
        file.write('-------------------------------------------\n')
        file.write('Episode number {self.current_episode}\n')
        file.write('{self.success_episode[-1]} in {self.current_step} steps\n')
        file.write(str(np.reshape(self.world, [3,3])))
        file.close()