import csv
import os.path
from constants import ROWS, COLS, FILE_NAME_CSV

def textToCsv(filename):
    
    # Ouvrir le fichier texte
    with open(filename, 'r') as fichier_texte:
        lignes = fichier_texte.readlines()

    # Traiter les lignes et créer une liste de listes
    donnees = []
    for ligne in lignes:
        donnees.append(ligne.strip().split())

    newFileName = filename.replace(".txt", ".csv")

    # Ecrire & Generer les données dans un fichier CSV 
    with open(newFileName, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerows(donnees)


# Fonction retournant une matrice contenant la fréquence
# bigramme des couples (a,a) -> (z,z)
def csvToMatrix(fileName):
    bg = [[0 for i in range(26)] for j in range(26)]
    a = 0
    with open(fileName, 'r') as file:
        fileReader = csv.reader(file)
        # On ignore la première ligne contenant A,B,...,Z
        next(fileReader)
        for ligne in fileReader:
            for i in range(1,27):
                bg[a][i-1] = int(ligne[i])
            a += 1
    
    return bg

def txtToMatrix(fileName):

    # Creates CSV FILE FROM TXT
    if (not os.path.isfile(FILE_NAME_CSV)):
        textToCsv(fileName)
    
    bg = csvToMatrix(FILE_NAME_CSV)
    return bg


# MANHATTAN DISTANCE
def calcDistance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def coordinatesFirstLetter(state):
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] != 0:
                return i,j
    return 0,0

# Fonction pour calculer le score d'un état par rapport à la première lettre
# du plateau
def score(state, bg):
    score = 0
    x,y = coordinatesFirstLetter(state)
    letter = state[x][y]
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] == 0:
                continue
            else:
                distance = calcDistance(x,y,i,j)
                if distance == 0: distance = 1
                score += (bg[letter-1][state[i][j]-1]) / distance
            
    return score


# Remplace une lettre par  0
def getCoordonnees(matrice, letter):
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if matrice[i][j] == letter:
                #matrice[i][j] = newLetter
                return i,j
    return 0,0
    

# Transforme la matrice avec les 1 -> 26
# En lettre a -> z
def intToKeyboard(bestState):
    keyBoard =  [['0' for i in range(COLS)] for j in range(ROWS) ]

    for i in range(ROWS):
        for j in range(COLS):
            if (bestState[i][j] != 0):
                keyBoard[i][j] = chr(bestState[i][j] + 96)
            else:
                keyBoard[i][j] = '*'
    
    return keyBoard

