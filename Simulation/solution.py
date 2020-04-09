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
T0 = 20  # Condition initiale : température à t=0
C = 43.3  # Capacité thermique du système
H = 0.3  # Coefficient de transfert thermique


def T(t):
    a = -(Pelec/H)
    b = -(H/C)
    c = T0 + (Pelec/H)
    return a*np.exp(b*t)+c


def draw_temperature(x, y, limit, step):
    current_abs = 0
    while(current_abs <= limit):
        x.append(current_abs)
        y.append(T(current_abs))
        current_abs += step


def plot_temperature(x, y):
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


def get_limit():
    print('Sur combien de secondes voulez vous effectuer la simulation ? (defaut = 300)\n')
    limit = input('limite = ')
    if(limit == ""):
        limit = 300
    else:
        limit = int(limit)
    print('\n\n')
    return limit


def get_step():
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
    limit = get_limit()
    step = get_step()
    x = []  # Ensemble des valeurs de t
    y = []  # Ensemble des valeurs de T(t)
    draw_temperature(x, y, limit, step)
    plot_temperature(x, y)


if __name__ == "__main__":
    main()
