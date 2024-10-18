


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del sistema
Q_gen = 5000  # Tasa de generación de calor en vatios (W)
k = 0.1  # Coeficiente de enfriamiento en W/°C
T_cool = 25  # Temperatura del sistema de enfriamiento en grados Celsius (°C)
C = 10000  # Capacidad térmica del reactor (J/°C)

# Ecuación diferencial para la variación de la temperatura
def modelo(T, t):
    dT_dt = (Q_gen / C) - k * (T - T_cool)
    return dT_dt

# Tiempo de simulación (0 a 200 minutos, con 1000 puntos)
tiempo = np.linspace(0, 200, 1000)  # Tiempo en minutos

# Temperatura inicial del reactor
T0 = 150  # °C

# Resolver la ecuación diferencial
solucion = odeint(modelo, T0, tiempo)

# Graficar los resultados
plt.figure(figsize=(10, 5))
plt.plot(tiempo, solucion, label='Temperatura del Reactor')
plt.xlabel('Tiempo (minutos)')
plt.ylabel('Temperatura (°C)')
plt.title('Enfriamiento del Reactor Nuclear')
plt.axhline(T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
plt.grid(True)
plt.legend()
plt.show()
