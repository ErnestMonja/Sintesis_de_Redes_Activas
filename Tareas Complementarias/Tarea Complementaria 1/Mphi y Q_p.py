import matplotlib
matplotlib.use("Qt5Agg")

import numpy as np
import matplotlib.pyplot as plt

# Defino ahora a M-phi como función de y Q_p
def M_phi(Qp):
    # Parte interna de la raíz
    termino = (-1/Qp**2 + np.sqrt((1/Qp**2)**2 + 4)) / 2
    dentro = Qp * np.sqrt(termino)

    # M_phi en grados
    return 90 - np.degrees(np.arctan(dentro))

# Defino el dominio que quiero graficar
Qp = np.linspace(0.2, 5, 1000)
M_vals = M_phi(Qp)

# Defino y calculo los dos puntos de interes para Q_p
Qp1 = 1 / np.sqrt(2)
Qp2 = 1 / np.sqrt(3)

M1 = M_phi(Qp1)
M2 = M_phi(Qp2)

print("Valor de M_phi para Q_p = 1/sqrt(2):", M1, "grados")
print("Valor de M_phi para Q_p = 1/sqrt(3):", M2, "grados")

# Grafico
plt.figure(figsize=(8,5))
plt.plot(Qp, M_vals, label="M_phi(Q_p)")

# Marco puntos
plt.scatter([Qp1, Qp2], [M1, M2], color='red')
plt.text(Qp1, M1, f"  ({Qp1:.3f}, {M1:.2f}°)", color='red')
plt.text(Qp2, M2, f"  ({Qp2:.3f}, {M2:.2f}°)", color='red')

plt.xlabel("Q_p")
plt.ylabel("M_phi (grados)")
plt.title("Margen de Fase M_phi(Q_p) con puntos de interés")
plt.grid(True)
plt.legend()
plt.show()