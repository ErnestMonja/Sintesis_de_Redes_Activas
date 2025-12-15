import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


## Frecuencias de Corte:
f1 = 500      # Hz
f2 = 1500     # Hz
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2
Wn = [w1, w2]


## Orden del Filtro Prototipo Pasa Bajos:
N = 2


## Aproximación de Filtro Pasa Banda con ButterWorth:
num, den = signal.butter(N, Wn, btype='bandpass', analog = True)


## Obtención de los Ceros, Polos y Constante:
z, p, k = signal.tf2zpk(num, den)
print("Ceros: ", z)                                 # 0 ; 0
print("Polos: ", p)                                 # -3116.32 + j7735.93 ; -3116.32 - j7735.93 ; -1326.56 + j3293.05 ; -1326.56 - j3293.05
print("Constante: ", k)                             # 39478417.60


## Descomposición en funciones bicuadráticas:
sos = signal.tf2sos(num, den)                       # [3.94784176e+07 0 0 ; 1 6.23264064e+03 6.95561180e+07]
print("Secciones de segundo orden (SOS):")          # [1 0 0 ; 1 2.65312524e+03 1.26039498e+07]]
print(sos)


## Diagrama de Bode de cada bicuadrática:
plt.figure()
for i in range(len(sos)):
    w, mag, _ = signal.bode((sos[i, :3], sos[i, 3:]))
    plt.semilogx(w/(2*np.pi), mag, label=f'Etapa {i+1}')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Respuesta individual de cada biquad')
plt.grid(True)
plt.legend()
plt.show()


## Respuesta en Frecuencia:
w, mag, phase = signal.bode((num, den))

# Gráfico de Magnitud
plt.figure()
plt.semilogx(w / (2*np.pi), mag)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.title('Diagrama de Bode - Módulo')
plt.grid(True)

# Gráfico de Fase
plt.figure()
plt.semilogx(w / (2*np.pi), phase)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [°]')
plt.title('Diagrama de Bode - Fase')
plt.grid(True)
plt.show()