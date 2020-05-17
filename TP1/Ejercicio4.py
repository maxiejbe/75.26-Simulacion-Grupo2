import numpy as np
import matplotlib.pyplot as plt


def generateNormal(n, mu, sigma):
    return np.random.normal(mu, sigma, n)


# mean and standard deviation
n, mu, sigma = 100000, 25, 2
numbers = generateNormal(n, mu, sigma)

print(len(numbers))
plt.hist(numbers, bins="sturges")
plt.show()
