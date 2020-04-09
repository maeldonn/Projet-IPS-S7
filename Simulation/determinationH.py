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


def T(t, last, Te):
    if(t == 0):
        return T0
    else:
        return (last + ((Pelec - H*(last - T0))/C)*Te)


def draw_temperature(x, y, limit, step):
    n = 0
    last = 0
    for n in range(0, limit+1):
        x.append(n)
        y.append(T(n, last, step))
        last = y[-1]
        n += 1


def plot_temperature(x, y, Te):
    plt.plot(x, y)
    plt.grid()
    plt.xlabel("nTe (avec Te = " + str(Te) + " s)")
    plt.ylabel("Température (°C)")
    plt.title("Evolution de la température pour Pelec = " +
              str(float(Pelec)) + "W")
    plt.show()


def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_limit():
    print('Sur combien de secondes voulez vous effectuer la simulation ? (defaut = 4000)\n')
    limit = input('limite = ')
    if(limit == ""):
        limit = 4000
    else:
        limit = int(limit)
    print('\n\n')
    return limit


def get_Te():
    print("Quel période d'échantillonage voulez-vous choisir ? (defaut = 0.2)\n")
    Te = input('Te = ')
    if(Te == ""):
        Te = 0.2
    else:
        Te = float(Te)
    print('\n\n')
    return Te


def main():
    clear()
    limit = get_limit()
    Te = get_Te()
    x = []  # Ensemble des valeurs de t
    y = []  # Ensemble des valeurs de T(t)
    draw_temperature(x, y, limit, Te)
    plot_temperature(x, y, Te)


if __name__ == "__main__":
    main()
