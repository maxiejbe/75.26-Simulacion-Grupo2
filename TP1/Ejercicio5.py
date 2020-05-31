import numpy as np
import sympy as sym
import scipy.stats as stats
import matplotlib.pyplot as plt
from Ejercicio1 import gcl01

# Aplicar un gap test al generador congruencial lineal implementado en el ejercicio 1 utilizando el intervalo [0,2 - 0,5].
# Analizar el resultado obtenido, e indicar si la distribución de probabilidades pasa o no el test.
# Considerar un nivel de significación del 1%.

def gapTest(numberOfGaps, alpha, beta):
    i = 0
    x0 = (101456 + 102214 + 94511 + 95295) // 4
    gap = 0
    gaps = np.zeros(numberOfGaps)
    while i < numberOfGaps:
        randomNumber = gcl01(1013904223, x0, 1664525, 2^32, 1)
        number = randomNumber[0]
        if((number < alpha) and (number >= beta)):
            gap += 1
        else:
            np.append(gaps, gap + 1)
            gaps[i] = gap + 1
            i += 1
            gap = 0
        x0 = number
    #probabilidades esperadas
    p = beta - alpha
    gapMax = max(gaps)
    expected = np.zeros(int(gapMax))
    for j in range(int(gapMax)):
        expected[j] = p*((1-p)**(j-1))*(numberOfGaps)

    [h,pValor] = stats.chisquare(gaps, expected)
    return pValor, gaps

[pValor, gaps] = gapTest(100000, 0.2, 0.5)
gapMax = max(gaps)
plt.axis([0, gapMax, 0, gapMax])
plt.bar(gaps, facecolor = 'purple')
plt.show()
if pValor < 0.01:
    print("Rechazo")
else:
    print("Acepto")



