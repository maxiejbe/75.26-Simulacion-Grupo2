import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio2 import generateRN
from scipy.stats import chi2




def main():
    a, x0, c, m, n = 1013904223, ((101456 + 102214 + 94511 + 95295) // 4), 1664525, 2**32, 10000
    mu, sigma = 5, 2.41523
    teoricos = np.random.normal(mu, sigma, n)

    teoricosAgrupados = [
        len((([number for number in teoricos if number <= 2]))), 
        len((([number for number in teoricos if number > 2 and number <= 4]))), 
        len((([number for number in teoricos if number > 4 and number <= 6]))),
        len((([number for number in teoricos if number > 6 and number <= 8]))),
        len((([number for number in teoricos if number > 8])))]

    observados = generateRN(a, x0, c, m , n)
    observadosAgrupados = [
        len((([number for number in observados if number <= 2]))), 
        len((([number for number in observados if number > 2 and number <= 4]))), 
        len((([number for number in observados if number > 4 and number <= 6]))),
        len((([number for number in observados if number > 6 and number <= 8]))),
        len((([number for number in observados if number > 8])))]

    i = 0
    D2 = 0
    while (i < len(observadosAgrupados)):
        D2 += (((observadosAgrupados[i] - teoricosAgrupados[i])**2)/teoricosAgrupados[i])
        i += 1
    limiteSuperior = chi2.ppf(0.9965, df=4)

    if D2 <= limiteSuperior:
        print("El test ACEPTA la hipotesis nula.")
    else:
        print("El test RECHAZA la hipótesis nula")
    return

if __name__ == "__main__":
    main()
