# coding=utf-8
from Ejercicio4 import generate_standard_normal_acceptance_rejection
import numpy as np
import scipy.stats as stats


def test_standard_normal_kolmogorov_smirnov(tests_n, numbers_per_test, alpha, output):
    rejected_tests_n = 0

    for i in range(tests_n):
        numbers = generate_standard_normal_acceptance_rejection(numbers_per_test, False)

        d, pval = stats.kstest(numbers, "norm")
        if output:
            print("P(KS dataset {}): {}".format(i, pval))

        if pval < alpha:
            rejected_tests_n += 1

    rejection_p = float(rejected_tests_n) / tests_n
    if output:
        print("Tests KS realizados: {}".format(tests_n))
        print("Tests KS rechazados: {}".format(rejected_tests_n))
    return rejection_p


def main():
    tests_n, alpha = 10, 0.01
    print("Cantidad de tests a realizar: {}".format(tests_n))
    print("Nivel de significación (Alpha): {}".format(alpha))

    numbers_per_test = 100000
    print("Generador: Normal(mu={},sigma={})".format(0, 1))
    print("Cantidad de Nros:{}".format(numbers_per_test))

    rejection_p = test_standard_normal_kolmogorov_smirnov(
        tests_n, numbers_per_test, alpha, True
    )
    print("Probabilidad de rechazo según test KS: {}".format(rejection_p))


if __name__ == "__main__":
    main()
