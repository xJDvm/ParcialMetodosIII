import tkinter as tk
from tkinter import ttk, messagebox
import random
from re import escape
import simpy
import math
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os
import sys
import datetime


paquetes_perdidos = 0
tiempo_total_espera = 0
paquetes_procesados = 0
te = 0.0 #tiempo de espera total
dt = 0.0#duracion del servicio
fin = 0.0#minuto en que finaliza
class Simulador:
    def __init__(self):
        random.seed(42)  # Semilla para reproducibilidad

    def simulacion_peluqueria(self, tot_clientes, tiempo_corte_min, tiempo_corte_max, t_llegadas, num_peluqueros):
        semilla = 30
        #procedimientos
        def  cortar(cliente):
            global dt
            R = random.random()
            tiempo = tiempo_corte_max - tiempo_corte_min
            tiempo_corte = tiempo_corte_min + (tiempo*R) #dist Uniforme
            yield env.timeout(tiempo_corte) #dejar correr el tiempo n minutos
            print("Corte listo a %s en %.2f minutos" % (cliente, tiempo_corte))
            dt = dt + tiempo_corte #acumular tiempo de uso de la instalacion

        def cliente(env, name, personal):
            global te
            global fin
            llega = env.now # guarda el minuto de llegada del cliente 
            print("--> %s llegó a la peluqueria en el minuto %.2f" % (name, llega))
            with personal.request() as request: # espera turno
                yield request # obtener turno
                pasa = env.now
                espera = pasa - llega # acumulo tiempo de espera
                te = te + espera # acumulo tiempo de espera
                print("%s Pasa y espera en la peluqueria en el minuto %.2f habiendo esperado %.2f" % (name, pasa, espera))
                yield env.process(cortar(name)) # llamar al proceso cortar
                deja = env.now # momento en que el cliente deja la peluquería
                print("<--%s deja la peluqueria en minuto %.2f" % (name, deja))
                fin = deja # guardo el minuto en que termina


        def principal(env, personal):
            llegada = 0
            i = 0
            for i in range(tot_clientes):
                R = random.random()
                llegada = -t_llegadas* math.log(R)
                yield env.timeout(llegada) #dejo transcurrir un tiempo entre un cliente y otro
                i=i+1
                env.process(cliente(env, 'cliente %d' % i, personal))

        #programa principal
        print("---Simulacion Peluqueria---")
        random.seed(semilla)
        env = simpy.Environment() #creo el entorno de simulacion
        personal = simpy.Resource(env, num_peluqueros) #crea los recursos peluqueros
        env.process(principal(env, personal))
        env.run()

        #salidas
        print("Indicadores optenidos")
        print("")
        lpc = te/fin
        print("Longitud promedio de la cola: %.2f" % lpc)
        tep = te/tot_clientes
        print("Tiempo de espera promedio: %.2f" % tep)
        upi = (dt/fin)/num_peluqueros
        print("Uso promedio de la instalacion: %.2f" % upi)
        pass

    def simulacion_restaurante(self, num_counters):
        global STATE, TEMP, SUM_ALL
        STATE = 0
        TEMP = 0
        SUM_ALL = 0.00
        CALC = [0] * 500  # Input capacity
        RANDOM_SEED = 42  # Random helper

        # Simulation time in minutes
        HOUR_OPEN = 7  # Morning
        HOUR_CLOSE = 23  # Night
        START = HOUR_OPEN * 60
        SIM_TIME = HOUR_CLOSE * 60

        print(START)
        print(SIM_TIME)

        SIM_FACTOR = 1 / 60  # Simulation realtime factor
        PEAK_START = 11
        PEAK_END = 13
        PEAK_TIME = 60 * (PEAK_END - PEAK_START)  # Range of peak hours

        NUM_COUNTERS = 1  # Number of counters in the drive-thru
        # Minutes it takes in each counters
        TIME_COUNTER_A = 2
        TIME_COUNTER_B = 1
        TIME_COUNTER_C = 3

        # Create a customer every [min, max] minutes
        CUSTOMER_RANGE_NORM = [5, 10]  # in normal hours
        CUSTOMER_RANGE_PEAK = [1, 5]  # in peak hours
        """
        Define clear screen function
        """


        def clear():
            os.system(['clear', 'cls'][os.name == 'nt'])


        """
        Define exact clock format function
        """


        def toc(raw):
            clock = ('%02d:%02d' % (raw / 60, raw % 60))
            return clock


        """
        Waiting lane class
        """


        class waitingLane(object):

            def __init__(self, env):
                self.env = env
                self.lane = simpy.Resource(env, 3)

            def serve(self, cust):
                yield self.env.timeout(0)
                print("[w] (%s) %s entered the area" % (toc(env.now), cust))


        """
        First counter class
        """


        class counterFirst(object):

            def __init__(self, env):
                self.env = env
                self.employee = simpy.Resource(env, 1)

            def serve(self, cust):
                yield self.env.timeout(
                    random.randint(TIME_COUNTER_A - 1, TIME_COUNTER_A + 1))
                print("[?] (%s) %s ordered the menu" % (toc(env.now), cust))


        """
        Second counter class
        """


        class counterSecond(object):

            def __init__(self, env):
                self.env = env
                self.employee = simpy.Resource(env, 1)

            def serve(self, cust):
                yield self.env.timeout(
                    random.randint(TIME_COUNTER_B - 1, TIME_COUNTER_B + 1))
                print("[$] (%s) %s paid the order" % (toc(env.now), cust))


        """
        First+Second counter class
        """


        class counterFirstSecond(object):

            def __init__(self, env):
                self.env = env
                self.employee = simpy.Resource(env, 1)

            def serve(self, cust):
                yield self.env.timeout(
                    random.randint(TIME_COUNTER_A - 1, TIME_COUNTER_A + 1))
                print("[?] (%s) %s ordered the menu" % (toc(env.now), cust))

                yield self.env.timeout(
                    random.randint(TIME_COUNTER_B - 1, TIME_COUNTER_B + 1))
                print("[$] (%s) %s paid the order" % (toc(env.now), cust))


        """
        Third counter class
        """


        class counterThird(object):

            def __init__(self, env):
                self.env = env
                self.employee = simpy.Resource(env, 1)

            def serve(self, cust):
                yield self.env.timeout(
                    random.randint(TIME_COUNTER_C - 1, TIME_COUNTER_C + 1))
                print("[#] (%s) %s took the order" % (toc(env.now), cust))


        """
        The customer process (each customer has a name)
        arrives at the drive-thru lane, counter, then serviced by the empoyee (ce).
        It then starts the service process for each counters then leaves.
        """
        """
        (Type 2) Define customer behavior at first counter
        """


        def customer2A(env, name, wl, ce12, ce3):

            with wl.lane.request() as request:

                if (env.now >= SIM_TIME):
                    print("[!] Not enough time! %s cancelled" % name)
                    env.exit()

                yield request
                yield env.process(wl.serve(name))
                print("[w] (%s) %s is in waiting lane" % (toc(env.now), name))

            # Start the actual drive-thru process
            print("[v] (%s) %s is in drive-thru counter" % (toc(env.now), name))

            with ce12.employee.request() as request:

                if (env.now + TIME_COUNTER_A + TIME_COUNTER_B >= SIM_TIME):
                    print("[!] Not enough time! Assumed %s is quickly finished" % name)
                    yield env.timeout(0.5)
                    env.exit()

                yield request

                CALC[int(name[5:])] = env.now
                yield env.process(ce12.serve(name))
                print("[?] (%s) %s choose the order" % (toc(env.now), name))

                yield env.process(ce12.serve(name))
                print("[$] (%s) %s is paying and will take the order" %
                    (toc(env.now), name))
                env.process(customer2B(env, name, ce12, ce3))


        """
        (Type 2) Define customer behavior at second counter
        """


        def customer2B(env, name, ce12, ce3):

            with ce3.employee.request() as request:

                if (env.now + TIME_COUNTER_C >= SIM_TIME):
                    print("[!] Not enough time! Assumed %s is quickly finished" % name)
                    yield env.timeout(0.5)
                    env.exit()

                yield request

                yield env.process(ce3.serve(name))
                print("[^] (%s) %s leaves" % (toc(env.now), name))

                global TEMP
                TEMP = int(name[5:])
                CALC[int(name[5:])] = env.now - CALC[int(name[5:])]


        """
        (Type 3) Define customer behavior at first counter
        """


        def customer3A(env, name, wl, ce1, ce2, ce3):

            with wl.lane.request() as request:

                if (env.now >= SIM_TIME):
                    print("[!] Not enough time! %s cancelled" % name)
                    env.exit()

                yield request
                yield env.process(wl.serve(name))
                print("[w] (%s) %s is in waiting lane" % (toc(env.now), name))

            # Start the actual drive-thru process
            print("[v] (%s) %s is in drive-thru counter" % (toc(env.now), name))

            with ce1.employee.request() as request:

                if (env.now + TIME_COUNTER_A >= SIM_TIME):
                    print("[!] Not enough time! Assumed %s is quickly finished" % name)
                    yield env.timeout(0.5)

                yield request

                CALC[int(name[5:])] = env.now
                yield env.process(ce1.serve(name))
                print("[?] (%s) %s choose the order" % (toc(env.now), name))

                print("[2] (%s) %s will pay the order" % (toc(env.now), name))
                env.process(customer3B(env, name, ce1, ce2, ce3))


        """
        (Type 3) Define customer behavior at second counter
        """


        def customer3B(env, name, ce1, ce2, ce3):

            with ce2.employee.request() as request:

                if (env.now + TIME_COUNTER_B >= SIM_TIME):
                    print("[!] Not enough time! Assumed %s is quickly finished" % name)
                    yield env.timeout(0.5)
                    env.exit()

                yield request

                yield env.process(ce2.serve(name))
                print("[$] (%s) %s is paying the order" % (toc(env.now), name))

                print("[3] (%s) %s will take the order" % (toc(env.now), name))
                env.process(customer3C(env, name, ce1, ce2, ce3))


        """
        (Type 3) Define customer behavior at third counter
        """


        def customer3C(env, name, ce1, ce2, ce3):

            with ce3.employee.request() as request:

                if (env.now + TIME_COUNTER_C >= SIM_TIME):
                    print("[!] Not enough time! Assumed %s is quickly finished" % name)
                    yield env.timeout(0.5)
                    env.exit()

                yield request

                yield env.process(ce3.serve(name))
                print("[^] (%s) %s leaves" % (toc(env.now), name))

                global TEMP
                TEMP = int(name[5:])
                CALC[int(name[5:])] = env.now - CALC[int(name[5:])]


        """
        Define detail of 2 counters setup environment
        """


        def setup2(env, cr):
            # Create all counters
            wl = waitingLane(env)
            ce12 = counterFirstSecond(env)
            ce3 = counterThird(env)
            i = 0

            # Create more customers while the simulation is running
            while True:
                yield env.timeout(random.randint(*cr))
                i += 1
                env.process(customer2A(env, "Cust %d" % i, wl, ce12, ce3))


        """
        Define detail of 3 counters setup environment
        """


        def setup3(env, cr):
            # Create all counters
            wl = waitingLane(env)
            ce1 = counterFirst(env)
            ce2 = counterSecond(env)
            ce3 = counterThird(env)
            i = 0

            # Create more customers while the simulation is running
            while True:
                yield env.timeout(random.randint(*cr))
                i += 1
                env.process(customer3A(env, "Cust %d" % i, wl, ce1, ce2, ce3))


        """
        Run the main program, execute via editor or terminal.
        """
        if __name__ == "__main__":

            clear()
            print("""
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        >> Restaurant Queuing Model Simulation
        >> Drive-Thru Fast Food Restaurant Design Model Evaluation
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>""")

            # Check if the number of counters is specified
            if len(sys.argv) < 2:
                nc = 3
            else:
                nc = int(sys.argv[1])

            # random.seed(RANDOM_SEED) # Helps reproducing the results

            # Has the environment in realtime (wall clock)
            # env = simpy.RealtimeEnvironment(factor=SIM_FACTOR)

            # Has the environment in manual step through
            env = simpy.Environment(initial_time=START)
            print("Environment created at %d!" % env.now)

            # Decide the counter model setup
            if nc == 2:
                env.process(setup2(env, CUSTOMER_RANGE_NORM))
            elif nc == 3:
                env.process(setup3(env, CUSTOMER_RANGE_NORM))

            print("Setup initialized!")

            print("Start simulation!")
            env.run(until=SIM_TIME)

            for i in range(TEMP + 1):
                SUM_ALL += CALC[i]

            averageTimeService = SUM_ALL / (TEMP + 1)
            servicePerSecond = 1.00 / (averageTimeService * 60)
            servicePerMinute = servicePerSecond * 60

            print("The end!")
            print("[i] Model: %d counters" % nc)
            print("[i] Average time:       %.4f" % averageTimeService)
            print("[i] Service per minute: %f" % servicePerMinute)

        pass

    def simulacion_restaurante2(self, num_mesas, tiempo_comer_min, tiempo_comer_max, tiempo_llegadas, total_clientes):
        SEMILLA = 42  # Semilla para reproducibilidad
        NUM_MESAS = 5  # Número de mesas disponibles en el restaurante
        TIEMPO_COMER_MIN = 20  # Tiempo mínimo que un cliente pasa comiendo (minutos)
        TIEMPO_COMER_MAX = 40  # Tiempo máximo que un cliente pasa comiendo (minutos)
        TIEMPO_LLEGADAS = 10  # Tiempo promedio entre la llegada de clientes (minutos)
        TOTAL_CLIENTES = 10  # Total de clientes a simular


        # Función para simular el proceso de un cliente
        def cliente(env, nombre, restaurante):
            """Simula el proceso de un cliente que llega, espera una mesa, come y luego se va."""
            print(f'{nombre} llega al restaurante en el minuto {env.now:.2f}')

            # El cliente solicita una mesa en el restaurante (espera si no hay mesas disponibles)
            with restaurante.request() as mesa:
                yield mesa  # Espera a que una mesa esté disponible
                print(f'{nombre} toma una mesa en el minuto {env.now:.2f}')

                # Simula el tiempo que el cliente pasa comiendo
                tiempo_comer = random.randint(TIEMPO_COMER_MIN, TIEMPO_COMER_MAX)
                yield env.timeout(tiempo_comer)
                print(
                    f'{nombre} termina de comer y deja la mesa en el minuto {env.now:.2f}'
                )


        # Función para la llegada de clientes
        def llegada_clientes(env, restaurante):
            """Genera la llegada de clientes al restaurante."""
            for i in range(TOTAL_CLIENTES):
                # Cada cliente llega al restaurante
                yield env.timeout(
                    random.expovariate(1.0 / TIEMPO_LLEGADAS)
                )  # Distribución exponencial para el tiempo entre llegadas
                env.process(cliente(env, f'Cliente {i+1}', restaurante))


        # Configuración y ejecución de la simulación
        print('--- Simulación del Restaurante ---')
        random.seed(SEMILLA)  # Establece la semilla para reproducir resultados
        env = simpy.Environment()  # Crea el entorno de simulación
        restaurante = simpy.Resource(
            env, NUM_MESAS)  # Crea el recurso de mesas en el restaurante
        env.process(llegada_clientes(
            env, restaurante))  # Inicia el proceso de llegada de clientes
        env.run()  # Ejecuta la simulación
        print('--- Fin de la simulación ---')
        pass

    def simulacion_sistema_redes(self, capacidad_servidor, capacidad_cola, tiempo_procesamiento_min, tiempo_procesamiento_max, tiempo_llegadas, total_paquetes):
        # Parámetros de la simulación
        SEMILLA = 42  # Semilla para reproducibilidad
        CAPACIDAD_SERVIDOR = capacidad_servidor  # Capacidad del servidor (cuántos paquetes puede procesar simultáneamente)
        CAPACIDAD_COLA = capacidad_cola  # Capacidad de la cola de espera
        TIEMPO_PROCESAMIENTO_MIN = tiempo_procesamiento_min  # Tiempo mínimo de procesamiento de un paquete (segundos)
        TIEMPO_PROCESAMIENTO_MAX = tiempo_procesamiento_max  # Tiempo máximo de procesamiento de un paquete (segundos)
        TIEMPO_LLEGADAS = tiempo_llegadas  # Tiempo promedio entre la llegada de paquetes (segundos)
        TOTAL_PAQUETES = total_paquetes  # Número total de paquetes a simular

        # Variables para seguimiento de estadísticas
       


        # Función para simular el proceso de un paquete
        def paquete(env, nombre, servidor):
            global paquetes_perdidos, tiempo_total_espera, paquetes_procesados

            llegada = env.now  # Momento de llegada del paquete al sistema
            print(f'{nombre} llega al servidor en el segundo {llegada:.2f}')

            with servidor.request() as req:
                # Si el servidor y la cola están llenos, el paquete se pierde
                if len(servidor.queue) >= CAPACIDAD_COLA:
                    paquetes_perdidos += 1
                    print(
                        f'{nombre} se pierde debido a cola llena en el segundo {env.now:.2f}'
                    )
                    return

                # El paquete espera su turno en la cola si es necesario
                yield req
                espera = env.now - llegada
                tiempo_total_espera += espera
                print(
                    f'{nombre} comienza a ser procesado después de esperar {espera:.2f} segundos en el segundo {env.now:.2f}'
                )

                # Simula el tiempo de procesamiento del paquete
                tiempo_procesamiento = random.randint(TIEMPO_PROCESAMIENTO_MIN,
                                                    TIEMPO_PROCESAMIENTO_MAX)
                yield env.timeout(tiempo_procesamiento)
                print(f'{nombre} termina de ser procesado en el segundo {env.now:.2f}')
                paquetes_procesados += 1


        # Función para la llegada de paquetes
        def llegada_paquetes(env, servidor):
            """Genera la llegada de paquetes al servidor."""
            for i in range(TOTAL_PAQUETES):
                yield env.timeout(random.expovariate(
                    1.0 / TIEMPO_LLEGADAS))  # Tiempo entre llegadas de paquetes
                env.process(paquete(env, f'Paquete {i+1}', servidor))


        # Configuración y ejecución de la simulación
        print('--- Simulación de Red de Computadoras ---')
        random.seed(SEMILLA)  # Establece la semilla para reproducir resultados
        env = simpy.Environment()  # Crea el entorno de simulación
        servidor = simpy.Resource(
            env, CAPACIDAD_SERVIDOR)  # Crea el recurso del servidor con su capacidad
        env.process(llegada_paquetes(
            env, servidor))  # Inicia el proceso de llegada de paquetes
        env.run()  # Ejecuta la simulación
        print('--- Fin de la simulación ---')

        # Salidas de la simulación
        print("\nResultados de la simulación:")
        print(f'Total de paquetes simulados: {TOTAL_PAQUETES}')
        print(f'Paquetes procesados: {paquetes_procesados}')
        print(f'Paquetes perdidos: {paquetes_perdidos}')
        print(
            f'Tasa de pérdida de paquetes: {100 * paquetes_perdidos / TOTAL_PAQUETES:.2f}%'
        )
        print(
            f'Tiempo promedio de espera de los paquetes: {tiempo_total_espera / paquetes_procesados if paquetes_procesados > 0 else 0:.2f} segundos'
        )
        print(
            f'Utilización del servidor: {100 * (paquetes_procesados * (TIEMPO_PROCESAMIENTO_MIN + TIEMPO_PROCESAMIENTO_MAX) / 2) / env.now:.2f}%'
        )
        pass

    def simulacion_reaccion_quimica(self, k, A0, tiempo_simulacion):
        k = 0.1  # Constante de velocidad de la reacción (1/min)
        A0 = 1.0  # Concentración inicial de A (mol/L)


