import numpy as np 
import matplotlib.pyplot as plt
import math
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

x = np.linspace(-np.pi/2, np.pi/2, 2000)
y = F(x)

plt.plot(x, y, '-r')
plt.show()

#plt.hist(y)

#invierto los ejes
#plt.plot(y, x)

#interpolo con puntos equiespaciados 0,1
x_interp = np.linspace(-np.pi/2, np.pi/2, 30)
y_interp = np.interp(x_interp, y, x)

plt.plot(y_interp, x_interp)

