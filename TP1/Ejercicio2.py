import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio1 import gcl

a = 1013904223
x0 = (101456 + 102214 + 94511 + 95295) // 4
c = 1664525
m = 2**32

def generateRN(n):
    x = (gcl(a, x0, c, m, 2*n) % 6)
    result = []
    i = 0
    while i < 2*n:
        result.append(x[i]+x[i+1])
        i = i+2
    return result

plt.close("all")
x = generateRN(10000)
plt.plot(x)
plt.show()