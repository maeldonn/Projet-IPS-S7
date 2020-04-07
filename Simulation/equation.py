# -*- coding: utf-8 -*-
"""
Created on Wed Apr 1 2020

@author: DONNART Maël
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import os
import platform

# données
Pelec = 15  # Puissance electrique en W
T0 = 290  # Température visée [40,290]
T1 = 15  # Condition initiale : température à t=0
C = 433  # Capacité thermique du système
H = 5.5  # Coefficient de transfert thermique


def T(t):
    a = (T1-T0)-(Pelec/H)
    b = -(H/C)
    c = T0 + (Pelec/H)
    return a*np.exp(b*t)+c


def drawTemperature(x, y, limit, step):
    current_abs = 0
    for t in range(limit+1):
        while(current_abs < t):
            x.append(current_abs)
            y.append(T(current_abs))
            current_abs += step


def plotTemperature(x, y):
    plt.plot(x, y)
    plt.grid()
    plt.xlabel("Temps (s)")
    plt.ylabel("Température (°C)")
    plt.title("Evolution de la température pour Pelec = " +
              str(float(Pelec)) + "W")
    plt.show()


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def getLimit():
    print('Sur combien de secondes voulez vous effectuer la simulation ? (defaut = 300)\n')
    limit = input('limite = ')
    if(limit == ""):
        limit = 300
    else:
        limit = int(limit)
    print('\n\n')
    return limit


def getStep():
    print('Quel pas de simulation voulez-vous choisir ? (defaut = 0.1)\n')
    step = input('pas = ')
    if(step == ""):
        step = 0.1
    else:
        step = float(step)
    print('\n\n')
    return step


def main():
    clear()
    limit = getLimit()
    step = getStep()
    x = []  # Ensemble des valeurs de t
    y = []  # Ensemble des valeurs de T(t)
    drawTemperature(x, y, limit, step)
    plotTemperature(x, y)


if __name__ == "__main__":
    main()
