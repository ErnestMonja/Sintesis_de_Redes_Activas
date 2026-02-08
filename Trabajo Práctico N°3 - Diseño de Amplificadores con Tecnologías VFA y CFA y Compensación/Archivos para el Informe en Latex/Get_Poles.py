import numpy as np
import control as ctl

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
Av = Ad0 / ((1 + s/wp1) * (1 + s/wp2))
print("\nAv(s) =", Av)

# Verificación de Polos y Ganancia Estática a lazo abierto
polos_Av = ctl.poles(Av)
f1_calc = polos_Av[0] / (2*np.pi)
f2_calc = polos_Av[1] / (2*np.pi)
K_Av = Av(0)

print("\nPolos de Av:")
print("\nf1 =", f1_calc, "Hz")
print("\nf2 =", f2_calc, "Hz")

print("\nGanancia estática de Av:")
print("\nK =", K_Av)

# Ganancia de Lazo
T = -Av * (Ri / (Rf + Ri))
print("\nT(s) =", T)

# Ganancia a Lazo Cerrado
Avf = ctl.minreal(Av / (1 - T), verbose=False)
print("\nAvf(s) =", Avf)

# Obtención de Polos y Ganancia Estática a lazo cerrado
polos_Avf = ctl.poles(Avf)
f3 = polos_Avf[0] / (2*np.pi)
f4 = polos_Avf[1] / (2*np.pi)
K_Avf = Avf(0)

print("\nPolos de Avf:")
print("\nf3 =", f3, "Hz")
print("\nf4 =", f4, "Hz")

print("\nGanancia estática de Avf:")
print("\nK =", K_Avf)