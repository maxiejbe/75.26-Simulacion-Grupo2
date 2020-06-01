import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio1 import gcl


def generate_rn(a, x0, c, m, n):
    gcl_values = (gcl(a, x0, c, m, 2*n) % 6)
    result = np.array([])
    i = 0
    while i < n:
        j = 2*i
        suma = np.take(gcl_values, j) + np.take(gcl_values, j+1) 
        result = np.append(result, suma)
        i = i + 1
    return result


def main():
    a, x0, c, m, n = 1013904223, ((101456 + 102214 + 94511 + 95295) // 4), 1664525, 2**32, 10000
    data = generate_rn(a, x0, c, m , n)
    plt.hist(data, bins=10)
    plt.show()
    return

if __name__ == "__main__":
    main()
