import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio2 import generateRN
from scipy.stats import chi2


def groupResults(numbers):
    grouped = np.zeros(5)
    for num in numbers:
        if(     num <= 2):
            np.put(grouped, 0, np.take(grouped, [0])+1)
        if( 2 < num <= 4):
            np.put(grouped, 1, np.take(grouped, [1])+1)
        if( 4 < num <= 6):
            np.put(grouped, 2, np.take(grouped, [2])+1)
        if( 6 < num <= 8):
            np.put(grouped, 3, np.take(grouped, [3])+1)
        if( 8 < num     ):
            np.put(grouped, 4,np.take(grouped, [4])+1)
    return grouped


def main():
    mu, sigma = 5, 2.41523
    teoricos = np.random.normal(mu, sigma, n)
    teoricosAgrupados = groupResults(teoricos)

    a, x0, c, m, n = 1013904223, ((101456 + 102214 + 94511 + 95295) // 4), 1664525, 2**32, 10000
    observados = generateRN(a, x0, c, m , n)
    observadosAgrupados = groupResults(observados)

    i,D2 = 0, 0
    while (i < len(observadosAgrupados)):
        D2 += (((observadosAgrupados[i] - teoricosAgrupados[i])**2)/teoricosAgrupados[i])
        i += 1
    limiteSuperior = chi2.ppf(0.998, df=4)

    if D2 <= limiteSuperior:
        print("El test ACEPTA la hipotesis nula.")
    else:
        print("El test RECHAZA la hipótesis nula")
    return

if __name__ == "__main__":
    main()
