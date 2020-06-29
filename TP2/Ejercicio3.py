import pandas as pd
from enum import Enum
from mpmath import *
from random import randint
import numpy as np
import matplotlib.pyplot as plt

accionA = pd.read_csv("accion A.csv")
accionB = pd.read_csv("accion B.csv")

lista_valores_A = accionA["Valor"].to_list()
lista_valores_B = accionB["Valor"].to_list()


class Direction(Enum):
    Sube = 0
    Baja = 1


cantidades = {}
cantidades[Direction.Sube, Direction.Sube] = 0
cantidades[Direction.Sube, Direction.Baja] = 0
cantidades[Direction.Baja, Direction.Sube] = 0
cantidades[Direction.Baja, Direction.Baja] = 0

cantidades_totales = {}
cantidades_totales[Direction.Sube] = 0
cantidades_totales[Direction.Baja] = 0


def obtener_direccion(lista, idx1, idx2):
    if (lista[idx2] - lista[idx1]) > 0:
        return Direction.Sube
    return Direction.Baja


def encontrar_cantidades(lista):
    for i in range(len(lista) - 2):
        comp1 = obtener_direccion(lista, i, i + 1)
        comp2 = obtener_direccion(lista, i + 1, i + 2)

        cantidades_totales[comp1] += 1
        cantidades[comp1, comp2] += 1

    return cantidades, cantidades_totales


def encontrar_probabilidades(lista):
    cantidades, cantidades_totales = encontrar_cantidades(lista)
    probabilidades = {}
    probabilidades[Direction.Sube, Direction.Sube] = (
        cantidades[Direction.Sube, Direction.Sube] / cantidades_totales[Direction.Sube]
    )
    probabilidades[Direction.Sube, Direction.Baja] = (
        cantidades[Direction.Sube, Direction.Baja] / cantidades_totales[Direction.Sube]
    )
    probabilidades[Direction.Baja, Direction.Sube] = (
        cantidades[Direction.Baja, Direction.Sube] / cantidades_totales[Direction.Baja]
    )
    probabilidades[Direction.Baja, Direction.Baja] = (
        cantidades[Direction.Baja, Direction.Baja] / cantidades_totales[Direction.Baja]
    )

    return probabilidades


prob_A = encontrar_probabilidades(lista_valores_A)
prob_B = encontrar_probabilidades(lista_valores_B)

print(prob_A)
print(prob_B)

#simulacion accion
def simulacion(diccionario):
  numeros_aleatorios = []
  for i in range(365):
    numeros_aleatorios.append(randint(0,1))

  valores_accion = [40]
  estado_anterior = True #True si aumenta, False si baja, asumimos que empieza en un aumento como valor "semilla"
  for i in range(1, 365):
    nro = numeros_aleatorios[i]
    matriz = matrix([[diccionario[Direction.Sube, Direction.Sube], diccionario[Direction.Sube, Direction.Baja]], [diccionario[Direction.Baja, Direction.Sube], diccionario[Direction.Baja, Direction.Baja]]])
    expm(matriz**i)

    if estado_anterior:
      if nro <= matriz[0,0]:
        valores_accion.append(randint(valores_accion[i-1], valores_accion[i-1]+5))
      else:
        valores_accion.append(randint(valores_accion[i-1]-5,valores_accion[i-1]))
    if not estado_anterior:
      if nro <= matriz[1,0]:
        valores_accion.append(randint(valores_accion[i-1], valores_accion[i-1]+5))
      else:
        valores_accion.append(randint(valores_accion[i-1]-5,valores_accion[i-1]))
  return valores_accion

valores_accion_A = simulacion(prob_A)
valores_accion_B = simulacion(prob_B)

x = np.arange(0, 365)

plt.plot(x, valores_accion_A)
plt.xlabel('Dias')
plt.ylabel('Valor acción')
plt.title('Evolución anual acción A')
plt.show()

plt.plot(x, valores_accion_B)
plt.xlabel('Dias')
plt.ylabel('Valor acción')
plt.title('Evolución anual acción B')
