import numpy as np
import matplotlib.pyplot as mp
from enum import Enum


# Hora de llegada de las muestras
def generar_tiempos_muestras(n, mu_muestras):
    z = np.random.exponential(mu_muestras, n)
    tiempos_muestras = np.concatenate(([0], np.cumsum(z)), axis=None)
    return tiempos_muestras


class Maquinas(Enum):
    primera = 0
    segunda = 1


def dividir_muestras_por_maquina(tiempos_muestras, p):
    tiempos_muestras_por_maquina = {}
    tiempos_muestras_por_maquina[Maquinas.primera] = []
    tiempos_muestras_por_maquina[Maquinas.segunda] = []

    for muestra in tiempos_muestras:
        u = np.random.rand()
        if u < p:
            maquina = Maquinas.primera
        else:
            maquina = Maquinas.segunda

        tiempos_muestras_por_maquina[maquina].append(muestra)

    return tiempos_muestras_por_maquina


# Tiempos del proveedor 1
def calcular_tiempos_espera_p1(tiempos_muestras, mu1, mu2, p, n):
    muestras_por_maquina = dividir_muestras_por_maquina(tiempos_muestras, p)
    tiempos_muestras_m1 = muestras_por_maquina[Maquinas.primera]
    tiempos_muestras_m2 = muestras_por_maquina[Maquinas.segunda]

    tiempos_espera_m1 = np.random.exponential(mu1, len(tiempos_muestras_m1))
    tiempos_proveedor_m1 = calcular_tiempos_espera(
        tiempos_muestras_m1, tiempos_espera_m1, mu1, len(tiempos_muestras_m1),
    )
    tiempos_espera_m2 = np.random.exponential(mu2, len(tiempos_muestras_m2))
    tiempos_proveedor_m2 = calcular_tiempos_espera(
        tiempos_muestras_m1, tiempos_espera_m2, mu2, len(tiempos_muestras_m2),
    )

    tiempos_espera = np.concatenate((tiempos_espera_m1, tiempos_proveedor_m2))
    tiempos_proveedor = np.concatenate((tiempos_proveedor_m1, tiempos_proveedor_m2))
    return tiempos_espera, tiempos_proveedor


def calcular_tiempos_espera_p2(tiempos_muestras, mu, n):
    tiempos_espera = np.random.exponential(mu, n)
    tiempos_proveedor = calcular_tiempos_espera(tiempos_muestras, tiempos_espera, mu, n)
    return tiempos_espera, tiempos_proveedor


# Funcion para calcular tiempos de espera
def calcular_tiempos_espera(tiempos_muestras, tiempos_proveedor, mu, n):
    tiempos_espera_proveedor = np.zeros(n)
    j = 1

    while j < n:
        termina_de_atender = (
            tiempos_muestras[j - 1]
            + tiempos_proveedor[j - 1]
            + tiempos_espera_proveedor[j - 1]
        )
        delta_tiempo = termina_de_atender - tiempos_muestras[j]

        if delta_tiempo >= 0:
            tiempos_espera_proveedor[j - 1] = delta_tiempo

        j += 1
    return tiempos_espera_proveedor


def main():
    # Variables
    n = 100000
    mu_muestras = 4
    p = 0.6
    mu_p1_1 = 0.7
    mu_p1_2 = 1
    mu_p2 = 0.8

    # Genero hora de llegada de muestras
    tiempos_muestras = generar_tiempos_muestras(n, mu_muestras)

    # Demoras proveedor 1
    tiempos_espera_p1, tiempos_proveedor_p1 = calcular_tiempos_espera_p1(
        tiempos_muestras, mu_p1_1, mu_p1_2, p, n
    )

    # Demoras proveedor 2
    tiempos_espera_p2, tiempos_proveedor_p2 = calcular_tiempos_espera_p2(
        tiempos_muestras, mu_p2, n
    )

    # Calculo para cada proveedor los tiempos totales de cada diagnostico
    tiempo_total_p1 = (tiempos_proveedor_p1 + tiempos_espera_p1).mean()
    tiempo_total_p2 = (tiempos_proveedor_p2 + tiempos_espera_p2).mean()

    diferencia = (tiempo_total_p2 - tiempo_total_p1) * 100 / tiempo_total_p1

    print("N = ", n, "\n")

    print("Proveedor 1:")
    print(
        "El tiempo medio de espera es de: {:.3f} horas".format(
            tiempos_proveedor_p1.mean()
        )
    )
    print(
        "La fraccion de las solicitudes que no esperaron es: {:.3f}%\n".format(
            (n - np.count_nonzero(tiempos_proveedor_p1)) / n * 100
        )
    )

    print("Proveedor 2:")
    print(
        "El tiempo medio de espera es de: {:.3f} horas".format(
            tiempos_proveedor_p2.mean()
        )
    )
    print(
        "La fraccion de las solicitudes que no esperaron es: {:.3f}% \n".format(
            (n - np.count_nonzero(tiempos_proveedor_p2)) / n * 100
        )
    )
    print("El proveedor 1 es {:.3f}% veces mas rapido que el 2".format(diferencia))
    if diferencia >= 50:
        print("El instituto puede aceptar hacer la inversion")
    else:
        print("El instituto no puede aceptar hacer la inversion")


if __name__ == "__main__":
    main()
