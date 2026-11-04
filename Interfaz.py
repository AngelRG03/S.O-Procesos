# Interfaz gráfica del monitor de procesos
# Muestra barras de progreso para la CPU y la memoria
# y una tabla con los procesos que más CPU usan.

import tkinter as tk
from tkinter import ttk

import psutil

NUCLEOS = psutil.cpu_count()


def actualizar_barras():
    cpu = psutil.cpu_percent()
    memoria = psutil.virtual_memory().percent

    barra_cpu["value"] = cpu
    barra_memoria["value"] = memoria
    etiqueta_cpu.config(text=f"{cpu:.1f} %")
    etiqueta_memoria.config(text=f"{memoria:.1f} %")

    ventana.after(1000, actualizar_barras)  # se repite cada segundo


def actualizar_tabla():
    # La primera vez todos salen con 0 % de CPU porque psutil necesita
    # dos mediciones; a partir de la segunda actualización ya salen bien.
    procesos = []
    for p in psutil.process_iter(['pid', 'name']):
        if p.pid == 0:
            continue
        try:
            cpu = p.cpu_percent() / NUCLEOS
            memoria = p.memory_info().rss / (1024 * 1024)
            procesos.append((p.pid, p.info['name'] or "desconocido", cpu, memoria))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    procesos.sort(key=lambda x: (x[2], x[3]), reverse=True)  # por CPU y luego memoria

    tabla.delete(*tabla.get_children())
    for pid, nombre, cpu, memoria in procesos[:15]:
        tabla.insert("", "end", values=(pid, nombre, f"{cpu:.1f}", f"{memoria:.1f}"))

    ventana.after(3000, actualizar_tabla)  # se repite cada 3 segundos


# ---------- Ventana ----------
ventana = tk.Tk()
ventana.title("Monitor de procesos")
ventana.geometry("620x480")

marco = ttk.Frame(ventana, padding=10)
marco.pack(fill="x")

ttk.Label(marco, text="CPU").grid(row=0, column=0, sticky="w")
barra_cpu = ttk.Progressbar(marco, length=420, maximum=100)
barra_cpu.grid(row=0, column=1, padx=10, pady=5)
etiqueta_cpu = ttk.Label(marco, text="0 %", width=8)
etiqueta_cpu.grid(row=0, column=2)

ttk.Label(marco, text="Memoria").grid(row=1, column=0, sticky="w")
barra_memoria = ttk.Progressbar(marco, length=420, maximum=100)
barra_memoria.grid(row=1, column=1, padx=10, pady=5)
etiqueta_memoria = ttk.Label(marco, text="0 %", width=8)
etiqueta_memoria.grid(row=1, column=2)

columnas = ("pid", "nombre", "cpu", "memoria")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
tabla.heading("pid", text="PID")
tabla.heading("nombre", text="Proceso")
tabla.heading("cpu", text="CPU %")
tabla.heading("memoria", text="Memoria (MB)")
tabla.column("pid", width=70, anchor="center")
tabla.column("nombre", width=280)
tabla.column("cpu", width=80, anchor="center")
tabla.column("memoria", width=110, anchor="center")
tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))

actualizar_barras()
actualizar_tabla()
ventana.mainloop()
