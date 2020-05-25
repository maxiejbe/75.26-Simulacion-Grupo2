# coding=utf-8
from Ejercicio4 import generateNormalAcceptanceRejection
import numpy as np
import scipy.stats as stats


def generateNormal(n, mu, sigma):
    def generateNormedNormal():
        numbers = generateNormalAcceptanceRejection(n, mu, sigma, False)
        # Shifteo y escalo los números para hacer el test contra N(0,1)
        return (numbers - mu) / sigma

    return generateNormedNormal


def testNormalKolmogorovSmirnov(normalGenerator, testsN, alpha, output):
    rejectedTestsN = 0

    for i in range(testsN):
        normedNumbers = normalGenerator()

        d, pval = stats.kstest(normedNumbers, "norm")
        if output:
            print("P(KS dataset {}): {}".format(i, pval))

        if pval < alpha:
            rejectedTestsN += 1

    rejectionProbability = float(rejectedTestsN) / testsN
    if output:
        print("Tests KS realizados: {}".format(testsN))
        print("Tests KS rechazados: {}".format(rejectedTestsN))
    return rejectionProbability


def main():
    testsN, alpha = 10, 0.01
    print("Cantidad de tests a realizar: {}".format(testsN))
    print("Nivel de significación (Alpha): {}".format(alpha))

    n, mu, sigma = 10000, 25, 2
    print("Generador: Normal(mu={},sigma={})".format(mu, sigma))
    print("Cantidad de Nros:{}".format(n))

    rejectionProbability = testNormalKolmogorovSmirnov(
        generateNormal(n, mu, sigma), testsN, alpha, True
    )
    print("Probabilidad de rechazo según test KS: {}".format(rejectionProbability))


if __name__ == "__main__":
    main()
