import numpy as np
import matplotlib.pyplot as mp

#Variables
n = 100000
mediaMuestras = 4 
p = 0.6
media1 = .7
media2 = 1
mediaP2 = .8

#Hora de llegada de las muestras
z = np.random.exponential(mediaMuestras, n)
tiemposMuestras = np.concatenate(([0], np.cumsum(z)), axis=None)

#Tiempos del proveedor 1
tiemposP1 = np.zeros(n)
u = np.random.rand(n)
for i in range (n):
    if (u[i] < p): 
        z = np.random.exponential(media1)
    else: 
        z = np.random.exponential(media2)
    tiemposP1[i] = z
    
#Tiempos del proveedor 2
tiemposP2 = np.random.exponential(mediaP2, n)

#Funcion para calcular demora
def calcularDemora(tiemposMuestras, tiemposProveedor, n):
    tiemposEsperaProveedor = np.zeros(n)
    tiempoDeEsperaAnterior = 0
    j = 1
    while j < n:
        deltaT = tiemposMuestras[j] + tiempoDeEsperaAnterior - tiemposMuestras[j-1]
        tiempoDeEspera =  tiemposProveedor[j-1] - deltaT
        if tiempoDeEspera <= 0:
            tiempoDeEspera = 0
        tiemposEsperaProveedor[j] = tiempoDeEspera
        tiempoDeEsperaAnterior = tiempoDeEspera
        j += 1
    return tiemposEsperaProveedor

#Demoras proveedor 1
tiemposEsperaP1 = calcularDemora(tiemposMuestras, tiemposP1, n)

#Demoras proveedor 2
tiemposEsperaP2 = calcularDemora(tiemposMuestras, tiemposP2, n)

#Calculo para cada proveedor los tiempos totales de cada diagnostico

tiempoTotalP1 = (tiemposEsperaP1 + tiemposP1).mean()
tiempoTotalP2 = (tiemposEsperaP2 + tiemposP2).mean()

diferencia = (tiempoTotalP2 - tiempoTotalP1)*100 / tiempoTotalP1

print("N = ", n, "\n")

print("Proveedor 1:")
print("El tiempo medio de espera es de: {:.3f} horas".format(tiemposEsperaP1.mean()))
print("La fraccion de las solicitudes que no esperaron es: {:.3f}\n".format((n - np.count_nonzero(tiemposEsperaP1))/n))

print("Proveedor 2:")
print("El tiempo medio de espera es de: {:.3f} horas".format(tiemposEsperaP2.mean()))
print("La fraccion de las solicitudes que no esperaron es: {:.3f} \n".format((n - np.count_nonzero(tiemposEsperaP2))/n))
print("El proveedor 1 es {:.3f}% veces mas rapido que el 2".format(diferencia))
if diferencia >= 50:
    print("El instituto puede aceptar hacer la inversion")
else:
    print("El instituto no puede aceptar hacer la inversion")
    

