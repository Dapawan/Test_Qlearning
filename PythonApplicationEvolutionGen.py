import evolutionGen
import Morpion
from random import *
import numpy
import time
import copy
import matplotlib.pyplot as plt
# Just disables the warning, doesn't enable AVX/FMA
#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


entree = numpy.ndarray(shape=(4, 1),
                     dtype=numpy.float32)

sortie = numpy.ndarray(shape=(4, 1),
                     dtype=numpy.float32)

entree[0] = [1]
entree[1] = [0.5]
entree[2] = [0]
entree[3] = [0.1]
#entree[4] = [0.8,0.4]
#entree[5] = [0.12,0.56]

sortie[0] = [0.5]
sortie[1] = [0.5]
sortie[2] = [1]
sortie[3] = [0.8]
#sortie[4] = [0.8,0.4]
#sortie[5] = [0.12,0.56]

#Init 
test = evolutionGen.evolutionGen(20,9,9)
monMorpion = Morpion.Morpion()
#Série de tests


#Test apprentissage règles
listePieceOutput = []
listePieceInput = []

#listeTest = []

actionIASimulee = numpy.ndarray(shape=(9, 1),
                    dtype=numpy.float32)

lossValues = []
categorical_accuracyValues = []

actionIASimulee = numpy.zeros(9)
#test.listeIA[0].reseau.load_weights('morpionIA_1.h5')
if(False):
    
    monMorpion.simulationPartie(listePieceInput,listePieceOutput,3000)
    for i in range(200):
        #On feed l'IA avec un des move possibles
        history = test.listeIA[0].reseau.fit(numpy.asarray(listePieceInput),numpy.asarray(listePieceOutput),epochs=10,verbose=1)

        # Plot training & validation accuracy values
        fig, ax1 = plt.subplots()
            
        ax2 = ax1.twinx()
        lossValues = lossValues + (copy.copy(history.history['loss']))
        categorical_accuracyValues = categorical_accuracyValues + (copy.copy(history.history['categorical_accuracy']))
        ax1.plot(lossValues, 'g-')
        ax2.plot(categorical_accuracyValues, 'b-')
        ax1.set_xlabel('Epochs')
        ax1.set_ylabel('loss')
        ax2.set_ylabel('categorical_accuracy')
        plt.savefig('Train_.png')
        plt.close()


        test.listeIA[0].reseau.save_weights('morpionIA_1.h5')

        #On test l'IA
        result = test.listeIA[0].reseau.predict(numpy.asarray(listePieceInput))

        cnt_error = 0
        result = result.tolist()
        #listePieceOutput = listePieceOutput.tolist()

        for k in range(len(listePieceInput)):
            temp_1 = result[k]
            temp_2 = listePieceOutput[k].tolist()
            if(temp_1.index(max(temp_1)) != temp_2.index(max(temp_2))):
                cnt_error+=1

        print("Error :" + str(cnt_error) + " / " + str(len(listePieceInput)) + " soit " + str( (cnt_error/len(listePieceInput)) * 100.0) + "% d'erreur")


