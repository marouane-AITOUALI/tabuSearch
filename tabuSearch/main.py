from copy import deepcopy
import random
from algo import textToCsv, csvToMatrix, score, intToKeyboard, txtToMatrix, getCoordonnees
from constants import NOMBRE_TOUR_TABOU, MAX_ITERATION , SCORE_OPTIMAL, ROWS, COLS, FILE_NAME

# Generate Bigramme Frequence matrix from the text File
bg = txtToMatrix(FILE_NAME)

# Initialisation des paramètres
listTabou = []
bestState = None
bestScore = float('-inf')
letters = list(range(1, 27))

# Création de l'état initial
# liste contenant 4 listes de longueur 10 
# les valeurs != 0 dans les 4 listes sont différentes de 1-26 
# représentant les lettres a -> z (Positionnement aléatoire au départ)
state = [[0 for j in range(COLS)] for i in range(ROWS)]
for chiffre in letters:
    i, j = None, None
    while i is None or state[i][j] != 0:
        i, j = random.randint(0, 3), random.randint(0, 9)
    state[i][j] = chiffre


# Affichage de la disposition aléatoire en chiffres 1 = a 26 = z
#for i in range(ROWS):
#    print(state[i])


# Boucle principale de recherche tabou
for k in range(MAX_ITERATION):
    # Choisir le meilleur voisin non-tabou
    meilleurVoisin = None
    meilleurScoreVoisin = float('-inf')
    for i in range(ROWS):
        for j in range(COLS):
            for letter in letters:
                #if letter == state[i][j]:
                 #   continue
                oldLetter = state[i][j] 
                # Deepcopy de l'état actuel
                copyState = deepcopy(state)
                
                # Coordonnees de la nouvelle lettre à trouver l'emplacement
                # Swap avec les coordonnees actuelles i,j
                x,y = getCoordonnees(copyState, letter)
                copyState[i][j], copyState[x][y] = copyState[x][y],copyState[i][j]
                

                    
                
                
                
                
                # Calcul du score
                neighbor_score = score(copyState, bg)
                if (i, j, letter) not in listTabou and neighbor_score > meilleurScoreVoisin :
                    meilleurScoreVoisin = neighbor_score
                    meilleurVoisin = (i, j, letter)
                    state = copyState
                else:
                    state[i][j] = oldLetter

    # Mettre à jour la meilleure solution
    if meilleurScoreVoisin > bestScore:
        bestScore = meilleurScoreVoisin
        bestState = [row[:] for row in state]

    # Mettre à jour la liste tabou
    if meilleurVoisin is not None:
        listTabou.append(meilleurVoisin)

    # Enlever la lettre tabou si le nombre de tour tabou s'est écoulé
    if len(listTabou) > NOMBRE_TOUR_TABOU:
        listTabou.pop(0)

    # Sortir de la boucle si le score optimal est atteint
    if bestScore >= SCORE_OPTIMAL:
        break


keyBoard =  intToKeyboard(bestState)
        
print("Meilleure solution trouvée: (* : Pas de lettres)\n")

# Affichage de la meilleure disposition en chiffres 1 = a 26 = z
#for i in range(ROWS):
#    print(bestState[i])

# Affichage de la meilleure disposition en lettres 
for i in range(ROWS):
    print(keyBoard[i])
print("\nScore:", bestScore)
