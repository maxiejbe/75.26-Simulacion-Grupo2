import numpy as np
import sympy as sym
import scipy.stats as stats
import matplotlib.pyplot as plt
from Ejercicio1 import gcl01, gcl

# Aplicar un gap test al generador congruencial lineal implementado en el ejercicio 1 utilizando el intervalo [0,2 - 0,5].
# Analizar el resultado obtenido, e indicar si la distribución de probabilidades pasa o no el test.
# Considerar un nivel de significación del 1%.


def gap_test(number_of_gaps, alpha, beta):
    current_gap = 0
    gaps = np.zeros(number_of_gaps)
    number = gcl01(1)
    while current_gap < number_of_gaps:
        if (number > alpha) and (number <= beta):
            current_gap += 1
        else:
            gaps[current_gap] = gaps[current_gap] + 1
        number_gcl = gcl(1, x0=number)
        number = gcl01(1, x0=number_gcl)

    # probabilidades esperadas
    p = beta - alpha
    j = 0
    max_gap_size = int(max(gaps)) + 1
    observed_p = np.zeros(max_gap_size)
    expected_p = np.zeros(max_gap_size)

    while j < max_gap_size:
        number_of_occ = np.count_nonzero(gaps == j)
        observed_p[j] = number_of_occ / number_of_gaps
        expected_p[j] = p * ((1 - p) ** (j))
        j += 1
    [h, pValor] = stats.chisquare(observed_p, expected_p)
    return pValor, gaps


[pValor, gaps] = gap_test(100000, 0.2, 0.5)
plt.hist(gaps, bins=50, color="purple")
plt.xlabel("Tamaño de gaps")
plt.ylabel("Frecuencia")
plt.show()
maxgap = max(gaps)
print("El gap de tamaño máximo fue: ", maxgap)
alpha = 0.01
if pValor < alpha:
    print(
        "Para un nivel de significación del ",
        alpha * 100,
        "%, obtenemos que podemos rechazar la hipótesis nula (h=0)",
    )
else:
    print(
        "Para un nivel de significación del ",
        alpha * 100,
        "%, obtenemos que no podemos rechazar la hipótesis nula (h=0)",
    )
