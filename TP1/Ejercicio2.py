import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio1 import gcl

a = 1013904223
x0 = (101456 + 102214 + 94511 + 95295) // 4
c = 1664525
m = 2**32

def generateRN(n):
    gclValues = (gcl(a, x0, c, m, 2*n) % 6)
    result = np.zeros(11)
    i = 0
    while i < n:
        j = 2*i
        index = np.take(gclValues, j) + np.take(gclValues, j+1) 
        np.put(result, [index], [np.take(result, [index])+1])
        i = i + 1
    return result

x = generateRN(10000)
print(x)
values = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9', '10']
plt.bar(values, x)
plt.xticks(values)
plt.yticks(x) 
plt.xlabel('Valores posibles')
plt.ylabel('Repeticiones')
plt.show()
