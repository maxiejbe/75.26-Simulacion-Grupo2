import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio1 import gcl


def generateRN(a, x0, c, m, n):
    gclValues = (gcl(a, x0, c, m, 2*n) % 6)
    result = np.zeros(11)
    i = 0
    while i < n:
        j = 2*i
        index = np.take(gclValues, j) + np.take(gclValues, j+1) 
        np.put(result, [index], [np.take(result, [index])+1])
        i = i + 1
    return result


def main():
    a, x0, c, m, n = 1013904223, ((101456 + 102214 + 94511 + 95295) // 4), 1664525, 2**32, 10000
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9', '10']
    np.set_printoptions(suppress = True)
    x = generateRN(a, x0, c, m , n)
    plt.bar(values, x)
    plt.xticks(values)
    plt.xlabel('Valores posibles')
    plt.ylabel('Repeticiones')
    plt.show()
    return

if __name__ == "__main__":
    main()
