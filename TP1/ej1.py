# implementar un Generador Congruencial Lineal (GCL) de módulo 2
# 32, multiplicador
# 1013904223, incremento de 1664525 y semilla igual a la parte entera del promedio de los números de padrón de los
# integrantes del grupo
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

def gcl(a, x0, c, m, iteraciones):
    valores = np.array([])
    i = 0
    while i < iteraciones:
        x = (a*x0 + c) % m
        x0 = x
        valores = np.append(valores, x)
        i += 1
    return valores

a = 1013904223
x0 = (101456 + 102214 + 94511 + 95295) // 4
c = 1664525
m = 2**32
resultado = gcl(a, x0, c, m, 10)
print (resultado)