cntScoreIA_old = 0
while(1):

    #t_start = time.time()

    #for i in range(entree.shape[0]-1):

    #    test.result(entree[i],sortie[i])
        
    #    test.tracerCourbe()


    

    for J1 in range(len(test.listeIA)):
        for J2 in range(len(test.listeIA)):
            #On check si les joueurs sont bien différents
            if(J1 != J2):
                #La partie ne s'arrête que quand le flag est passé à True
                while(monMorpion.finPartie == False):
                    #Tour J1
                    result = monMorpion.tourJ_UN(test.listeIA[J1].result(numpy.asarray(monMorpion.getListePionJ_UN())))                    #Un mauvais déplacement est compté négativement
                    if(result == -2):
                        test.listeIA[J1].score += -20
                        monMorpion.finPartie = False
                        #On passe à la partie suivante
                        break
                    #partie gagnée
                    elif(result == 1):
                        test.listeIA[J1].score += 100
                        #Partie perdue pour le J2
                        test.listeIA[J2].score += -10
                    else:
                        #Chaque tour bien joué est récompensé
                        test.listeIA[J1].score += 10
                    #Tour J2
                    result = monMorpion.tourJ_DEUX(test.listeIA[J2].result(numpy.asarray(monMorpion.getListePionJ_DEUX())))                    #Un mauvais déplacement est compté négativement
                    if(result == -2):
                        test.listeIA[J2].score += -20
                        monMorpion.finPartie = False
                        #On passe à la partie suivante
                        break
                    #partie gagnée
                    elif(result == 1):
                        test.listeIA[J2].score += 100
                        #Partie perdue pour le J1
                        test.listeIA[J1].score += -10
                    else:
                        #Chaque tour bien joué est récompensé
                        test.listeIA[J2].score += 10
                #Partie suivante
                monMorpion.initPartie()

    if(test.newGen() == -1):
        break
    #save meilleure IA
    test.listeMeilleurIA[0].reseau.save_weights('morpionBestIA.h5')

    #On teste notre meilleure IA
    cntVictoireIA = 0
    cntVictoireJ2 = 0
    cntMauvaisDeplacement = 0
    cntBonDeplacement = 0
    #On save les moves
    listeMoveJ1J2 = []
    cnt = 1
    for i in range(100): #On fait 10 parties
        #La partie ne s'arrête que quand le flag est passé à True
        while(monMorpion.finPartie == False):
            #Tour J1
            result = monMorpion.tourJ_UN(copy.copy(test.listeIA[0].result(numpy.asarray(monMorpion.getListePionJ_UN()))))                    #Un mauvais déplacement est compté négativement
            listeMoveJ1J2.append(copy.copy(monMorpion.getListePionJ_UN()))
            if(result == -2):
                cntMauvaisDeplacement += 1
                monMorpion.finPartie = False
                #On passe à la partie suivante
                break
            #partie gagnée
            elif(result == 1):
                cntVictoireIA += 1
            else:
                cntBonDeplacement += 1

            #Tour J2

            move = monMorpion.getAllMovePossible()

            #Dans le cas où aucuns déplacement n'est possible
            if(len(move) == 0):
                break
            moveChoisi = move[randint(0,len(move)-1)]
            #On max l'index du move
            actionIASimulee[moveChoisi] = 1.0
            #On fait le move
            result = monMorpion.tourJ_DEUX(copy.copy(actionIASimulee))
            listeMoveJ1J2.append(copy.copy(monMorpion.getListePionJ_UN()))

            if(result == 1):
                cntVictoireJ2 += 1
            #On min l'index du move
            actionIASimulee[moveChoisi] = 0.0

        #Fin de partie
        #Partie suivante
        monMorpion.enregistrerPartie(numpy.asarray(listeMoveJ1J2),"Partie_.txt",cnt)
        listeMoveJ1J2.clear()
        cnt += 1
        monMorpion.initPartie()
    cntScoreIA = (100 * cntVictoireIA) + cntBonDeplacement - (cntMauvaisDeplacement * 1) 
    if(cntScoreIA_old < cntScoreIA):
        print("Meilleure IA !!!!")
        cntScoreIA_old = copy.copy(cntScoreIA)
        test.listeIA[0].score = copy.copy(test.listeMeilleurScore[0]+10)
        test.listeMeilleurIA.insert(0,copy.copy(test.listeIA[0]))
        test.listeIA[0].score = 0
        test.listeMeilleurIA.pop()
        test.listeMeilleurScore.insert(0,copy.copy(test.listeMeilleurScore[0]+10))
        test.listeMeilleurScore.pop()

        test.listeIA[0].reseau.save_weights('morpionBestIA_TEST.h5')


    #On affiche les résultats
    print("Victoire IA :" + str(cntVictoireIA) + "/100" + " Victoire J2 :" + str(cntVictoireJ2) + "/100" + " Parties nulles : " + str(100-(cntVictoireIA+cntVictoireJ2)))
    print("Bon move : " + str(cntBonDeplacement) + "/" + str(cntBonDeplacement+cntMauvaisDeplacement) + " Mauvais move :" + str(cntMauvaisDeplacement) )
    test.tracerCourbe()

    

    #t_stop = time.time()
    #delta_time = t_stop - t_start
    #print("Time_tot : " + str(delta_time) + "\n")

