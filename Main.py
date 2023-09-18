import random
import time
import threading
from Processimulator import Simulator

# Variable de simulación
simulation = Simulator('time', 1, 5, 20, 4, 4, 3)

def print_simulator_settings(simulator):
    print("Configuración de la simulación:")
    print("-----------------------------------")
    print(f"-> Duración de la simulación: {simulator.simulation_time} ciclos de reloj")
    print(f"-> Retardo entre ciclos de reloj: {simulator.delay} segundos")
    print(f"-> Tiempo máximo para el próximo proceso: {simulator.max_next_process_time} ciclos de reloj")
    print(f"-> Tiempo máximo de vida del proceso: {simulator.max_process_life_time} ciclos de reloj")
    print(f"-> Tiempo máximo para la próxima operación de E/S: {simulator.max_next_IO_time} ciclos de reloj")
    print(f"-> Tiempo máximo de ejecución de E/S: {simulator.max_IO_execution_time} ciclos de reloj")
    print(f"-> Cantidad de ciclos de reloj por quantum: {simulator.quantum}")
    print("\n")
    time.sleep(3)

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
    print_simulator_settings(simulation)
    simulation.start()

if __name__ == "__main__":
    print("Process Manager Project")

    # Iniciar la simulación
    num_procesos = 10  # Puedes ajustar la cantidad de procesos
    start_simulation()
