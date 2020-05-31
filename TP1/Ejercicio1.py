# implementar un Generador Congruencial Lineal (GCL) de módulo 2
# 32, multiplicador
# 1013904223, incremento de 1664525 y semilla igual a la parte entera del promedio de los números de padrón de los
# integrantes del grupo

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt


def gcl(a, x0, c, m, iterations):
    values = np.array([])
    i = 0
    while i < iterations:
        x = (a * x0 + c) % m
        x0 = x
        values = np.append(values, x)
        i += 1
    return values


def gcl01(a, x0, c, m, iterations):
    values = gcl(a, x0, c, m, iterations)
    values_01 = values / m
    return values_01


def gcl_parameters():
    a = 1013904223
    x0 = (101456 + 102214 + 94511 + 95295) // 4
    c = 1664525
    m = 2 ** 32
    return a, x0, c, m


def gcl_with_parameters(iterations):
    a, x0, c, m = gcl_parameters()
    return gcl(a, x0, c, m, iterations)


def gcl01_with_parameters(iterations):
    a, x0, c, m = gcl_parameters()
    return gcl01(a, x0, c, m, iterations)


def main():
    np.set_printoptions(suppress=True)
    print("a) Informar los primeros 10 números generados.")
    resultado_a = gcl_with_parameters(10)
    print(resultado_a)

    # b) Modificar el GCL para que devuelva números al azar entre 0 y 1
    print("b) Modificar el GCL para que devuelva números al azar entre 0 y 1")
    np.set_printoptions(suppress=True)
    results_b = gcl01_with_parameters(100000)
    print(results_b)

    # c) Realizar un histograma mostrando 100.000 valores generados en el punto b.
    print("c) Realizar un histograma mostrando 100.000 valores generados en el punto b")
    num_bins = 6
    plt.hist(results_b, num_bins, facecolor="purple", alpha=0.5)
    plt.show()
    return


if __name__ == "__main__":
    main()
