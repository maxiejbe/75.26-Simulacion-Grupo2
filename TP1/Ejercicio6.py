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

def ChiSquaredTest(mu, sigma, n, observedValues) :
    observadosAgrupados = groupResults(observedValues)
    teoricos = np.random.normal(mu, sigma, n)
    teoricosAgrupados = groupResults(teoricos)

    i,D2 = 0, 0
    while (i < len(observadosAgrupados)):
        D2 += (((observadosAgrupados[i] - teoricosAgrupados[i])**2)/teoricosAgrupados[i])
        i += 1
    limiteSuperior = chi2.ppf(0.999, df=4)
    return D2 <= limiteSuperior

def multipleChiSquaredTest(n, testsN):
    a, x0, c, m = 1013904223, ((101456 + 102214 + 94511 + 95295) // 4), 1664525, 2**32
    observedValues = generateRN(a, x0, c, m , n)
    mu, sigma = 5, 2.41523
    resutls = [ChiSquaredTest(mu, sigma,n, observedValues) for _ in range(testsN)]
    return resutls


def main():
    n, testsN = 10000, 100
    results =  multipleChiSquaredTest(n, testsN)
    print("El test ACEPTA la hipotesis nula {} veces.".format(len([result for result in results if result])))
    print("El test RECHAZA la hipótesis nula {} veces".format(len([result for result in results if not result])))
    

if __name__ == "__main__":
    main()


