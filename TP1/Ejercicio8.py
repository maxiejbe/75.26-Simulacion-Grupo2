import numpy as np
import random
from matplotlib import pyplot as plt

# Cantidad de pasos
n_steps = 1000

# Probabilidad: equiprobable para moverse en cualquiera de las 4 direcciones
# (arriba, abajo, derecha o izquierda)
prob = 0.25

# board_size_x = 50
# board_size_y = 50


def random_walk(N):

    position = []
    x = 0
    y = 0
    position.append((x, y))

    for i in range(1, N):
        # Probabilidad random entre 0 y 1
        p = random.random()
        # Modifica posicion segun corresponda
        if p < 0.25:
            x += 1
        elif 0.25 <= p < 0.5:
            y += 1
        elif 0.5 <= p < 0.75:
            x -= 1
        elif 0.75 <= p < 1:
            y -= 1

        # Agrega coordenadas movimiento a la lista de posiciones
        position.append((x, y))
        plt.plot(
            *zip(*position), color="blue",
        )
        # plt.xlim(-board_size_x, board_size_x)
        # plt.ylim(-board_size_y, board_size_y)
        point = plt.plot(x, y, "--bo", color="green")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.pause(0.001)
        for p in point:
            p.remove()

    plt.show()
    return


random_walk(n_steps)
