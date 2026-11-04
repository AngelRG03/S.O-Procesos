# Monitoreo de procesos del sistema operativo
# Muestra los procesos activos (PID, nombre, CPU y memoria) usando psutil
# y simula un cambio de contexto con algunos de ellos.

import random
import time
from collections import deque

import psutil


def obtener_procesos():
    """Regresa la lista de procesos activos ordenada por uso de CPU."""
    procesos = list(psutil.process_iter(['pid', 'name']))

    # psutil necesita dos mediciones para calcular el % de CPU:
    # hacemos la primera, esperamos un segundo y luego la segunda.
    for p in procesos:
        try:
            p.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    time.sleep(1)

    nucleos = psutil.cpu_count()
    lista = []
    for p in procesos:
        if p.pid == 0:  # "System Idle Process" en Windows, no es un proceso real
            continue
        try:
            lista.append({
                'pid': p.pid,
                'nombre': p.info['name'] or 'desconocido',
                'cpu': p.cpu_percent() / nucleos,  # igual que el Administrador de tareas
                'memoria': p.memory_info().rss / (1024 * 1024),  # en MB
                'estado': p.status(),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # el proceso ya terminó o no tenemos permiso para leerlo

    # Ordena por CPU y, si empatan, por memoria
    lista.sort(key=lambda p: (p['cpu'], p['memoria']), reverse=True)
    return lista


def mostrar_procesos(procesos, cantidad=15):
    print(f"\n{'PID':>7}  {'Proceso':<28} {'CPU %':>6} {'Memoria MB':>11}  Estado SO")
    print("-" * 70)
    for p in procesos[:cantidad]:
        print(f"{p['pid']:>7}  {p['nombre'][:28]:<28} {p['cpu']:>6.1f} "
              f"{p['memoria']:>11.1f}  {p['estado']}")


def elegir_procesos(procesos, cantidad=5):
    """Toma los procesos que más CPU usan, sin repetir nombre."""
    elegidos = []
    nombres = []
    for p in procesos:
        if p['nombre'] not in nombres:
            elegidos.append(p)
            nombres.append(p['nombre'])
        if len(elegidos) == cantidad:
            break
    return elegidos


def simular_cambio_de_contexto(procesos, turnos=8):
    """Simula un planificador Round Robin con una sola CPU.

    En cada turno un proceso usa la CPU y los demás esperan en la cola de listos.
    Cuando termina su turno, el proceso regresa a la cola o se bloquea si pide E/S.
    """
    cola_listos = deque(procesos)
    bloqueados = []
    en_cpu = None

    for turno in range(1, turnos + 1):
        print(f"\n--- Turno {turno} ---")

        # Los que estaban esperando E/S ya terminaron y vuelven a la cola
        cola_listos.extend(bloqueados)
        bloqueados = []

        # El proceso que estaba en la CPU sale: a veces pide E/S y se bloquea,
        # si no, se le acabó su tiempo (quantum) y regresa al final de la cola
        if en_cpu is not None:
            if random.random() < 0.3:
                bloqueados.append(en_cpu)
            else:
                cola_listos.append(en_cpu)

        # Entra a la CPU el primero de la cola
        anterior = en_cpu
        en_cpu = cola_listos.popleft()
        if anterior is not None and anterior != en_cpu:
            print(f"Cambio de contexto: se guarda {anterior['nombre']} "
                  f"y se carga {en_cpu['nombre']}")

        for p in procesos:
            if p == en_cpu:
                estado = "Ejecutándose"
            elif p in bloqueados:
                estado = "Bloqueado (esperando I/O)"
            else:
                estado = "Listo"
            print(f"PID: {p['pid']} | Proceso: {p['nombre']} | Estado: {estado}")

        time.sleep(1)


if __name__ == "__main__":
    print("Midiendo procesos, espera un momento...")
    procesos = obtener_procesos()

    print(f"\nCPU total: {psutil.cpu_percent(interval=1)} %")
    print(f"Memoria usada: {psutil.virtual_memory().percent} %")
    print(f"Procesos activos: {len(procesos)}")

    mostrar_procesos(procesos)

    print("\n=== Simulación de cambio de contexto (Round Robin) ===")
    simular_cambio_de_contexto(elegir_procesos(procesos))
