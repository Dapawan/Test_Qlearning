import keras
import copy
import time
import numpy

class Ia(object):
    """description of class"""

    score = 0
    reseau = 0

    def result(self,entree):
        resultat = self.reseau.predict_on_batch(numpy.asarray(entree))

        return resultat[0]

    def __init__(self,input_dim,output_dim):

        self.reseau = keras.Sequential()
        self.reseau.add(keras.layers.Dense(18, activation='relu', input_shape=(9,)))
        self.reseau.add(keras.layers.BatchNormalization(momentum=0.8))
        #self.reseau.add(keras.layers.Dropout(0.2))
        self.reseau.add(keras.layers.Dense(18, activation='relu'))
        self.reseau.add(keras.layers.BatchNormalization(momentum=0.8))
        #self.reseau.add(keras.layers.Dropout(0.2))
        #self.reseau.add(keras.layers.Dense(29, activation='relu'))
        #self.reseau.add(keras.layers.Dense(29, activation='relu'))
        self.reseau.add(keras.layers.Dense(output_dim, activation='softmax'))

        self.reseau.compile(loss=keras.losses.mean_squared_error,
        optimizer=keras.optimizers.Adam(lr=0.0001, beta_1=0.5), metrics=[keras.metrics.categorical_accuracy])

    
