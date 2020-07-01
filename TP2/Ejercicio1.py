import numpy as np
import matplotlib.pyplot as mp
from enum import Enum


class Maquinas(Enum):
    primera = 0
    segunda = 1


# Funcion para dividir las muestras entre las dos maquinas del primer proveedor
def dividirMuestrasPorMaquina(tiemposMuestras, p):
    tiemposMuestrasPorMaquina = {}
    tiemposMuestrasPorMaquina[Maquinas.primera] = []
    tiemposMuestrasPorMaquina[Maquinas.segunda] = []

    for muestra in tiemposMuestras:
        u = np.random.rand()
        if u < p:
            maquina = Maquinas.primera
        else:
            maquina = Maquinas.segunda

        tiemposMuestrasPorMaquina[maquina].append(muestra)

    return tiemposMuestrasPorMaquina


# Funcion para calcular la demora
def calcularDemora(tiemposMuestras, tiemposProveedor, n):
    tiemposEsperaProveedor = np.zeros(n)
    tiempoDeEsperaAnterior = 0
    j = 1
    while j < n:
        deltaT = tiemposMuestras[j] - (tiemposMuestras[j - 1] + tiempoDeEsperaAnterior)
        tiempoDeEspera = tiemposProveedor[j - 1] - deltaT
        if tiempoDeEspera <= 0:
            tiempoDeEspera = 0
        tiemposEsperaProveedor[j] = tiempoDeEspera
        tiempoDeEsperaAnterior = tiempoDeEspera
        j += 1
    return tiemposEsperaProveedor


# Calcula los tiempos del proveedor 1 uniendo los tiempos de las dos maquinas
def calcularDemoraP1(tiemposMuestras, mu1, mu2, p, n):
    muestrasPorMaquina = dividirMuestrasPorMaquina(tiemposMuestras, p)
    tiemposMuestrasM1 = muestrasPorMaquina[Maquinas.primera]
    tiemposMuestrasM2 = muestrasPorMaquina[Maquinas.segunda]

    tiemposEsperaM1 = np.random.exponential(mu1, len(tiemposMuestrasM1))
    tiemposProveedorM1 = calcularDemora(
        tiemposMuestrasM1, tiemposEsperaM1, len(tiemposMuestrasM1)
    )

    tiemposEsperaM2 = np.random.exponential(mu2, len(tiemposMuestrasM2))
    tiemposProveedorM2 = calcularDemora(
        tiemposMuestrasM1, tiemposEsperaM2, len(tiemposMuestrasM2)
    )

    tiemposEspera = np.concatenate((tiemposEsperaM1, tiemposProveedorM2))
    tiemposProveedor = np.concatenate((tiemposProveedorM1, tiemposProveedorM2))

    return tiemposEspera, tiemposProveedor


def main():
    # Variables
    n = 100000
    muMuestras = 4
    p = 0.6
    muP1_1 = 0.7
    muP1_2 = 1
    muP2 = 0.8

    # Genero hora de llegada de muestras
    z = np.random.exponential(muMuestras, n)
    tiemposMuestras = np.concatenate(([0], np.cumsum(z)), axis=None)

    # Demoras proveedor 1
    tiemposP1, tiemposEsperaP1 = calcularDemoraP1(tiemposMuestras, muP1_1, muP1_2, p, n)

    # Demoras proveedor 2
    tiemposP2 = np.random.exponential(muP2, n)
    tiemposEsperaP2 = calcularDemora(tiemposMuestras, tiemposP2, n)

    # Calculo para cada proveedor los tiempos totales de cada diagnostico
    tiempoTotalP1 = (tiemposEsperaP1 + tiemposP1).mean()
    tiempoTotalP2 = (tiemposEsperaP2 + tiemposP2).mean()

    diferencia = (tiempoTotalP2 - tiempoTotalP1) * 100 / tiempoTotalP1

    print("N = ", n, "\n")

    print("Proveedor 1:")
    print(
        "El tiempo medio de espera es de: {:.3f} horas".format(tiemposEsperaP1.mean())
    )
    print(
        "La fraccion de las solicitudes que no esperaron es: {:.3f}\n".format(
            (n - np.count_nonzero(tiemposEsperaP1)) / n
        )
    )

    print("Proveedor 2:")
    print(
        "El tiempo medio de espera es de: {:.3f} horas".format(tiemposEsperaP2.mean())
    )
    print(
        "La fraccion de las solicitudes que no esperaron es: {:.3f}\n".format(
            (n - np.count_nonzero(tiemposEsperaP2)) / n
        )
    )

    print("El proveedor 1 es {:.3f}% veces mas rapido que el 2".format(diferencia))
    if diferencia >= 50:
        print("El instituto puede aceptar hacer la inversion")
    else:
        print("El instituto no puede aceptar hacer la inversion")


if __name__ == "__main__":
    main()
