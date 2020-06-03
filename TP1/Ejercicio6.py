import numpy as np
import matplotlib.pyplot as plt
import math
from Ejercicio2 import generate_rn
from scipy.stats import chi2
from scipy import stats


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

def chi_squared_test(n, mu, sigma):
    observed_values = generate_rn(n)
    observed_grouped = group_results(observed_values)
    theoretical_grouped = [stats.norm.cdf(2, mu, sigma), 
                           stats.norm.cdf(4, mu, sigma) - stats.norm.cdf(2, mu, sigma),
                           stats.norm.cdf(6, mu, sigma) - stats.norm.cdf(4, mu, sigma),
                           stats.norm.cdf(8, mu, sigma) - stats.norm.cdf(6, mu, sigma),
                           1 - stats.norm.cdf(8, mu, sigma)]
    i,D2 = 0, 0
    while (i < len(observed_grouped)):
        D2 += (observed_grouped[i] - (theoretical_grouped[i]*n))**2
        D2 = D2/theoretical_grouped[i]*n
        i += 1
    top_limit = chi2.ppf(0.99, df=4)

    print('D2: ', D2)
    print('Top limit: ', top_limit)
    if D2 <= top_limit:
        print('H0 es aceptada')
    else:
        print('H1 es rechazada')


def main():
    mu, sigma, n = 5, 2, 10000
    chi_squared_test(n, mu, sigma)
    

if __name__ == "__main__":
    main()


