import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del sistema
k = 0.1  # Constante de velocidad de la reacción (1/min)
A0 = 1.0  # Concentración inicial de A (mol/L)


# Ecuación diferencial para la concentración de A
def modelo(A, t):
    dA_dt = -k * A
    return dA_dt


# Tiempo de simulación (0 a 50 minutos, con 1000 puntos)
tiempo = np.linspace(0, 50, 1000)  # Tiempo en minutos

# Resolver la ecuación diferencial
solucion = odeint(modelo, A0, tiempo)

# Graficar los resultados
plt.figure(figsize=(10, 5))
plt.plot(tiempo, solucion, label='Concentración de [A]')
plt.xlabel('Tiempo (minutos)')
plt.ylabel('Concentración (mol/L)')
plt.title('Descomposición de un Reactivo de Primer Orden')
plt.grid(True)
plt.legend()
plt.show()
