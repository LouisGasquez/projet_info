import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


##
projet=pd.read_csv('EIVP_KM.csv',sep=';',index_col='sent_at',parse_dates=True)


##Partie 1 - fonctions de base à implémenter- partie Louis

def moyenne(liste):
    n = len(liste)
    compteur = 0
    for i in liste:
        compteur += i
    if n > 0:
        k = compteur/n
        return k
    else:
        return None




##Partie 2 - Impplémenter les données du tableau csv

# le mieux ça serait de faire un tableau par dimension utilisée

bruit =
temperature =
lum =
co2 =



## Partie 3 : Recherche des similarités




## trier les données sous ordre croissant - tri par insertion
# cela permet d'avoir une sorte d'histogramme sans le tracer, réorganisation des données


def insertionsort(liste):
    n = len(liste)
    for i in range (n):
        p = liste[i]
        j = i-1
        while j >= 0 and p< liste[j]:
            liste[j + 1] = liste[j]
            j -= 1
            liste[j + 1] = p
    return liste



##calcul les différences entre deux termes sur la liste triée.
# On répertorie les sauts entre deux termes, afin de pouvoir séparer nos tas. Cela correspond à un saut en abscisse sur notre histogramme.


def difference_deux_a_deux(liste):
    n = len(liste)
    difference = np.zeros(n-1)
    for i in range (n-1):
        difference[i] = liste[i+1]-liste[i]
    return difference





##Recherche des indices où il y a les plus grands sauts entre les valeurs.

# on va donc repérer les plus grands sauts entre deux termes successifs, ainsi que les indices où ils se produisent. Cela nous permettra ensuite de calculer nos similitudes.



## initialisation : tas simplification
# Nous avons choisi de proposer une méthode où il fallait connaître le nombre de tas au préalable. Nous montrerons plus tard comment en trouver un nombre pertinent.



indice_saut = [0]*nb_tas
valeur_saut = np.zeros(nb_tas)

# on créer donc deux listes qui vont évoluer parralèllement, La liste des valeurs des sauts et la liste des indices où ils se produisent, afin que nous sachions où ont lieu les sauts.

##Production des listes réduites des plus grands sauts et de leurs indices.


#initialisation de ces listes

for i in range (nb_tas):
    valeur_saut[i] = difference[i]  # il faut remplacer difference par la liste difference_donnée (bruit, lumière, etc.)
    indice_saut[i] = i



# tri de la liste initiale valeur_saut et indice_saut
for i in range(nb_tas):
    p = valeur_saut[i]
    j = i-1
    while j>=0 and p < valeur_saut[j]:

        valeur_saut[j+1] = valeur_saut[j]
        indice_saut[j+1] = indice_saut[j]
        j-=1
        valeur_saut[j+1] = p
        indice_saut[j+1] = i
##

def tri_listes_saut(nb_tas,valeur_saut,indice_saut):
    for i in range(nb_tas-1):
        p = valeur_saut[i]
        j = i-1
        while j>=0 and p<valeur_saut[j]:
            valeur_saut[j+1] = valeur_saut[j]
            indice_saut[j+1] = indice_saut[j]
            j-=1
            valeur_saut[j+1] = p
            indice_saut[j+1] = i


nb_mesure = len(difference)

# recherche dans la liste globale

for i in range(nb_tas,nb_mesure):
    if difference[i] < valeur_saut[0]:
        i+=1
    else:
        valeur_saut[0] = difference[i]
        indice_saut[0] = i
        for i in range(nb_tas-1):
            p = valeur_saut[i]
            k = indice_saut[i]
            j = i-1
            while j>=0 and p < valeur_saut[j]:
                valeur_saut[j+1] = valeur_saut[j]
                indice_saut[j+1] = indice_saut[j]
                j-=1
                valeur_saut[j+1] = p
                indice_saut[j+1] = k
        i+=1

##
for i in range(nb_tas,nb_mesure):
    if difference[i] < valeur_saut[0]:
        i+=1
    else:
        valeur_saut[0] = difference[i]
        indice_saut[0] = i
        tri_listes_saut(nb_tas,valeur_saut,indice_saut)

##Ecriture des différents tas en fonction des indices des plus grands sauts




def moyenne_tas(data,indice_saut,moyennes,point_isole):
    n = len(indice_saut)
    for i in range(1,n):
        k = indice_saut[i-1]+1
        j = indice_saut[i]+1
        if len(data[k:j])<=1:
#Si le point considéré est un point isolé, on le supprime
            moyennes[i] = moyenne(data[k:j])
            point_isole.append(i)
            print(moyennes[i])
        else:
            liste = data[k:j]
            m = moyenne(liste)
            moyennes[i] = m
    return moyennes

#Il y a t il assez de tas ? + Affichage des similitudes si c'est le cas. On considère dans cet algorithme que le nombre de tas est satisfaisant dès qu'il y en a plus que de points isolés.
##



