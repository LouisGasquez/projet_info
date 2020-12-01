# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 12:11:09 2020

@author: LOUIS
"""

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import math 

projet=pd.read_csv('EIVP_KM.csv',sep=';',index_col='sent_at',parse_dates=True)      #je nomme le document projet et je fais lire le fichier excel par pandas,le point virgule sert de séparateur pour avoir plusieurs colonne, j'indexe la colonne sent_at pour avoir un dataframe 

projet.groupby('id').plot() #graphique de toutes les variables de chaque capteur
projet.groupby('id').temp.plot() #graphique de la temperature des 6 capteurs
projet.shape #taille du tableau

#1

projet=projet.drop(['Unnamed: 0'],axis=1)#suppression de la colonne qui ne sert pas 

id_1=(projet['id']==1) #filtre pour avoir le capteur 1

plt.title("Temperature en degre en fonction du temps")
projet[id_1]['15 08 2019':'20 08 2019'].temp.plot(style='c') 
plt.xlabel('Temps')
plt.show()


#2

#graphique d'une variable avec la moyenne, ecart_type, variance, max, min mais en dehors du graphique, il faut les mettre dessus

projet[id_1]['temp'].plot()
print('la moyenne est', moyenne(liste_variable(1)[1]))
print('l ecart-type est', ecart_type(liste_variable(1)[1]))
print('le maximum est', maximum(liste_variable(1)[1]))
print('le minimum est', minimum(liste_variable(1)[1]))
print('la variance est variance', variance(liste_variable(1)[1]))
print('la médiane est',mediane(tri_insertion(liste_variable(1)[1])))
plt.show()

#graphique montrant une variable en fonction du temps et la moyenne, l'ecart-type, le maximum, le minimum, la variance et la médiane.
projet['moyenne']=moyenne(liste_variable(1)[1])
projet[id_1].temp.plot()
projet.moyenne.plot(label='moyenne')
projet['ecart_type']=ecart_type(liste_variable(1)[1])   
projet.ecart_type.plot(label='ecart-type')  
projet['maximum']=maximum(liste_variable(1)[1])   
projet.maximum.plot(label='maximum')
projet['minimum']=minimum(liste_variable(1)[1])   
projet.minimum.plot(label='minimum')    
projet['variance']=variance(liste_variable(1)[1])   
projet.variance.plot(label='variance')
projet['mediane']=mediane(tri_insertion(liste_variable(1)[1]))   
projet.mediane(tri_insertion).plot(label='mediane') 
plt.show()


#3

#fonction qui calcule l'humidex grâce à une formule qui prend l'humidité relative 
#et calcule ainsi le point de rosée pour avoir l'indice humidex    
def humidex(t,h):
    phi=h/100.0   #on passe l'humidité relative en chiffre entre 0 et 1
    a=17.27  #j'affecte des lettres aux valeurs pour plus de visibilité 
    b=237.7    
    alpha=(a*t)/(b+t)+math.log(phi)   
    pr=b*alpha/(a-alpha)
    e=6.11*math.exp(5417.7530*(1/273.16-1/(273.15+pr))) #formule prise sur internet
    hu=t+0.5555*(e-10)
    return hu
    
    
#calculer humidex de chaque capteur séparément   
def humidex_capteur(n):
    if n<=0:   #il faut que le numéro du capteur soit compris entre 1 et 6
        return False
    elif n>=7:
        return False
    else:
        L=[]  #liste où seront stockées les valeurs de l'indice humidex
        p=(projet['id']==n)   #filtre pour avoir le bon capteur     
        for i in range(0,len(projet[p]),1):#pour chaque donnée
            L.append(humidex(projet[p]['temp'][i],projet[p]['humidity'][i]))  #on remplit la liste avec l'indice humidex 
        return L

#calculer humidex de chaque capteur séparément avec une option de début et de fin
def humidex_capteur1(n,d,f):
    debut=d
    fin=f
    if n<=0:   #il faut que le numéro du capteur soit compris entre 1 et 6
        return False
    elif n>=7:
        return False
    else:
        L=[]  #liste où seront stockées les valeurs de l'indice humidex
        p=(projet['id']==n)   #filtre pour avoir le bon capteur     
        for i in range(0,len(projet[p]),1):#pour chaque donnée
            L.append(humidex(projet[p]['debut':'fin']['temp'][i],projet[p]['debut':'fin']['humidity'][i]))  #on remplt la liste avec l'indice humidex 
        return L
        
#afficher indice humidex de chaque capteur sur un graphique 

projet['humidex']=humidex_capteur(1,)+humidex_capteur(2)+humidex_capteur(3)+humidex_capteur(4)+humidex_capteur(5)+humidex_capteur(6) #cela ajoute l'indice humidex à la dataframe 

plt.plot(humidex_capteur(1), label='capteur 1')
plt.plot(humidex_capteur(2), label='capteur 2')
plt.plot(humidex_capteur(3), label='capteur 3')
plt.plot(humidex_capteur(4), label='capteur 4')
plt.plot(humidex_capteur(5), label='capteur 5')
plt.plot(humidex_capteur(6), label='capteur 6')
plt.xlabel('Temps')
plt.ylabel('Indice humidex')
plt.legend()
plt.show()

   
#4
   
def maximum(L): #fonction qui calule le maximum d'une liste 
    M=L[0]  #initialisation au premier élément
    for i in L:
        if i>M:
            M=i
    return M

def minimum(L): #fonction qui calule le minimum d'une liste
    m=L[0]  #initialisation au premier élément
    for i in L:
        if i<m:
            m=i
    return m
    
def moyenne(L): #fonction qui calcule la moyenne d'une liste 
    s=0
    n=0
    for i in L:
        s=s+i  #somme des élément 
        n=n+1 #compte le nombre d'élément
    return s/n

def variance(L): #calcul la variance d'une liste grâce à la moyenne
    u=0
    b=0
    for i in L:
        u=u+(i-moyenne(L))**2 #formule du cours de mathématiques 
        b=b+1 #compte le nombre d'élémént
    return u/b

def tri_insertion(liste):
    n=len(liste)
    for i in range (n):
        p=liste[i]
        j=i-1
        while j>=0 and p<liste[j]:
            liste[j+1]=liste[j]
            j-=1
            liste[j+1]=p
    return liste  

def mediane(L):
    if len(L)<1:
        return False
    if len(L)%2==0 :
        return (L[(len(L)-1)/2] + L[(len(L)+1)/2] )/2.0
    else:
        return L[(len(L)-1)/2]
    
def ecart_type(L):
    return variance(L)**0.5 #racine carrée de la variance
    
def covariance(L,M):   #calcule la covariance
    if len(L)!=len(M): #il faut que les listes soient egales
        return False
    else:        
        m_L=moyenne(L) #affectation pour une meilleure lisibilité 
        m_M=moyenne(M)
        s=0
        for i in range(0,len(L)):
           s=s+((L[i]-m_L)*(M[i]-m_M)) #formule du cours de mathématiques
    return s/(len(L)-1)

#calcul du coefficient de correlation
def correlation(L,M):
    return covariance(L,M)/(ecart_type(L)*ecart_type(M)) #application de la formule mathématique


#calcul du coef de correlation avec phrases            
def coef_correlation(L,M):
    t=covariance(L,M)/(ecart_type(L)*ecart_type(M))
    if np.abs(t)<=0.5:
        return 'Correlation faible',t
    else:
        return 'Correlation forte',t

#prendre les données d'une variable pour un capteur et en faire une liste        
def liste_variable(n): #choisir le capteur
    noise=[] #créer chaque liste nécessaire
    temp=[]
    humidity=[]
    lum=[]
    co2=[]
    for i in range(7880): #nombre d'éléments que l'on a (facile à avoir avec la dataframe avec .shape)
        if projet.id[i]==n:  #pour avoir les données du capteur choisis
            noise.append(projet.noise[i])
            temp.append(projet.temp[i])
            humidity.append(projet.humidity[i])
            lum.append(projet.lum[i])
            co2.append(projet.co2[i])
    return noise,temp,humidity,lum,co2

#graphique de la temperature des capteurs 1 et 2 et avec le coef de correlation (mais je n'arrive pas à l'afficher sur le graphique)    

plt.title("Temperature en fonction du temps")
projet[projet['id']==1].temp.plot(label="capteur 1")
projet[projet['id']==2].temp.plot(label="capteur 2")
i=coef_correlation(liste_variable(1)[1],liste_variable(2)[1])
print(i)
plt.xlabel('temps')
plt.legend()
plt.show()

   



