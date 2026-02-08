import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# Parámetros de la red
Cx = 10e-12        
Rx = 3145          
Ry = 3145          

s = ctl.TransferFunction.s

# Función de transferencia
Ac = (Ry/(Ry + Rx)) * ((1 + s*Cx*Rx)/(1 + s*Cx*(Rx*Ry/(Rx + Ry))))

Ac = ctl.minreal(Ac, verbose=False)

print("Función de transferencia Ac(s):")
print(Ac)

# Polos y ceros
ceros_Ac = ctl.zeros(Ac)
polos_Ac = ctl.poles(Ac)

print("\nCeros:")
for c in ceros_Ac:
    freq = abs(c)/(2*np.pi)
    print(f"{freq} Hz")


print("Polos:")
for p in polos_Ac:
    freq = abs(p)/(2*np.pi)
    print(f"{freq} Hz")

# Ganancia Estática
K_Ac = ctl.dcgain(Ac)
print("K =", K_Ac, "veces")

# Bode
w = np.logspace(6, 10, 1000)
plt.figure()
ctl.bode_plot(Ac, w, dB=True)
plt.suptitle("Red cero–polo pasiva")
plt.show()