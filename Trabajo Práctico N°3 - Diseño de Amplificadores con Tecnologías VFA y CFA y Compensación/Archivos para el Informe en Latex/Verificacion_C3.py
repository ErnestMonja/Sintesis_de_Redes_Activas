import numpy as np
import control as ctl
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

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
R2 = 3925.46
R1 = 95.9
Rf = 90e3
Ri = 10e3

s = ctl.TransferFunction.s

wp1 = 2*np.pi*fp1
wp2 = 2*np.pi*fp2
wp3 = 2*np.pi*fp3
wp4 = 2*np.pi*fp4

# Parámetros de la red
Cx = 10e-12        
Rx = 3145.355          
Ry = 3145.355          

# Función de transferencia de la red
Ac = (Ry/(Ry + Rx)) * ((1 + s*Cx*Rx)/(1 + s*Cx*(Rx*Ry/(Rx + Ry))))
Ac = ctl.minreal(Ac, verbose=False)

# CFA
Avfi2 = 1 + R2/R1
ZT = RT/((1 + s/(wp1))*(1 + s/wp2))
T2 = -ZT/R2
Avf2 = Avfi2/(1 - 1/T2)

# Ganancia a lazo abierto total
Av = Ad0 / ((1 + s/wp3)*(1 + s/wp4)) * Avf2 * Ac

# Ganancia de lazo
T = - Av / (1 + Rf/Ri)
T = ctl.minreal(T, verbose=False)

# Ganancia a lazo cerrado
Avf = Av / (1 - T)
Avf = ctl.minreal(Avf, verbose=False)

# Bodes
plt.figure()
ctl.bode_plot(T, dB=True)
plt.suptitle("T(s) – Ganancia de lazo")
plt.show()

plt.figure()
ctl.bode_plot(Avf, dB=True)
plt.suptitle("Avf(s) – Ganancia a lazo cerrado")
plt.show()

# Margen de fase
gm, pm, wg, wp = ctl.margin(T)  
print(f"Margen de fase analítico = {180 + pm:.2f}°")

# Respuesta al escalón
t = np.linspace(0, 2e-6, 5000) 
t, y = ctl.step_response(Avf, T=t)

# Valor final
y_final = y[-1]

# Sobrepico
Mp = (np.max(y) - y_final) / y_final

# Estimar zeta desde Mp
def eq_zeta(z):
    return np.exp(-np.pi*z/np.sqrt(1-z**2)) - Mp

zeta = fsolve(eq_zeta, 0.7)[0]

# Estimar margen de fase
PM_rad = np.arctan(
    (2*zeta) /
    np.sqrt(np.sqrt(1 + 4*zeta**4) - 2*zeta**2)
)

PM_deg = np.degrees(PM_rad)

# Resultados
print("=== Estimación desde respuesta al escalón ===")
print(f"Nivel máximo = {np.max(y)}")
print(f"Sobrepico Mp = {Mp*100:.2f} %")
print(f"Factor de amortiguamiento ζ = {zeta:.3f}")
print(f"Margen de fase estimado ≈ {PM_deg:.2f}°")

plt.figure()
plt.plot(t, y)
plt.grid(True)
plt.xlabel("Tiempo [s]")
plt.ylabel("Salida")
plt.title("Respuesta al escalón del amplificador compuesto")
plt.show()

