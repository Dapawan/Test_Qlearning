import numpy as np

class Q_table:

    SIZE_MAX_LISTS = 10_000 

    def __init__(self , state_size , action_size , discount_rate , learning_rate ):
        self.state_size     = state_size
        self.action_size    = action_size

        self.discount_rate      = discount_rate
        self.learning_rate      = learning_rate

        #Clear input/output table
        self.reset()

    def reset(self):
        #state_table
        self.input_table    = []
        #Output q table
        self.q_table        = []

    #return index of source_array on source_list --> If it doesn't exist return -1
    def get_index_array(self, source_array, source_list):
        for i in range( len(source_list) ):
            if( np.array_equal( source_list[i] , source_array )  ):
                #These 2 arrays are the same
                return i
        #This array doesn't exist yet
        return -1

    #Return the q table from this state
    def get_q_table(self , state ):
        index_state = self.get_index_array( state , self.input_table )
        if( index_state == -1 ):
            return -1
        else:
            return self.q_table[index_state]

    #Set value of _table between 0 to 100.0
    def normalize_q_table(self):
        max_value = np.max( self.q_table )

        self.q_table = ( self.q_table / max_value ) * 100.0

        #Convert array to list
        self.q_table = list( self.q_table )

    #Return -1 if size exceeded and 0 if all good
    def append(self , last_state , reward , action , next_state):
        index_last_state = self.get_index_array( last_state , self.input_table )
        if( index_last_state == -1  ):
            
            #We have exceed the size max
            if( len( self.input_table ) >= self.SIZE_MAX_LISTS ):
                return -1

            #This state doesn't exist we add it
            self.input_table.append(last_state)
            #We add too a Q_table filled with zeros
            self.q_table.append( np.zeros( self.action_size , )  )
            #Get index
            index_last_state = len( self.input_table ) - 1


        #Get values 
        q_actual_value = self.q_table[index_last_state][np.argmax( action )]
        #Max value of the next_state
        q_max_value = 0
        index_next_state = self.get_index_array( next_state , self.input_table )
        if( index_next_state != -1 ):
            q_max_value = np.amax( self.q_table[index_next_state] )
        else:
            #We have exceed the size max
            if( len( self.input_table ) >= self.SIZE_MAX_LISTS ):
                return -1

            #This state doesn't exist we add it
            self.input_table.append(next_state)
            #We add too a Q_table filled with zeros
            self.q_table.append( np.zeros( self.action_size , )  )
            #Get index
            index_next_state = len( self.input_table ) - 1


        #New q_value
        #new_q_value = q_actual_value + self.learning_rate * ( reward + ( self.discount_rate * q_max_value ) - q_actual_value )
        new_q_value = ( reward + ( self.discount_rate * q_max_value ) )
        #refresh q_value
        self.q_table[index_last_state][np.argmax( action )] = new_q_value

        #We normalize the q_table value between 0 to 100.0
        self.normalize_q_table()

        return 0
