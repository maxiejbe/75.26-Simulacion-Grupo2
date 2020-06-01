import numpy as np 
import matplotlib.pyplot as plt
import math

#Graficar la función de densidad de probabilidad

def my_dist(x):
    return (13/12*math.pi) - (x**2)/(math.pi)**3

x = np.arange(-math.pi/2, math.pi/2)
p = my_dist(x)
plt.plot(x, p)
plt.show()