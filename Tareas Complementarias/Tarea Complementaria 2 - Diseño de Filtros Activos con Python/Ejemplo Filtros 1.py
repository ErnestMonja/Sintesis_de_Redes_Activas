import numpy as np
from scipy import signal

fc = 1000            # Hz
wc = 2 * np.pi * fc  # rad/s

num, den = signal.butter(N=2, Wn=wc, analog=True)

print("Numerador:", num)
print("Denominador:", den)