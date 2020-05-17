import numpy as np 
import matplotlib.pyplot as plt
import math

#Graficar la función de densidad de probabilidad

def f(x):
    return (13/12*math.pi) - (x**2)/(math.pi)**3

x = np.arange(-math.pi/2, math.pi/2)
p = f(x)
plt.plot(x, p)
plt.show()

#Calcular y graficar la función de probabilidad acumulada y su inversa

#Función de probabilidad acumulada (Función de distribución):
def F(x):
    if x < (-math.pi/2):
        return 0
    elif x >= -math.pi/2 and x <= math.pi/2:
        return (13*x/12*math.pi)-(x**3/3*(math.pi**3))
    return 1
