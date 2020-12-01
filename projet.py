# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 12:11:09 2020

@author: LOUIS
"""

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import math 

projet=pd.read_csv('EIVP_KM.csv',sep=';',index_col='sent_at',parse_dates=True) #je nomme le document projet et je fais lire le fichier excel par pandas,le point virgule sert de séparateur pour avoir plusieurs colonne, j'indexe la colonne sent_at pour avoir un dataframe 
#projet['temp'].plot()
#projet.groupby('id').plot() #graphe de tout de chaque capteur
#projet.groupby('id').temp.plot() #graphe de la temperature des 6 capteurs
#projet.shape
#projet.describe()
#projet.columns
projet=projet.drop(['Unnamed: 0'],axis=1) #je supprime la colonne qui ne sert pas 
#
#1

id_1=(projet['id']==1) #evolution variable ou appelé aussi filtre 
#projet[id_1].temp.plot(style='c') #evolution variable
#projet[id_1]['15 08 2019':'20 08 2019'].temp.plot(style='c') #evo temp avec intervalle de temps



#2

#projet['temp'][id_1].mean()
#projet['temp'][id_1].std()
#projet['temp'][id_1].min()
#projet['temp'][id_1].max()
#projet['temp'][id_1].variance()


#3
#fonction qui calcul l'humidex grâce à une formule qui prend l'humidité relative et calcul ainsi le poiit de rosée puis on calcule l'indice humidex    
def humidex(t,h):
    phi=h/100.0   #on passe l'humidité relative en chiffre entre 0 et 1
    a=17.27  #j'affecte aux valeurs des lettres pour plus de visibilité 
    b=237.7    
    alpha=(a*t)/(b+t)+math.log(phi)   
    pr=b*alpha/(a-alpha)
    e=6.11*math.exp(5417.7530*(1/273.16-1/(273.15+pr)))
    hu=t+0.5555*(e-10)
    return hu
    
#fonction qui calcule l'humidex pour le capteur1 (ne set à rien)
def humi_capt1(x):
    c1=[]
    for i in range(0,len(x),1):
        c1.append(humidex(projet[id_1]['temp'][i],projet[id_1]['humidity'][i]))
    return c1

#calculer l'indice humidex pour chaque capteur (ne marche pas ?)
def humi_capt(x):
    for i in range(1,7,1): 
        C=[]        
        p=(projet['id']==i)
        for j in range(0,len(projet[p]),1):
            C.append(humidex(projet[p]['d':'f']['temp'][j],projet[p]['d':'f']['humidity'][j]))
    return C
    
#calculer humidex de chaque capteur séparément (il faut mettre une date en option)   
def humidex_capteur(n,d,f):
    if n<=0:   #il faut que le numéro du capteur soit compris entre 1 et 6
        return False
    elif n>=7:
        return False
    else:
        L=[]  #liste où seront stocké les valeurs de l'indice humidex
        p=(projet['id']==n)   #filtre pour avoir le bon capteur     
        for i in range(0,len(projet[p]),1):#pour chaque donnée
            L.append(humidex(projet[p]['d':'f']['temp'][i],projet[p]['d':'f']['humidity'][i]))  #on remplt la liste avec l'indice humidex 
        return L
        
#afficher indice humidex de chaque capteur sur un graphique 

projet['humidex']=humidex_capteur(1)+humidex_capteur(2)+humidex_capteur(3)+humidex_capteur(4)+humidex_capteur(5)+humidex_capteur(6)

#plt.plot(humidex_capteur(1), label='capteur 1')
#plt.plot(humidex_capteur(2), label='capteur 2')
#plt.plot(humidex_capteur(3), label='capteur 3')
#plt.plot(humidex_capteur(4), label='capteur 4')
#plt.plot(humidex_capteur(5), label='capteur 5')
#plt.plot(humidex_capteur(6), label='capteur 6')
#plt.xlabel('Temps')
#plt.ylabel('Indice humidex')
#plt.legend()
#plt.show()

   
#4
def maximum(L): #fonction qui calule le maximum d'une liste 
    M=L[0]  #initialisation au premier élément
    for i in L:
        if L[i]>M:
            M=L[i]
    return M

def minimum(L): #fonction qui calule le minimum d'une liste
    m=L[0]  #initialisation au premier élément
    for i in L:
        if L[i]<m:
            m=L[i]
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
        u=u+(i-moyenne(L))**2 #formule de könig sans la premier moyenne 
        b=b+1 #compte le nombre d'élémént
    return u/b
    
def ecart_type(L):
    return variance(L)**0.5 #racine carrée de la variance
    
def covariance(L,M):   #calcul la covariance
    if len(L)!=len(M): #il faut que les listes soient egales
        return False
    else:        
        m_L=moyenne(L) #affecte pour une meilleur lisibilité 
        m_M=moyenne(M)
        s=0
        for i in range(0,len(L)):
           s=s+((L[i]-m_L)*(M[i]-m_M)) #formule du cours de mathématiques
    return s/(len(L)-1)

#calcul du coefficient de correlation
def correlation(L,M):
    return covariance(L,M)/(ecart_type(L)*ecart_type(M)) #application de la formule mathématiques


#calcul du coef de correlation avec phrases qui font bien            
def coef_correlation(L,M):
    t=covariance(L,M)/(ecart_type(L)*ecart_type(M))
    if np.abs(t)<=0.5:
        return 'Correlation faible',t
    else:
        return 'Correlation forte',t

#prendre les données d'une variable pour un capteur et en faire une liste        
def liste_variable(n): #choisir le capteur
    noise=[] #créer chauqe liste nécessaire
    temp=[]
    humidity=[]
    lum=[]
    co2=[]
    for i in range(7880): #prend tous les éléments que l'on a (facile a avoir avec la data frame avec describe, shape)
        if projet.id[i]==n:  #pour avoir les données du capteur choisis
            noise.append(projet.noise[i])
            temp.append(projet.temp[i])
            humidity.append(projet.humidity[i])
            lum.append(projet.lum[i])
            co2.append(projet.co2[i])
    return noise,temp,humidity,lum,co2

#graphique de la temperature des capteurs 1 et 2 et avec le coef de correlation (mais je n'arrive pas à l'afficher sur le graphique)    
#plt.title("Temperature en fonction du temps")
#projet[projet['id']==1].temp.plot(label="capteur 1")
#projet[projet['id']==2].temp.plot(label="capteur 2")
#i=indice_correlation(liste_variable(1)[1],liste_variable(2)[1])
#print(i)
#plt.xlabel('temps')
#plt.legend()
#plt.show()

#2
#graphique d'une variable avec la moyenne, ecart_type, variance, max, min mais en dehors du graphique, il faut les mettre dessus
#projet[id_1]['temp'].plot()
#print('la moyenne est', moyenne(liste_variable(1)[1]))
#print('l ecart-type est', ecart_type(liste_variable(1)[1]))
#print('le max est', max(liste_variable(1)[1]))
#print('le min est', min(liste_variable(1)[1]))
#print('la variance est variance', variance(liste_variable(1)[1]))
#plt.show()
#    
    
    
    
    
    
    
    
    
    



