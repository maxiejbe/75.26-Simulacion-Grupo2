import numpy as np
import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from turtle import *

#Cantidad de pasos
N_steps = 1000

#Probabilidad: equiprobable para moverse en cualquiera de las 4 direcciones
#(arriba, abajo, derecha o izquierda)
prob = 0.25

def generate_positions_RW(N, colo):

    #grafico
    position = []
    animation = []
    x = 0
    y = 0
    position.append((x,y))

    #animacion
    setpos(0,0)
    shape("turtle")
    color(colo)

    for i in range(1,N):
        #Probabilidad random entre 0 y 1
        p = random.random()
        #Modifica posicion segun corresponda
        if p < 0.25:
          x += 1
          forward(10)
        elif 0.25 <= p < 0.5:
          y += 1
          #left(90)
          forward(10)
        elif 0.5 <= p < 0.75:
          x -= 1
          #left(180)
          backward(10)
        elif 0.75 <= p < 1:
          y -= 1
          #left(180)
          backward(10)

        #Agrega coordenadas movimiento nuevo a la lista de posiciones
        position.append((x,y))
        #plt.subplot()
        #plt.cla()
        #plt.plot(*zip(*position))
        #plt.show()
        #plt.pause(1)
    done()
    return position

def animate(x, y, position):
    p = sns.lineplot(x=x, y=y, data=position, color="r")
    p.tick_params(labelsize=17)
    plt.setp(p.lines,linewidth=7)

def randomWalk(N, colo):
  position = generate_positions_RW(N, colo)
  
  plt.plot(*zip(*position))
  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()
  return

randomWalk(N_steps, "mediumturquoise")