def nb_tas_suffisant(nb_tas,point_isole):
    compteur = len(point_isole)
    result = nb_tas-compteur
    if result < compteur:
        nb_tas = nb_tas+1
    return nb_tas













## essai infructueux

# recherche des 5 plus grandes différences deux à deux de la totalité des mesures. on considère dans ce programmme qu'on calcule 5 tas.
# a voir comment on informatise le nombre de tas calculé

# reprendre à partir de l'étape 2

# problème ne fonctionne pas comme on souhaite le voir fonctionner, notamment un problème dans le tri de la liste.



for i in range(5,nb_mesure-1):
    print(difference[i])
    print(valeur_saut)
    if  difference[i] < valeur_saut[0]:
        i+1
    if difference[i]  >  valeur_saut[4] or  difference[i]  == valeur_saut[4]:
        valeur_saut[4] = difference[i]
        indice_saut[4] = i
        for j in range(3):
            valeur_saut[j] = valeur_saut[j+1]
            indice_saut[j] = indice_saut[j+1]

        i+=1
    if difference[i]  > valeur_saut[3] or  difference[i]  ==  valeur_saut[3]:
        valeur_saut[3] = difference[i]
        indice_saut[3] = i
        for j in range(2):
            valeur_saut[j] = valeur_saut[j+1]
            indice_saut[j] = indice_saut[j+1]

        i+=1
    if difference[i]  > valeur_saut[2] or  difference[i]  ==  valeur_saut[2]:
        valeur_saut[2] = difference[i]
        indice_saut[2] = i
        for j in range(1):
            valeur_saut[j] = valeur_saut[j+1]
            indice_saut[j] = indice_saut[j+1]

        i+=1
    if difference[i]  > valeur_saut[1] or  difference[i]  ==  valeur_saut[1]:
        valeur_saut[0] = valeur_saut[1]
        indice_saut[0] = indice_saut[1]
        valeur_saut[1] = difference[i]
        indice_saut[1] = i
        i+=1
    if difference[i]  > valeur_saut[0]or  difference[i]  ==  valeur_saut[0]:
        valeur_saut[0] = difference[i]
        indice_saut[0] = i
        i+=1



#on a dorénavant les positions et valeurs de nos 5 plus grands sauts

for i in range(1,nb_tas):
    j = indice_saut[i-1]+1
    k = indice_saut[i]
    tas_i = data[j:k]

k = indice_saut[0]
tas_0 = data[:k]
tas_1 =  data[j:k]

#calcul des infos sur les similitudes + affichage


## Essai programme total:

#on appelle data, l'extraction des données à une dimension de la bdd, autremenent une des colonnes du tableau de EIVP_KM


def similitude(data, nb_tas):
    nb_tas_initial = nb_tas
    data = insertionsort(data)
    difference = difference_deux_a_deux(data)
    indice_saut = [0]*(nb_tas-1)
    valeur_saut = np.zeros(nb_tas-1)
    nb_mesure = len(difference)
    point_isole = []

    for i in range (nb_tas-1):
        valeur_saut[i] = difference[i]  # il faut remplacer difference par la liste difference_donnée (bruit, lumière, etc.)
        indice_saut[i] = i
# tri de la liste initiale valeur_saut et indice_saut
    tri_listes_saut(nb_tas,valeur_saut,indice_saut)
 # recherche des nb_tas plus grands sauts et de leur indice
    for i in range(nb_tas-1,nb_mesure):
        if difference[i] >= valeur_saut[0]:
            valeur_saut[0] = difference[i]
            indice_saut[0] = i
            for i in range(nb_tas-1):
                p = valeur_saut[i]
                k = indice_saut[i]
                j = i-1
                while j>=0 and p < valeur_saut[j]:
                    valeur_saut[j+1] = valeur_saut[j]
                    indice_saut[j+1] = indice_saut[j]
                    j-=1
                    valeur_saut[j+1] = p
                    indice_saut[j+1] = k
            i+=1

    insertionsort(indice_saut)



# on va dorénavant calculer les moyennes de nos similitudes et les entrer dans un tableau
    moyennes = np.zeros(nb_tas)
    k = indice_saut[0]+1
    moyennes[0] = moyenne(data[:k])
    if len(data[:k]) <= 1:
        point_isole.append(1)
    moyennes = moyenne_tas(data,indice_saut,moyennes,point_isole)
    m = indice_saut[-1]
    moyennes[-1] = moyenne(data[m:])
    if len(data[m:])<=1:
        point_isole.append(nb_saut)

# jusqu'ici tout va bien

    # verification de notre condition plus de tas que de points isolés
    nb_tas = nb_tas_suffisant(nb_tas, point_isole)
    if nb_tas == nb_tas_initial:
         for i in range(nb_tas):
             if moyennes[i] == None:
                 moyennes[i] = data[difference[indice_saut[i]]]
         return moyennes,point_isole

    else :
        similitude(data,nb_tas)












