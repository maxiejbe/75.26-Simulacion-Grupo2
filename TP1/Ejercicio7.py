import numpy as np
import scipy.stats as stats
from Ejercicio4 import generateNormalAcceptanceRejection

n, mu, sigma = 1000, 25, 2
numbers = generateNormalAcceptanceRejection(n, mu, sigma)

print(numbers)
