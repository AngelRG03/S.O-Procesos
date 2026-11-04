# S.O-Procesos
Monitor de procesos del SO

Proyecto de Sistemas Operativos hecho en Python con la librería psutil. Muestra los procesos que se están ejecutando en la computadora y simula un cambio de contexto entre ellos.

¿Qué hace?
Lista los procesos activos con su PID, nombre, uso de CPU y memoria.
Simula un planificador Round Robin con algunos procesos reales para ver cuál está ejecutándose, cuáles están listos y cuáles están bloqueados esperando E/S.
Tiene una interfaz gráfica con barras de progreso para la CPU y la memoria.
Requisitos
Python 3
psutil
Instalación
bash
pip install -r requirements.txt
Uso

Versión de consola:

bash
python monitor.py

Interfaz gráfica:

bash
python interfaz.py
Ejemplo de salida
--- Turno 3 ---
Cambio de contexto: se guarda chrome.exe y se carga explorer.exe
PID: 1234 | Proceso: chrome.exe | Estado: Listo
PID: 5678 | Proceso: explorer.exe | Estado: Ejecutándose
PID: 9101 | Proceso: spotify.exe | Estado: Bloqueado (esperando I/O)
Captura de pantalla

Interfaz gráfica

Multitarea: Windows vs Linux
Aspecto	Windows	Linux
Qué planifica	Hilos	Tareas (procesos e hilos se manejan igual)
Algoritmo	Por prioridades (0 a 31), con Round Robin entre hilos de la misma prioridad	EEVDF (desde el kernel 6.6, antes CFS): reparte la CPU de forma justa según la prioridad nice
Tiempo de CPU (quantum)	Fijo, de unas decenas de milisegundos; la ventana activa recibe más	Variable, de pocos milisegundos; depende de cuántos procesos haya
Prioridades	Clases: Baja, Normal, Alta, Tiempo real, etc.	Valor nice de -20 (más prioridad) a 19
Crear un proceso	CreateProcess()	fork() y después exec()
Estados que muestra psutil	Casi todos aparecen como running	El estado real: running, sleeping, disk-sleep, stopped, zombie
Herramienta para verlos	Administrador de tareas	top, htop, ps

Al correr el programa se nota una diferencia: en Windows casi todos los procesos salen como running, porque Windows planifica hilos y no procesos. En Linux cada proceso muestra su estado real, y la mayoría aparecen como sleeping porque están esperando algo (una tecla, la red, el disco).

Archivos
Archivo	Descripción
monitor.py	Lista de procesos y simulación del cambio de contexto en consola
interfaz.py	Interfaz gráfica con barras de CPU y memoria
requirements.txt	Librerías necesarias
Autor
Reyes Garcia Miguel Angel
Torres Rodriguez Lizeth Danae 