# Ecuación diferencial para la concentración de A
        def modelo(A, t):
            dA_dt = -k * A
            return dA_dt


        # Tiempo de simulación (0 a 50 minutos, con 1000 puntos)
        tiempo_simulacion = np.linspace(0, 50, 1000)  # Tiempo en minutos

        # Resolver la ecuación diferencial
        solucion = odeint(modelo, A0, tiempo_simulacion)

        # Graficar los resultados
        plt.figure(figsize=(10, 5))
        plt.plot(tiempo_simulacion, solucion, label='Concentración de [A]')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Concentración (mol/L)')
        plt.title('Descomposición de un Reactivo de Primer Orden')
        plt.grid(True)
        plt.legend()
        plt.show()

        pass

    def simulacion_reactor_nuclear(self, Q_gen, k, T_cool, C, T0, tiempo_simulacion):
        # Ecuación diferencial para la variación de la temperatura
        def modelo(T, t):
            dT_dt = (Q_gen / C) - k * (T - T_cool)
            return dT_dt

        # Tiempo de simulación (0 a 200 minutos, con 1000 puntos)
        tiempo_simulacion = np.linspace(0, 200, 1000)  # Tiempo en minutos

        # Temperatura inicial del reactor
        T0 = 150  # °C

        # Resolver la ecuación diferencial
        solucion = odeint(modelo, T0, tiempo_simulacion)

        # Graficar los resultados
        plt.figure(figsize=(10, 5))
        plt.plot(tiempo_simulacion, solucion, label='Temperatura del Reactor')
        plt.xlabel('Tiempo (minutos)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Enfriamiento del Reactor Nuclear')
        plt.axhline(T_cool, color='red', linestyle='--', label='Temperatura del Sistema de Enfriamiento')
        plt.grid(True)
        plt.legend()
        plt.show()
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