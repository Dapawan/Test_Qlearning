import numpy
import copy
from random import *

class Morpion(object):

    listePions = []
    tourJ1 = True
    tourJ2 = True
    victoireJ1 = False
    victoireJ2 = False
    finPartie = False

    # 1 : pion adverse (J2)
    # 0 : aucun pion
    # 0.5 : pion allié (J1)

    valeurAucunPion = 1
    valeurPionJ1 = 2
    valeurPionJ2 = 3

    def __init__(self):
        self.initPartie()

    def initPartie(self):
        self.listePions.clear()
        #On remplit d'espace libre le plateau
        self.listePions = [self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion,self.valeurAucunPion]
        self.finPartie = False
        self.victoireJ1 = False
        self.victoireJ2 = False
        self.tourJ1 = True
        self.tourJ2 = False
    

    def tourJ_UN(self,positionPieceTableau):
        #On exit si la partie est finit
        if(self.finPartie == True):
            return -3
        #On exit si ce n'est pas le tour du J1
        if(self.tourJ1 == False):
            return -1
        
        #On passe notre tableau en liste
        positionPieceTableau = positionPieceTableau.tolist()
        #On convertie en prenant l'index du max pour savoir la position cible
        positionPiece = positionPieceTableau.index(max(positionPieceTableau))

        #On quitte si son placement est impossible
        if(self.verificationPositionnement(positionPiece) == False):
            return -2

        #On peut faire le placement de la pièce
        self.listePions[positionPiece] = self.valeurPionJ1
        #On passe le tour
        self.tourJ1 = False
        self.tourJ2 = True


        #On teste si la partie est finit  
        if( (self.finPartie == True) | (self.verificationFinPartie() == 0) ):
            self.victoireJ1 = True
            return 1
        return 0

    def tourJ_DEUX(self,positionPieceTableau):
        #On exit si la partie est finit
        if(self.finPartie == True):
            return -3
        #On exit si ce n'est pas le tour du J1
        if(self.tourJ2 == False):
            return -1

        #On passe notre tableau en liste
        positionPieceTableau = positionPieceTableau.tolist()
        #On convertie en prenant l'index du max pour savoir la position cible
        positionPiece = positionPieceTableau.index(max(positionPieceTableau))

        #On quitte si son placement est impossible
        if(self.verificationPositionnement(positionPiece) == False):
            return -2

        #On peut faire le placement de la pièce
        self.listePions[positionPiece] = self.valeurPionJ2
        #On passe le tour
        self.tourJ1 = True
        self.tourJ2 = False

        #On teste si la partie est finit
        if( (self.finPartie == True) | (self.verificationFinPartie() == 0) ):
            self.victoireJ2 = True
            return 1
        return 0


    def verificationFinPartie(self):

         #on regarde si tous les emplacements sont pris
        if(self.listePions.count(self.valeurAucunPion) == 0):
            self.finPartie = True
            return -1

        #On doit vérifier si 3 pions sont alignés
        if( (self.listePions[0] == self.listePions[1] == self.listePions[2] != self.valeurAucunPion)
           | (self.listePions[3] == self.listePions[4] == self.listePions[5] != self.valeurAucunPion)
           | (self.listePions[6] == self.listePions[7] == self.listePions[8] != self.valeurAucunPion)
           #vertical
           | (self.listePions[0] == self.listePions[3] == self.listePions[6] != self.valeurAucunPion)
           | (self.listePions[1] == self.listePions[4] == self.listePions[7] != self.valeurAucunPion)
           | (self.listePions[2] == self.listePions[5] == self.listePions[8] != self.valeurAucunPion)

           #diagonale
           | (self.listePions[0] == self.listePions[4] == self.listePions[8] != self.valeurAucunPion)
           | (self.listePions[2] == self.listePions[4] == self.listePions[6] != self.valeurAucunPion)
          
           ):

            self.finPartie = True
            return 0
        self.finPartie = False

        return 1

    def getListePionJ_UN(self):
        return self.listePions

    def getListePionJ_DEUX(self):
        listePionJ_DEUX = []

        for i in range(len(self.listePions)):
            if(self.listePions[i] == self.valeurPionJ1):
                listePionJ_DEUX.append(self.valeurPionJ2)
            elif(self.listePions[i] == self.valeurPionJ2):
                listePionJ_DEUX.append(self.valeurPionJ1)
            else:
                listePionJ_DEUX.append(self.valeurAucunPion)
        return listePionJ_DEUX


    def getAllMovePossible(self):
        listeEmplacementDispo = []
        for i in range(len(self.listePions)):
            if(self.listePions[i]==self.valeurAucunPion):
                listeEmplacementDispo.append(i)

        return listeEmplacementDispo


    def verificationPositionnement(self,positionPieceATester):
        if(self.listePions[positionPieceATester] == self.valeurAucunPion):
            return True
        return False
        
    def enregistrerPartie(self,listeMoveJ1J2,nomFichier,numero):
        #On clear le fichier si c'est la premiere partie
        if(numero == 1):
            mon_fichier = open(nomFichier,"w")
            mon_fichier.close()
        stri = "\n\n PARTIE N° " + str(numero)
        for i in range(listeMoveJ1J2.shape[0]):
            #On coupe par 9
            stri += "**TOUR n° " + str(i)
            if(i%2 == 0):
                stri += " J1\n"
            else:
                stri += " J2\n"
            for a in range(listeMoveJ1J2.shape[1]):
                valeur = listeMoveJ1J2[i][a]
                if(valeur == self.valeurAucunPion):
                    stri += "-"
                elif(valeur == self.valeurPionJ1):
                    stri += "X"
                else:
                    stri += "O"
                if(((a+1) % 3) == 0):
                    stri += "\n"
            #Fin tour
            stri += "**Fin TOUR\n"
        #On save
        mon_fichier = open(nomFichier,"a")
        mon_fichier.write(stri)
        mon_fichier.close()

    def strToDisplay(self,listeMove):
        stri = ""
        for i in range(listeMove.shape[0]):
            valeur = listeMove[i]
            if(valeur == self.valeurAucunPion):
                stri += "-"
            elif(valeur == self.valeurPionJ1):
                stri += "X"
            else:
                stri += "O"
            if(((i+1) % 3) == 0):
                stri += "\n"
        return stri

    def simulationPartie(self, listePieceInput, listePieceOutput, nbrPartie):

        actionIASimulee = numpy.ndarray(shape=(9, 1),
                    dtype=numpy.float32)


        actionIASimulee = numpy.zeros(9)

        for i in range(nbrPartie):#nbr de parties
            print('Simulation partie n°' + str(i+1) + "/" + str(nbrPartie), end='\r')

            #Partie suivante
            self.initPartie()
            while(self.finPartie == False):
                #On prend un move possible alétoire
                move = self.getAllMovePossible()

                #Dans le cas où aucuns déplacement n'est possible
                if(len(move) == 0):
                    break
                #On sauvegarde l'input
                listePieceInput.append(copy.copy(self.getListePionJ_UN()))
                #listeTest.append(copy.copy(monMorpion.getListePionJ_UN()))
                moveChoisi = move[randint(0,len(move)-1)]
                #On max l'index du move
                actionIASimulee[moveChoisi] = 0.5
                #On fait le move
                self.tourJ_UN(actionIASimulee)
                #On sauvegarde l'output
                listePieceOutput.append(copy.copy(actionIASimulee))

                #On min l'index du move
                actionIASimulee[moveChoisi] = 0.0

                if(self.finPartie == True):
                    break

                #J2 (on save comme si J1)
                #On prend un move possible alétoire
                move = self.getAllMovePossible()

                #Dans le cas où aucuns déplacement n'est possible
                if(len(move) == 0):
                    break
                #On sauvegarde l'input
                listePieceInput.append(copy.copy(self.getListePionJ_UN()))
                #listeTest.append(copy.copy(monMorpion.getListePionJ_DEUX()))
                moveChoisi = move[randint(0,len(move)-1)]
                #On max l'index du move
                actionIASimulee[moveChoisi] = 0.5
                #On fait le move
                self.tourJ_DEUX(actionIASimulee)
                #On sauvegarde l'output
                listePieceOutput.append(copy.copy(actionIASimulee))

                #On min l'index du move
                actionIASimulee[moveChoisi] = 0.0
            #monMorpion.enregistrerPartie(numpy.asarray(listeTest),"Partie_llll.txt",i)
            #listeTest.clear()

        #return listePieceInput,listePieceOutput