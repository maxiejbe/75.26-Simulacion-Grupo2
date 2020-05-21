# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def generateNormal(n, mu, sigma):
    numbers = np.array([])
    acceptedN = 0
    while acceptedN <= n:
        x = np.random.normal(mu, sigma)
        y = np.random.normal(mu, sigma)
        if y < x:
            numbers = np.append(numbers, y)
            acceptedN = acceptedN + 1
    return numbers


def drawHistogram(numbers, show):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(numbers, weights=np.zeros_like(numbers) + 1.0 / numbers.size)
    ax.set_xlabel("Numbers range")
    ax.set_ylabel("Relative frequency")
    if show:
        plt.show()


# Aplicando el algoritmo de Aceptación y rechazo se pide:
# a) Generar 100.000 número aleatorios con distribución Normal de media 25 y desvío estándar 2 .
n, mu, sigma = 100000, 25, 2
numbers = generateNormal(n, mu, sigma)

# b) Realizar un histograma de frecuencias relativas con todos los valores obtenidos.
drawHistogram(numbers, True)
