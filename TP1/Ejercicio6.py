import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio2 import generate_rn
from scipy.stats import chi2


def group_results(numbers):
    grouped = np.zeros(5)
    for num in numbers:
        if(     num <= 2):
            np.put(grouped, 0, np.take(grouped, [0])+1)
        if( 2 < num <= 4):
            np.put(grouped, 1, np.take(grouped, [1])+1)
        if( 4 < num <= 6):
            np.put(grouped, 2, np.take(grouped, [2])+1)
        if( 6 < num <= 8):
            np.put(grouped, 3, np.take(grouped, [3])+1)
        if( 8 < num     ):
            np.put(grouped, 4,np.take(grouped, [4])+1)
    return grouped

def chi_squared_test(mu, sigma, n, observed_values) :
    observed_grouped = group_results(observed_values)
    theoretical = np.random.normal(mu, sigma, n)
    theoretical_grouped = group_results(theoretical)

    i,D2 = 0, 0
    while (i < len(observed_grouped)):
        D2 += (((observed_grouped[i] - theoretical_grouped[i])**2)/theoretical_grouped[i])
        i += 1
    top_limit = chi2.ppf(0.99, df=4)
    return D2 <= top_limit

def multiplechi_squared_test(n, tests_n):
    observed_values = generate_rn(n)
    mu, sigma = 5, 2.41523
    resutls = [chi_squared_test(mu, sigma,n, observed_values) for _ in range(tests_n)]
    return resutls


def main():
    n, tests_n = 10000, 100
    results =  multiplechi_squared_test(n, tests_n)
    print("El test ACEPTA la hipotesis nula {} veces.".format(len([result for result in results if result])))
    print("El test RECHAZA la hipótesis nula {} veces".format(len([result for result in results if not result])))
    

if __name__ == "__main__":
    main()


