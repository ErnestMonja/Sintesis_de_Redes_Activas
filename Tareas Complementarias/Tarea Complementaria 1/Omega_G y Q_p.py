import matplotlib
matplotlib.use("Qt5Agg")

import numpy as np
import matplotlib.pyplot as plt

# Defino a Omega_G como función de Q_p
def Omega_G(Qp):
    termino = (- 1/Qp**2 + np.sqrt((1/Qp**2)**2 + 4)) / 2
    return np.sqrt(termino)

# Defino el dominio que quiero graficar
Qp = np.linspace(0.2, 5, 1000)
Omega_vals = Omega_G(Qp)

# Defino y calculo los dos puntos de interes para Q_p
Qp1 = 1 / np.sqrt(2)
Qp2 = 1 / np.sqrt(3)

Omega1 = Omega_G(Qp1)
Omega2 = Omega_G(Qp2)

print("Valor de Omega_G para Q_p = 1/sqrt(2):", Omega1)
print("Valor de Omega_G para Q_p = 1/sqrt(3):", Omega2)

# Grafico
plt.figure(figsize=(8,5))
plt.plot(Qp, Omega_vals, label="Omega_G(Q_p)")

# Marco puntos
plt.scatter([Qp1, Qp2], [Omega1, Omega2], color='red')
plt.text(Qp1, Omega1, f"  ({Qp1:.3f}, {Omega1:.3f})", color='red')
plt.text(Qp2, Omega2, f"  ({Qp2:.3f}, {Omega2:.3f})", color='red')

plt.xlabel("Q_p")
plt.ylabel("Omega_G")
plt.title("Omega_G(Q_p) con puntos de interés")
plt.grid(True)
plt.legend()
plt.show()