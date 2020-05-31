import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


#%matplotlib inline

#Graficar la función de densidad de probabilidad

def f(x):
    return (13/(12*math.pi)) - (x**2)/((math.pi)**3)

x = np.arange(-math.pi/2, math.pi/2)
p = f(x)
plt.plot(x, p)
plt.show()

#Calcular y graficar la función de probabilidad acumulada y su inversa

#Función de probabilidad acumulada (Función de distribución):
def F(x):
    return ((13*x)/(12*np.pi))-((x**3)/(3*(np.pi**3))) + 0.5

#Grafico funcion distribucion original
x = np.linspace(-np.pi/2, np.pi/2, 30)
y = [F(xi) for xi in x]
plt.plot(x, y, '-r')
plt.show()

#invierto los ejes
x, y = y, x
plt.plot(x, y)
plt.show()

#interpolo con puntos equiespaciados 0,1
F_inversa = interpolate.interp1d(x, y)

x_new = gcl01(100000)
y_new = F_inversa(x_new)

plt.hist(y_new)
