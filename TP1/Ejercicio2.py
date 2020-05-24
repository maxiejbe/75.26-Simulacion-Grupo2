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
    # print(len([number for number in x if number == 0]))
    # print(len([number for number in x if number == 1]))
    # print(len([number for number in x if number == 2]))
    # print(len([number for number in x if number == 3]))
    # print(len([number for number in x if number == 4]))
    # print(len([number for number in x if number == 5]))
    result = []
    i = 0
    while i < n:
        j = 2*i
        result.append(x[j]+x[j+1])
        i = i + 1
    return result

x = generateRN(10000)
plt.plot(x)
plt.show()