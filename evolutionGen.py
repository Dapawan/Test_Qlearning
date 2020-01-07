import Ia
import numpy
from random import *
import copy
import matplotlib.pyplot

class evolutionGen(object):
    """description of class"""
    #IA
    listeIA = []
    listeResultat = []
    #Meilleurs IA
    listeMeilleurIA = []
    listeMeilleurScore = []


    #Pour tracer les courbes
    listeMoyenneIA_Matplot = []
    listeMeilleurScore_Matplot = []


    indexMutation = 0

    input_dim = 0
    output_dim = 0

    #Propriétés modifiables
    weightMax = 10.0
    weightMin = -10.0
    nbrIAbest = 4 #Nbr paire pour pouvoir avoir père et mère
    scoreInit = -10000000.0 #Le moins bon score de base
    weightAmplificateur = 1.0

    def __init__(self, nbrIa, input_dim, output_dim):

        self.input_dim = input_dim
        self.output_dim = output_dim

        #On crée les IA
        for i in range(nbrIa):
            self.listeIA.append(Ia.Ia(input_dim,output_dim))

        #On crée la liste des meilleurs IA auxquelles on donne le moins bon score
        for i in range(self.nbrIAbest):
            iaTemp = Ia.Ia(input_dim,output_dim)
            #iaTemp.score = self.scoreInit
            self.listeMeilleurIA.append(iaTemp)
            self.listeMeilleurScore.append(self.scoreInit)
            
            

    def result(self,entree,sortie):

        for i in range(len(self.listeIA)):
            weight = self.listeIA[i].reseau.get_weights()

            result = self.listeIA[i].result(entree)
            #calcul du score
            newScore = (abs(result[0]-sortie[0]))#+abs(result[1]-sortie[0]))
            
            self.listeIA[i].score += newScore
        #print("Time entrainement : " + str(tps) + "\n")


    def tri_a_bulle(self,listeScore,listeIA):

        #On trie par ordre décroissant
        for a in range(len(listeIA)-1):
            for i in range(len(listeIA)-1):
                #On teste si la valeur est plus petite
                if(listeScore[i] < listeScore[i+1]):
                    valeurTemp = listeScore[i+1]

                    listeScore[i+1] = listeScore[i]
                    listeScore[i] = valeurTemp

                    #On fait la même chose pour les IA
                    iaTemp = listeIA[i+1]
                    listeIA[i+1] = listeIA[i]
                    listeIA[i] = iaTemp

    def supprDoublons(self,listeScore,listeIA):

        for a in range(len(listeIA)-1):
            i = 0
            while(i < len(listeIA)-1):
                if(listeScore[i] == listeScore[i+1]):
                    del listeScore[i+1]
                    del listeIA[i+1]
                i+=1
                #if(id(listeIA[i]) == id(listeIA[i+1])):
                #    print("Même ID IA")

                #if(id(listeIA[i].reseau.get_weights()) == id(listeIA[i+1].reseau.get_weights())):
                #    print("Même ID weight")
                #t = numpy.array_equal(listeIA[i].reseau.get_weights() , listeIA[i+1].reseau.get_weights())
                #if(t == True):
                #    print("Même weight")


    def moyenneScore(self):
        moyenne = 0.0
        nbrIA = len(self.listeIA)
        for i in range(nbrIA):
            moyenne = moyenne + self.listeIA[i].score * (1.0/nbrIA)
        print("Moyenne IA : " + str(moyenne))
        #On ajoute la moyenne à la liste mémoire
        self.listeMoyenneIA_Matplot.append(moyenne)

    def classementIA(self):

        self.moyenneScore()

        self.listeResultat.clear()

        for i in range(len(self.listeIA)):
            self.listeResultat.append(self.listeIA[i].score)

        print("Score max IA : " + str(max(self.listeResultat)))
        #On ajoute nos scores aux scores des meilleurs IA + les IA
        for i in range(len(self.listeResultat)):
            self.listeMeilleurScore.append(self.listeResultat[i])
            self.listeMeilleurIA.append(copy.copy(self.listeIA[i]))

        #On enlève les scores en doublon
        self.supprDoublons(self.listeMeilleurScore,self.listeMeilleurIA)
        #On trie les meilleurs IAs
        self.tri_a_bulle(self.listeResultat,self.listeIA)
        self.tri_a_bulle(self.listeMeilleurScore,self.listeMeilleurIA)


        #On del le surplus (en supprimant depuis la fin de la liste)
        while(len(self.listeMeilleurScore) > self.nbrIAbest):
            self.listeMeilleurScore.pop()
            self.listeMeilleurIA.pop()


    def mutationAleatoire(self,ia):
        #On get les différents poids
        weights = ia.reseau.get_weights()

        randomValue = 0.0
        valueWeight = self.weightMax + 1.0#On veut faire au moins 1 fois le while
        compteurMutationTest = 0
        premiereLoop = True
        #indexNeurone = randint(0,len(weights[self.indexMutation][0])-1)
            
        indexDim = randint(0,len(weights[self.indexMutation])-1)

        while((premiereLoop == True) | (valueWeight < self.weightMin == True) | (valueWeight > self.weightMax == True)):

            if(premiereLoop == True):
                premiereLoop = False

            randomValue = (random() - 0.5) * self.weightAmplificateur
            valueWeight = weights[self.indexMutation][indexDim]
            valueWeight += randomValue

            if(compteurMutationTest > 50):
                print("Compteur de mutation sup à " + str(compteurMutationTest) + "\nARRET")
                return -1

            compteurMutationTest+=1

        weights[self.indexMutation][indexDim] += randomValue

        self.indexMutation+=2

        if(self.indexMutation >= len(weights)):
            self.indexMutation = 0 

        return weights

    def newGen(self):

        #On lance le classement des IAs
        self.classementIA()
        
        print("Meilleur score : " + str(self.listeMeilleurIA[0].score))
        #On ajoute le meilleur score à la liste matplot
        self.listeMeilleurScore_Matplot.append(self.listeMeilleurIA[0].score)
        #On récupère le nbrIA
        nbrIA = len(self.listeIA)
        
        #On re-génère de nouvelles IA
        for i in range(nbrIA):

            #On réalise la mutation suivant un certain %
            randomValue = random() * 100.0
            if(randomValue > 100.0):#30% de chance de mutation

                #On prend une meilleure IA au hasard
                numeroIABest = randint(0,self.nbrIAbest-1)
                #On applique des mutations
                meilleurIA_aMuter = copy.copy(self.listeMeilleurIA[numeroIABest])

                #On set le poids muté
                self.listeIA[i].reseau.set_weights(self.mutationAleatoire(meilleurIA_aMuter))
            else:

                #On set le poids
                self.listeIA[i].reseau.set_weights(self.creationEnfant())

                #On mute
                #On set le poids muté
                #self.listeIA[i].reseau.set_weights(self.mutationAleatoire(self.listeIA[i]))

            #reset du score
            self.listeIA[i].score = 0

    def creationEnfant(self):
        
        #On prend aléatoirement un père et une mère (qui doivent être différents)
        indexPere = randint(0,self.nbrIAbest-1)
        #reseauPere = copy.copy(self.listeMeilleurIA[indexPere])
        weightPere = self.listeMeilleurIA[indexPere].reseau.get_weights()
        indexMere = copy.copy(indexPere)
        while(indexMere == indexPere):
            indexMere = randint(0,self.nbrIAbest-1)
        #reseauMere = copy.copy(self.listeMeilleurIA[indexMere])
        weightMere = self.listeMeilleurIA[indexPere].reseau.get_weights()

        #On get les différents poids
        weights = copy.copy(weightMere)

        for couche in range(0,len(weights),2):
            for dim in range(len(weights[couche])):
                #for neurone in range(len(weights[couche][dim])):
                #On réalise le choix du poids père ou mère suivant un certain %
                randomValue = random() * 100.0
                if(randomValue > 50.0):#50% de chance de prendre le poids du père
                    weights[couche][dim] = weightPere[couche][dim]
                    #else:#Comme on a déjà les poids de la mère
                        #weights[couche][dim][neurone] = weightMere[couche][dim][neurone]


        return weights

    
    def tracerCourbe(self):

        try :

            fig, ax1 = matplotlib.pyplot.subplots()
            
            ax2 = ax1.twinx()
            ax1.plot(self.listeMeilleurScore_Matplot, 'g-')
            ax2.plot(self.listeMoyenneIA_Matplot, 'b-')
            ax1.set_xlabel('Epochs')
            ax1.set_ylabel('Meilleur score IA')
            ax2.set_ylabel('Moyenne score IA')
            #matplotlib.pyplot.grid(True)
            matplotlib.pyplot.savefig('Test.png')
            matplotlib.pyplot.close()

        except :
            print("Erreur")

