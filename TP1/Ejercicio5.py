import numpy as np
import sympy as sym
import scipy.stats as stats
import matplotlib.pyplot as plt
from Ejercicio1 import gcl01, gcl

# Aplicar un gap test al generador congruencial lineal implementado en el ejercicio 1 utilizando el intervalo [0,2 - 0,5].
# Analizar el resultado obtenido, e indicar si la distribución de probabilidades pasa o no el test.
# Considerar un nivel de significación del 1%.

def gapTest(numberOfGaps, alpha, beta):
    i = 0
    gap = 0
    gaps = np.zeros(numberOfGaps)
    number = gcl01(1)
    while i < numberOfGaps:
        if((number > alpha) and (number <= beta)):
            gap += 1
        else:
            np.append(gaps, gap + 1)
            gaps[i] = gap + 1
            i += 1
            gap = 0
        number_gcl = gcl(1, x0 = number)
        number = gcl01(1, x0 = number_gcl)

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
plt.title('Histograma de la distribución de las longitudes de gaps para 100.000 gaps generados')
plt.xlabel('Gaps')
plt.ylabel('Cantidad de gaps')
plt.show()
maxgap = max(gaps)
print("El gap mas largo fue: ", maxgap)
nivelDeSignifiacion = 0.01
if pValor < nivelDeSignifiacion:
    print("Para un nivel de significación del ", nivelDeSignifiacion*100, "%, obtenemos que podemos rechazar la hipótesis nula (h=0)")
else:
    print("Para un nivel de significación del ", nivelDeSignifiacion*100, "%, obtenemos que no podemos rechazar la hipótesis nula (h=0)")



