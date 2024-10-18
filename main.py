import tkinter as tk
from tkinter import ttk, messagebox
import random


class Simulador:
    def __init__(self):
        random.seed(42)  # Semilla para reproducibilidad

    def simulacion_peluqueria(self, num_clientes, tiempo_corte_min, tiempo_corte_max, tiempo_llegadas, num_peluqueros):
        # Código de la simulación de la peluquería
        pass

    def simulacion_restaurante(self, num_counters):
        # Código de la simulación del restaurante
        pass

    def simulacion_restaurante2(self, num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes):
        # Código de la simulación del restaurante 2
        pass

    def simulacion_sistema_redes(self, capacidad_servidor, capacidad_cola, tiempo_procesamiento_min, tiempo_procesamiento_max, tiempo_llegadas, total_paquetes):
        # Código de la simulación del sistema de redes
        pass

    def simulacion_reaccion_quimica(self, k, A0, tiempo_simulacion):
        # Código de la simulación de la reacción química
        pass

    def simulacion_reactor_nuclear(self, Q_gen, k, T_cool, C, T0, tiempo_simulacion):
        # Código de la simulación del reactor nuclear
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Simulaciones")
        self.geometry("600x400")
        self.simulador = Simulador()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Seleccione una simulación:")
        self.label.pack(pady=10)

        self.simulation_buttons = [
            ("Peluquería", self.simulacion_peluqueria),
            ("Restaurante", self.simulacion_restaurante),
            ("Restaurante 2", self.simulacion_restaurante2),
            ("Sistema Redes", self.simulacion_sistema_redes),
            ("Reacción Química", self.simulacion_reaccion_quimica),
            ("Reactor Nuclear", self.simulacion_reactor_nuclear)
        ]

        for text, command in self.simulation_buttons:
            button = tk.Button(self, text=text, command=command)
            button.pack(pady=5)

        self.result_text = tk.Text(self, height=10, width=70)
        self.result_text.pack(pady=10)

    def simulacion_peluqueria(self):
        self.clear_text()
        self.show_inputs(["Número de clientes", "Tiempo mínimo de corte", "Tiempo máximo de corte", "Tiempo promedio entre llegadas", "Número de peluqueros"], self.run_simulacion_peluqueria)

    def run_simulacion_peluqueria(self, inputs):
        num_clientes, tiempo_corte_min, tiempo_corte_max, tiempo_llegadas, num_peluqueros = map(int, inputs)
        self.simulador.simulacion_peluqueria(num_clientes, tiempo_corte_min, tiempo_corte_max, tiempo_llegadas, num_peluqueros)
        self.result_text.insert(tk.END, "Simulación de Peluquería completada.\n")

    def simulacion_restaurante(self):
        self.clear_text()
        self.show_inputs(["Número de counters"], self.run_simulacion_restaurante)

    def run_simulacion_restaurante(self, inputs):
        num_counters = int(inputs[0])
        self.simulador.simulacion_restaurante(num_counters)
        self.result_text.insert(tk.END, "Simulación de Restaurante completada.\n")

    def simulacion_restaurante2(self):
        self.clear_text()
        self.show_inputs(["Número de mesas", "Tiempo mínimo de comer", "Tiempo máximo de comer", "Tiempo promedio entre llegadas", "Total de clientes"], self.run_simulacion_restaurante2)

    def run_simulacion_restaurante2(self, inputs):
        num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes = map(int, inputs)
        self.simulador.simulacion_restaurante2(num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes)
        self.result_text.insert(tk.END, "Simulación de Restaurante 2 completada.\n")

    def simulacion_sistema_redes(self):
        self.clear_text()
        self.show_inputs(["Capacidad del servidor", "Capacidad de la cola", "Tiempo mínimo de procesamiento", "Tiempo máximo de procesamiento", "Tiempo promedio entre llegadas", "Total de paquetes"], self.run_simulacion_sistema_redes)

    def run_simulacion_sistema_redes(self, inputs):
        capacidad_servidor, capacidad_cola, tiempo_procesamiento_min, tiempo_procesamiento_max, tiempo_llegadas, total_paquetes = map(int, inputs)
        self.simulador.simulacion_sistema_redes(capacidad_servidor, capacidad_cola, tiempo_procesamiento_min, tiempo_procesamiento_max, tiempo_llegadas, total_paquetes)
        self.result_text.insert(tk.END, "Simulación de Sistema de Redes completada.\n")

    def simulacion_reaccion_quimica(self):
        self.clear_text()
        self.show_inputs(["Constante de velocidad de la reacción", "Concentración inicial de A", "Tiempo de simulación"], self.run_simulacion_reaccion_quimica)

    def run_simulacion_reaccion_quimica(self, inputs):
        k, A0, tiempo_simulacion = map(float, inputs)
        self.simulador.simulacion_reaccion_quimica(k, A0, tiempo_simulacion)
        self.result_text.insert(tk.END, "Simulación de Reacción Química completada.\n")

    def simulacion_reactor_nuclear(self):
        self.clear_text()
        self.show_inputs(["Tasa de generación de calor", "Coeficiente de enfriamiento", "Temperatura del sistema de enfriamiento", "Capacidad térmica del reactor", "Temperatura inicial del reactor", "Tiempo de simulación"], self.run_simulacion_reactor_nuclear)

    def run_simulacion_reactor_nuclear(self, inputs):
        Q_gen, k, T_cool, C, T0, tiempo_simulacion = map(float, inputs)
        self.simulador.simulacion_reactor_nuclear(Q_gen, k, T_cool, C, T0, tiempo_simulacion)
        self.result_text.insert(tk.END, "Simulación de Reactor Nuclear completada.\n")

    def show_inputs(self, labels, command):
        self.input_window = tk.Toplevel(self)
        self.input_window.title("Ingrese los datos")
        self.entries = []

        for label in labels:
            frame = tk.Frame(self.input_window)
            frame.pack(pady=5)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT)
            self.entries.append(entry)

        tk.Button(self.input_window, text="Ejecutar", command=lambda: self.get_inputs(command)).pack(pady=10)

    def get_inputs(self, command):
        inputs = [entry.get() for entry in self.entries]
        self.input_window.destroy()
        command(inputs)

    def clear_text(self):
        self.result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()