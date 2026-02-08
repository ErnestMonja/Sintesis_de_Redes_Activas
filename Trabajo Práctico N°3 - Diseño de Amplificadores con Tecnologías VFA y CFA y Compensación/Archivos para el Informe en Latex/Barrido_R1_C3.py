import numpy as np
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
          
R2  = 3925.46           
Rf_Ri = 9                  

wp1 = 2*np.pi*fp1
wp2 = 2*np.pi*fp2
wp3 = 2*np.pi*fp3
wp4 = 2*np.pi*fp4

# Parámetros de la red
Cx = 10e-12        
Rx = 3145.355          
Ry = 3145.355          

# Frecuencia de barrido
f = np.logspace(3, 8, 12000)   # 1 kHz a 100 MHz
w = 2*np.pi*f

# Barrido de R1
R1_valores = np.linspace(10, 100, 1000)
fG_valores = []

target_fG = 2e6

best_R1 = None
best_fG = None
best_error = 1e12 # Guardan los mejores valores en cada iteración (arranca grande para poder minimizarlo)

for R1 in R1_valores: # En cada iteración se recalcula todo

    Avfi2 = 1 + R2/R1

    T = (Ad0 /
         ((1 + 1j*w/wp3)*(1 + 1j*w/wp4)) *
         (Avfi2 / (1 + 1j*w*CT*R2)) *
         (1 / (1 + Rf_Ri)) * (Ry/(Ry + Rx)) * ((1 + 1j*w*Cx*Rx)/(1 + 1j*w*Cx*(Rx*Ry/(Rx + Ry)))))

    magT = np.abs(T) # Calcula el módulo de T(s)

    idx = np.argmin(np.abs(magT - 1)) # Busca donde |T(s)| = 1 y guarda el índice
    fG = f[idx] # Busca el índice para esa frecuencia

    fG_valores.append(fG) # La guarda para el gráfico

    error = abs(fG - target_fG) # Ve qué tan lejos está de 2 MHz, si está más cerca que la iteración anterior, actualiza los mejores valores
    if error < best_error:
        best_error = error
        best_R1 = R1
        best_fG = fG

fG_valores = np.array(fG_valores) # Convierte a array para el plot

# Resultados numéricos
print(f"R1 óptimo ≈ {best_R1:.2f} ohm")
print(f"fG obtenido ≈ {best_fG/1e6:.3f} MHz")

# Gráfico fG vs R1
plt.figure()
plt.plot(R1_valores, fG_valores/1e6, label=r'$f_G(R_1)$')
plt.axhline(2, linestyle='--', label='fG = 2 MHz')
plt.axvline(best_R1, linestyle=':', label=f'R1 ≈ {best_R1:.1f} Ω')
plt.grid(True)
plt.xlabel('R1 [Ω]')
plt.ylabel('fG [MHz]')
plt.title('Frecuencia de punto crítico vs R1')
plt.legend()
plt.tight_layout()
plt.show()
