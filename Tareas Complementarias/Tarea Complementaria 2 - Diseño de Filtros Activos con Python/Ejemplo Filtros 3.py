import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

## Ancho de Banda a Aceptar:
f1 = 1000                                       # Frecuencia Inferior: 1000 [Hz]
f2 = 2000                                       # Frecuencia Superior: 2000 [Hz]
Wbw = [2*np.pi*f1, 2*np.pi*f2]

## Aproximación de un filtro pasa banda, analógico y de segundo orden que sigue 
## las frecuencias listadas anteriormente.
num, den = signal.butter(N = 2,                 # Filtro de 2do Orden
                        Wn = Wbw,               # Frecuencias a Rechazar
                        btype = 'bandpass',     # Filtro pasa banda
                        analog = True,          # Filtro analógico
                        output = 'ba')          # Salida del tipo: F(s) = num/den


## Impresión de los parámetros obtenidos:
print("Numerador:", num)
print("Denominador:", den)

## Descomposición en ceros, polos y constante
z, p, k = signal.tf2zpk(num, den)
print("Ceros: ", z)                             # [0 ; 0]
print("Polos: ", p)                             # [-2775.72 +- j11124.47 ;
                                                #  -1667.15 +- j6681.59]
print("Constante: ", k)                         # [39478417.60]

## Descomposición en bicuadraticas mediante sos
sos = signal.tf2sos(num,den)                    # [[3.94784176e+07 0 0 ;
                                                # 1 5.55144899e+03 1.31458664e+08]
print("Coeficientes del SOS:", sos)             # [1 0 0 ;
                                                # 1 3.33431689e+03 4.74231339e+07]]

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
