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

# Relación k = R2/R1
k = -1.345

# Ganancia a lazo abierto de VFA
Av = Ad0/((1 + s/(wp1))*(1 + s/(wp2)))

# Ganancia de lazo principal
T1 = - (Av**2)*(Ri/(Ri + Rf))

# Ganancia de lazo local
T2 = -Av * (1/(1 + k))

# Ganancia de lazo total
T = T1 + T2

# Ganancia a lazo cerrado de AO2
Avf2 = Av/(1 - T2)

# Ganancia a lazo cerrado total
Avf = Av*Avf2/(1 - T)

ctl.bode_plot(T, dB=True, Hz=False)
plt.title("T - Ganancia de Lazo")
plt.show()

ctl.bode_plot(Avf, dB=True, Hz=False)
plt.title("Avf - Ganancia global")
plt.show()

f1 = np.logspace(np.log10(1e4), np.log10(1e8), 1000)  # rad/s
mag1, phase1, w1 = ctl.bode(T, f1, plot=False)
dB1 = 20*np.log10(mag1)

# Busca el cruce de |T|= 0 dB y devuelve la info
idx1 = np.where(dB1 <= 1.001)[0]
if len(idx1) > 0:
    idx1 = idx1[0]
    wg = w1[idx1]
    phig = phase1[idx1] * (180/np.pi)
    MF = 180 + phig
else:
    wg = None
    phig = None
    MF = None

print("\n---- Resultado wg ----")
print("wg =", wg)
print("fase(wg) =", phig, "°")
print("MF =", MF, "°")

# Busca el cruce de Avf = (Avf(0) -3 dB) y devuelve la info
f2 = np.logspace(np.log10(1e4), np.log10(1e6), 1000)
mag2, phase2, w2 = ctl.bode(Avf/ctl.dcgain(Avf), f2, plot=False)

dB2 = 20*np.log10(mag2)
idx2 = np.where(dB2 <= -3)[0]
if len(idx2) > 0:
    idx2 = idx2[0]
    w_3dB = w2[idx2]
else:
    w_3dB = None

print("\n---- Resultado w_3dB ----")
print("w_3dB =", w_3dB)
