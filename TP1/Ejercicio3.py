import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from Ejercicio1 import gcl01

# Graficar la función de densidad de probabilidad


def f(x):
    return (13 / (12 * math.pi)) - (x ** 2) / ((math.pi) ** 3)


x = np.arange(-math.pi / 2, math.pi / 2)
p = f(x)
plt.plot(x, p, label="linear")
plt.title("Función de densidad de probabilidad")
plt.show()

# Calcular y graficar la función de probabilidad acumulada y su inversa

# Función de probabilidad acumulada (Función de distribución):
def F(x):
    return ((13 * x) / (12 * np.pi)) - ((x ** 3) / (3 * (np.pi ** 3))) + 0.5


def main():
    # Grafico funcion distribucion original
    x = np.linspace(-3, 3, 30)
    y = [F(xi) for xi in x]
    plt.plot(x, y, "-r")
    plt.title("Función de probabilidad acumulada")
    plt.show()

    # inviersión de los ejes
    x, y = y, x

    # interpolación con puntos equiespaciados
    F_inversa = interpolate.interp1d(x, y)

    # Gráfico de la inversa
    plt.plot(x, y, "o", x, F_inversa(x), "-")
    plt.title("Función de distribución inversa")
    plt.show()

    # Histograma valores generados con gcl01
    simulacion_valores(F_inversa)

    return


def simulacion_valores(funcion):
    x_new = gcl01(100000)
    y_new = funcion(x_new)
    plt.hist(y_new)
    plt.title("Histograma")
    plt.show()
    return


main()
