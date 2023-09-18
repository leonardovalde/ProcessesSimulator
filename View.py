import random
import time
import threading
from Processimulator import Simulator

# Variable de simulación
simulation = Simulator('time', 1, 5, 20, 4, 4, 3)

# Función para iniciar la simulación
def start_simulation():
    try:
        time = int(input("Tiempo de simulación: "))
        start_thread(time)
    except ValueError:
        print('Ingresa un número entero positivo.')

# Función para iniciar la simulación en un hilo separado
def start_thread(time):
    simulation = Simulator(time, 1, 5, 20, 4, 4, 3)
    simulation.start()

if __name__ == "__main__":
    print("Process Manager Project")

    # Iniciar la simulación
    num_procesos = 10  # Puedes ajustar la cantidad de procesos
    start_simulation()
