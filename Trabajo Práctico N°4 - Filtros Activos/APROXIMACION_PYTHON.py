import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# %% Parámetros de Entrada
fp = [800, 1250]                # Banda de paso [Hz]
fs = [200, 5000]                # Banda de rechazo [Hz]
Wp = 2 * np.pi * np.array(fp)   # Banda de paso [rad/s]
Ws = 2 * np.pi * np.array(fs)   # Banda de rechazo [rad/s]
Ap = 0.25                       # Atenuación máxima en banda de paso [dB]
As = 30                         # Atenuación mínima en banda de rechazo [dB]

# %% Cálculo del filtro
n, Wn = signal.cheb1ord(Wp, Ws, Ap, As, analog=True)
num, den = signal.cheby1(n, Ap, Wn, btype='band', analog=True, output='ba')

# Filtro completo
Filtro = signal.TransferFunction(num, den)

# Secciones SOS (SciPy da orden inverso a MATLAB)
sos = signal.tf2sos(num, den)

# Como en MATLAB, pero ajustado al orden de SciPy
# Sección "PasaBajo" (segunda en SciPy, factor 1/2) -> roja fina (plana en bajas freq)
PB_raw_num = (1/2) * sos[1, :3]
PB_raw_den = sos[1, 3:]

# Sección "PasaAlto" (primera en SciPy, factor 2*g) -> verde fina (plana en altas freq)
g = sos[0, 0]                     # Ganancia global en primera sección de SciPy
PA_raw_num = 2 * g * sos[0, :3]
PA_raw_den = sos[0, 3:]

# --- Normalización para coincidir visualmente con MATLAB ---
# "PasaBajo": normalizar por ganancia en altas frecuencias (coef s^2) -> hace que parezca plana en bajas (relativo)
gain_high_pb = PB_raw_num[0] / PB_raw_den[0]
norm_pb = 1 / gain_high_pb
PB_num = PB_raw_num * norm_pb
PB_den = PB_raw_den

# "PasaAlto": normalizar por ganancia en altas frecuencias
gain_high_pa = PA_raw_num[0] / PA_raw_den[0]
norm_pa = 1 / gain_high_pa
PA_num = PA_raw_num * norm_pa
PA_den = PA_raw_den

# Funciones de Transferencia
PasaBajo = signal.TransferFunction(PB_num, PB_den)
PasaAlto = signal.TransferFunction(PA_num, PA_den)

# %% Gráficos
fig, ax = plt.subplots(figsize=(11, 7))

w = np.logspace(1, 5.5, 3000)
freq_hz = w / (2 * np.pi)

# Filtro completo (azul)
_, mag_total, _ = signal.bode(Filtro, w=w)
ax.semilogx(freq_hz, mag_total, color='blue', linewidth=2.5, label='Filtro pasa-banda')

# Sección PasaBajo (roja fina - plana en bajas frecuencias)
_, mag_pb, _ = signal.bode(PasaBajo, w=w)
ax.semilogx(freq_hz, mag_pb, color='red', linewidth=1.5, label='Sección PasaBajo')

# Sección PasaAlto (verde fina - plana en altas frecuencias)
_, mag_pa, _ = signal.bode(PasaAlto, w=w)
ax.semilogx(freq_hz, mag_pa, color='green', linewidth=1.5, label='Sección PasaAlto')

# Especificaciones
ax.plot([fs[0]/10, fs[0], fs[0]], [-As, -As, -Ap], color='r', linewidth=3)
ax.plot([fs[1], fs[1], fs[1]*10], [-Ap, -As, -As], color='r', linewidth=3)
ax.plot([fp[0], fp[0], fp[1], fp[1]], [-As, -Ap, -Ap, -As], color='g', linewidth=3)

ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')
ax.set_title('Respuesta en frecuencia del filtro Chebyshev Tipo I pasa-banda')
ax.grid(True, which='both', ls='-', alpha=0.5)
ax.legend()
ax.set_xlim([10, 1e5])
ax.set_ylim([-100, 20])

plt.tight_layout()
plt.show()