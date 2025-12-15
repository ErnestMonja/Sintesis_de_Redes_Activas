import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

f_c = 1000
w_c = 2*np.pi*f_c
z, p, k = signal.butter(2, w_c, btype='lowpass', analog=True, output = 'zpk')
print("Ceros: ", z)
print("Polos: ", p)
print("Constante: ", k)

w = np.logspace(1, 5, 1000)
w, h = signal.freqs(num, den, w)

plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud [dB]")
plt.grid()
plt.show()