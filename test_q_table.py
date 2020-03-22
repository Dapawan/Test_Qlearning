import Q_table
import random
import numpy as np


done = False
state = [0,1,0,0,0,0]
state_size = len(state)
action_size = 2
q_table = Q_table.Q_table(state_size,action_size,0.9,0.9)

for i in range(2000):
    '''
    On fait un jeu ayant 5 cases en lignes
    case 1 : case de depart
    case 0 : recompense 5
    case 2 : recompense 1
    case 3 : recompense 1
    case 4 : recompense 20
    '''
    state = [0,1,0,0,0,0]
    next_state = np.zeros( state_size, )
    reward = 0
    done = False

    while(done == False):
        
        #Random action
        action_rand = random.randint(0,1)
        next_state = np.zeros( state_size, dtype=int )
        action = np.zeros( action_size, )
        action[action_rand] = 1

        posAct = np.argmax( state )

        if( action_rand == 0 ):
            #move backward
            
            if( posAct > 0 ):
                posAct = posAct - 1
            else:
                done = True
                reward = 0
        else:
            #move forward
            if( posAct < ( state_size - 1 ) ):
                posAct = posAct + 1
            else:
                done = True
                reward = 0

        if( posAct == 0 ):
            reward = 5
        elif( posAct == 5 ):
            reward = 30
        else:
            reward = 1

        if( done == False ):
            next_state[posAct] = 1
            q_table.append( state , reward , action , next_state )

        state = next_state

        
q_table.get_q_table(state)