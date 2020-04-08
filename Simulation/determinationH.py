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
T0 = 20  # Valeur initiale
C = 43.3  # Capacité thermique du système
H = 0.3  # Coefficient de transfert thermique


def T(t, last, step):
    if(t == 0):
        return T0
    else:
        return (last + ((Pelec - H*(last - T0))/C)*step)


def drawTemperature(x, y, limit, step):
    current_abs = 0
    last = 0
    while current_abs < limit:
        x.append(current_abs)
        y.append(T(current_abs, last, step))
        last = y[-1]
        current_abs += step


def plotTemperature(x, y):
    plt.plot(x, y)
    plt.grid()
    plt.xlabel("k")
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
    print('Quel pas de simulation voulez-vous choisir ? (defaut = 1)\n')
    step = input('pas = ')
    if(step == ""):
        step = 1
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
