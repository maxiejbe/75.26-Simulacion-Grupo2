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
        if((number > alpha) and (number <= beta)):
            gap += 1
        else:
            np.append(gaps, gap + 1)
            gaps[i] = gap + 1
            i += 1
            gap = 0
        x0 = number
    #probabilidades esperadas
    p = beta - alpha
    expected = np.zeros(numberOfGaps)
    j = 0
    while j < len(gaps):
        num = gaps[j]
        expected[j] = p*((1-p)**(num-1))*(numberOfGaps)
        j += 1

    [h,pValor] = stats.chisquare(gaps, expected)
    return pValor, gaps

[pValor, gaps] = gapTest(100000, 0.2, 0.5)
plt.hist(gaps, bins = 50, color = 'purple')
plt.show()
if pValor < 0.01:
    print("Rechazo")
else:
    print("Acepto")



