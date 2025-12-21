import numpy as np
from scipy import signal


## Ancho de Banda a Rechazar:
f1 = 1000                                       # Frecuencia Inferior: 1000 [Hz]
f2 = 2000                                       # Frecuencia Superior: 2000 [Hz]
Wbw = [2*np.pi*f1, 2*np.pi*f2]

## Aproximación de un filtro rechaza banda, analógico y de segundo orden, con un 
## ripple en la banda de rechazo de 1 [dB] que sigue las frecuencias listadas 
## anteriormente.
num, den = signal.cheby1(N = 2,                 # Filtro de 2do Orden
                        rp = 1,                 # Ripple de 1 [dB]
                        Wn = Wbw,               # Frecuencias a Rechazar
                        btype = 'bandstop',     # Filtro rechaza banda
                        analog = True,          # Filtro analógico
                        output = 'ba')          # Salida del tipo: F(s) = num/den

## Impresión de los parámetros obtenidos:
print("Numerador:", num)
print("Denominador:", den)

## Descomposición en ceros, polos y constante
z, p, k = signal.tf2zpk(num, den)
print("Ceros: ", z)
print("Polos: ", p)
print("Constante: ", k)

## Descomposición en bicuadraticas mediante sos
sos = signal.tf2sos(num,den)
print("Coeficientes del SOS:", sos)
