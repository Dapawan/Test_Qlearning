import Morpion
import copy
import numpy
from random import *

class EnvJeu(object):
    """description of class"""

    monMorpion = Morpion.Morpion()
    actionIASimulee = numpy.ndarray(shape=(9, 1),
                    dtype=numpy.float32)

    rewardWin = 100
    rewardWellPLay = 1
    rewardBadPlay = -200
    rewardLose = -100
    #Constructeur
    #def __init__(self):
    #    #On crée l'objet morpion pour gérer la partie
    #    self.monMorpion 

    #On override la fonction reset
    def reset(self):
        #Permet de recommencer la partie
        self.monMorpion.initPartie()
        return self.monMorpion.getListePionJ_UN()

    #Fonction pour agir sur l'env
    def step(self, action, isJ1, isAlgo):


        if(isAlgo == True):
            #On gère l'autre déplacement
            self.actionIASimulee = numpy.zeros(9)
            move = self.monMorpion.getAllMovePossible()
            #Dans le cas où aucuns déplacement n'est possible
            if(len(move) > 0):
                moveChoisi = move[randint(0,len(move)-1)]
                #On max l'index du move
                self.actionIASimulee[moveChoisi] = 1.0
                #On fait le move
                self.monMorpion.tourJ_DEUX(copy.copy(self.actionIASimulee))

            #On check la fin de partie
            self.monMorpion.verificationFinPartie()
            return self.monMorpion.getListePionJ_DEUX(), 0, self.monMorpion.finPartie


        #On fait jouer l'IA
        self.actionIASimulee = numpy.zeros(9)
        self.actionIASimulee[action] = 1.0
        if(isJ1 == True):
            result = self.monMorpion.tourJ_UN(copy.copy(self.actionIASimulee))
        else:
            result = self.monMorpion.tourJ_DEUX(copy.copy(self.actionIASimulee))
        #On gère le score
        if(result == -2):
            self.monMorpion.finPartie = False
            #On passe à la partie suivante --> Mauvais move
            if(isJ1 == True):
                return self.monMorpion.getListePionJ_UN(), self.rewardBadPlay, True
            else:
                return self.monMorpion.getListePionJ_DEUX(), self.rewardBadPlay, True
        #partie gagnée
        elif(result == 1):
            if(isJ1 == True):
                return self.monMorpion.getListePionJ_UN(), self.rewardWin, True
            else:
                return self.monMorpion.getListePionJ_DEUX(), self.rewardWin, True


        #On retourne l'emplacement des pièces actuelles
        self.monMorpion.verificationFinPartie()
        if(isJ1 == True):
            return self.monMorpion.getListePionJ_UN(), self.rewardWellPLay, self.monMorpion.finPartie
        else:
            return self.monMorpion.getListePionJ_DEUX(), self.rewardWellPLay, self.monMorpion.finPartie

    #Fonction pour afficher les résultats
    def render(self):
        print(self.monMorpion.strToDisplay(numpy.asarray(self.monMorpion.getListePionJ_UN())))

