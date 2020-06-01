import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio1 import gcl


def generate_rn(n):
    gcl_values = (gcl(2*n) % 6)
    result = np.array([])
    i = 0
    while i < n:
        j = 2*i
        suma = np.take(gcl_values, j) + np.take(gcl_values, j+1) 
        result = np.append(result, suma)
        i = i + 1
    return result


def main():
    n = 10000
    data = generate_rn(n)
    plt.hist(data, bins=10)
    plt.show()
    return

if __name__ == "__main__":
    main()
