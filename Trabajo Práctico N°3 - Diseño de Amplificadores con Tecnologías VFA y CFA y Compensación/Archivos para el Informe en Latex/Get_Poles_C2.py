import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# VFA (LM324)
Ad0 = 1e5
fp3 = 10
fp4 = 5.06e6

# CFA (LM6181)
fp1 = 14e3
fp2 = 82.3e6
RT = 2.37e6
CT = 4.8e-12

# Resistencias del circuito
R2 = 850
R1 = 41.4   
Rf = 90e3
Ri = 10e3

s = ctl.TransferFunction.s

wp1 = 2*np.pi*fp1
wp2 = 2*np.pi*fp2
wp3 = 2*np.pi*fp3
wp4 = 2*np.pi*fp4

# CFA
Avfi2 = 1 + R2/R1
ZT = RT/((1 + s/(wp1))*(1 + s/wp2))
T2 = -ZT/R2
Avf2 = Avfi2/(1 - 1/T2)

# Ganancia a lazo abierto total
Av = Ad0 / ((1 + s/wp3)*(1 + s/wp4)) * Avf2

# Ganancia de lazo
T = - Av / (1 + Rf/Ri)

# Ganancia a lazo cerrado
Avf = Av / (1 - T)
Avf = ctl.minreal(Avf, verbose=False)

polos_Avf = ctl.poles(Avf)

for p in polos_Avf:
    freq = abs(p)/(2*np.pi)
    print(f"{freq} Hz")

K_Avf = ctl.dcgain(Avf)
print("K =", K_Avf, "veces")