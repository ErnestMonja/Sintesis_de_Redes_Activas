import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# VFA (LM324)
Ad0 = 1e5
fp1 = 10
fp2 = 5e6

# Resistencias del circuito
Ri = 10e3
Rf = 90e3

wp1 = 2*np.pi*fp1
wp2 = 2*np.pi*fp2

s = ctl.TransferFunction.s

# Ganancia a lazo abierto del VFA
Av = Ad0/((1 + s/(wp1))*(1 + s/(wp2)))

# Ganancia de lazo del sistema compuesto
T1 = - (Av**2)*(Ri/(Ri + Rf))

w_search = np.logspace(1, 8, 2000)   # Analizamos de 1e4 a 1e8 rad/s
k_vec =  np.logspace(-4, 7, 100)      # Barre el parámetro k=R2/R1 de muy chico a muy grande

mf_vec = [] # Guarda resultados

def calc_mf(k): # Calcula el MF para cierto k
    T2 = -Av * (1/(1 + k))
    T = T1 + T2

    mag, phase, wout = ctl.bode(T, w_search, plot=False)

    dB = 20*np.log10(mag) # Guarda el modulo en dB

    # Buscar cruce de 0 dB
    idx = np.where(dB <= 0)[0]

    idx = idx[0]  # primer cruce
    phi = phase[idx] * (180/np.pi)
    MF = 180 + phi

    return MF

for k in k_vec:
    mf_vec.append(calc_mf(k)) # Itera para todos los k

mf_vec = np.array(mf_vec)

plt.figure(figsize=(9,5))
plt.semilogx(k_vec, mf_vec, linewidth=2)
plt.axhline(60, color='gray', linestyle='--', alpha=0.4)
plt.grid(True, which='both')
plt.xlabel("k = R2/R1")
plt.ylabel("Margen de fase (°)")
plt.title("Margen de fase vs k (modelo exacto)")
plt.tight_layout()
plt.show()
