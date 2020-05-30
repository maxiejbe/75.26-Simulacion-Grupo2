# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import random as rn
import math


def generate_normal_acceptance_rejection(n, mu, sigma, output):
    numbers = generate_standard_normal_acceptance_rejection(n, output)
    return (numbers * sigma) + mu


def generate_standard_normal_acceptance_rejection(n, output):
    # Theory: Derive Fx(t)/Fy(t) => t=1
    c = 2 * (stats.norm.pdf(1)) / stats.expon.pdf(1)

    numbers = np.array([])
    accepted_n, rejected_n = 0, 0
    while accepted_n < n:
        x = np.random.exponential()
        p = stats.norm.pdf(x) / (c * stats.expon.pdf(x))
        y = rn.random()

        if y <= p:
            r1 = rn.random()
            if r1 < 0.5:
                numbers = np.append(numbers, x)
            else:
                numbers = np.append(numbers, -x)

            accepted_n += 1
            continue
        else:
            rejected_n += 1

    total_n = accepted_n + rejected_n
    rejection_percentage = rejected_n * 100 / total_n
    if output:
        print("Cantidad aceptados={}".format(accepted_n))
        print("Cantidad rechazados={}".format(rejected_n))
        print("Porcentaje de rechazos={}%".format(rejection_percentage))

    return numbers


def draw_histogram(numbers, show):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(numbers, weights=np.zeros_like(numbers) + 1.0 / numbers.size, bins=20)
    ax.set_xlabel("Numbers range")
    ax.set_ylabel("Relative frequency")
    if show:
        plt.show()


def draw_normal_pdf(mu, sigma):
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), "-r")
    plt.show()


def main():
    # Aplicando el algoritmo de Aceptación y rechazo se pide:
    # a) Generar 100.000 número aleatorios con distribución Normal de media 25 y desvío estándar 2 .
    n, mu, sigma = 100000, 25, 2
    print("Cantidad de números a generar={}".format(n))
    print("Distribución Normal(mu={},sigma={})".format(mu, sigma))

    numbers = generate_normal_acceptance_rejection(n, mu, sigma, True)

    # b) Realizar un histograma de frecuencias relativas con todos los valores obtenidos.
    draw_histogram(numbers, True)

    # c) Comparar, en el mismo gráfico, el histograma realizado en el punto anterior con la función de densidad de
    # probabilidad brindada por el lenguaje elegido (para esta última distribución utilizar un gráfico de línea).
    draw_histogram(numbers, False)
    draw_normal_pdf(mu, sigma)

    # d) Calcular la media y la varianza de la distribución obtenida y compararlos con los valores teóricos
    print("Valores teóricos: Media={},Varianza={}".format(mu, sigma ** 2))
    print(
        "Valores prácticos: Media={},Varianza={}".format(
            np.average(numbers), np.var(numbers)
        )
    )


if __name__ == "__main__":
    main()
