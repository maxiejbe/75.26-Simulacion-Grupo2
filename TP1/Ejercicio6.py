import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio2 import generate_rn
from scipy.stats import chi2
from scipy import stats

k_classes = 10


def group_observed(numbers):
    grouped = np.zeros(k_classes)
    for i in range(k_classes):
        grouped[i] = np.count_nonzero(numbers == i)
    return grouped


def theoretical_normal_p(mu, sigma):
    theoretical_p = np.zeros(k_classes)
    for i in range(k_classes):
        pi = stats.norm.cdf(i, mu, sigma)
        theoretical_p[i] = stats.norm.cdf(i + 1, mu, sigma) - pi

    return theoretical_p


def chi_squared_test(n, mu, sigma, alpha):
    observed_values = generate_rn(n)
    observed_grouped = group_observed(observed_values)
    theoretical_p = theoretical_normal_p(mu, sigma)

    # Python chisquare test p
    [h, pValor] = stats.chisquare(observed_grouped / n, theoretical_p)

    i, D2 = 0, 0
    while i < len(observed_grouped):
        D2 = D2 + (
            ((observed_grouped[i] - (theoretical_p[i] * n)) ** 2)
            / (theoretical_p[i] * n)
        )
        i += 1
    # top_limit = chi2.ppf(1 - alpha, df=k_classes)
    # scaled_d2 = D2 / n * k_classes
    # or scaled_d2 <= top_limit
    if pValor < (1 - alpha):
        print("H0 es rechazada")
    else:
        print("H1 es aceptada")


def main():
    mu, sigma, n, alpha = 7, 35 / 6, 10000, 0.01
    chi_squared_test(n, mu, sigma, alpha)


if __name__ == "__main__":
    main()
