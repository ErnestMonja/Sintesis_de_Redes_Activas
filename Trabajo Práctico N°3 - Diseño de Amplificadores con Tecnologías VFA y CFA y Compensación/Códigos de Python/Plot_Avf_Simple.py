import numpy as np
import matplotlib.pyplot as plt

# Ganancia Ideal
Avfi = 10

# Polos calculados a lazo cerrado
fp1 = 102e3
fp2 = 4.9e6

# Frecuencia
f = np.logspace(np.log10(10), np.log10(20e6), 2000) # De 10Hz a 20MHz pero en rad/s
w = 2 * np.pi * f

# Polos
wp1 = 2*np.pi*fp1
wp2 = 2 * np.pi * fp2

# Función de transferencia
Avf = Avfi / ((1 + 1j*w/wp1) * (1 + 1j*w/wp2))

# Módulo en dB
Avf_dB = 20 * np.log10(np.abs(Avf))

plt.figure()
plt.semilogx(f, Avf_dB)
plt.grid(True, which='both')

plt.axvline(fp1, linestyle='--')
plt.axvline(fp2, linestyle='--')
plt.axhline(17,  linestyle='-.')

# Etiquetas
plt.text(fp1, -35, '  fp1 = 102 kHz', rotation=0, va='bottom')
plt.text(fp2, -35, '  fp2 = 4.9 MHz', rotation=0, va='bottom')
plt.text(10,  17, ' 17 dB',  rotation=0, va='bottom')

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('|Avf(jω)| [dB]')
plt.show()
