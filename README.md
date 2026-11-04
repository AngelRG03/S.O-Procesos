[README (1).md](https://github.com/user-attachments/files/34387554/README.1.md)
# Monitor de procesos del SO

Proyecto de Sistemas Operativos hecho en Python con la librería **psutil**. Muestra los procesos que se están ejecutando en la computadora y simula un cambio de contexto entre ellos.

## ¿Qué hace?

- Lista los procesos activos con su **PID**, **nombre**, **uso de CPU** y **memoria**.
- Simula un planificador **Round Robin** con algunos procesos reales para ver cuál está *ejecutándose*, cuáles están *listos* y cuáles están *bloqueados* esperando E/S.
- Tiene una **interfaz gráfica** con barras de progreso para la CPU y la memoria.

## Requisitos

- Python 3
- psutil

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

Versión de consola:

```bash
python monitor.py
```

Interfaz gráfica:

```bash
python interfaz.py
```

## Ejemplo de salida

```
## Ejemplo de salida

Resultado de ejecutar `monitor.py` en mi computadora con Windows.

### Lista de procesos

```
CPU total: 9.9 %
Memoria usada: 82.8 %
Procesos activos: 312

    PID  Proceso                       CPU %  Memoria MB  Estado SO
----------------------------------------------------------------------
   5936  rsEngineSvc.exe                 2.9       149.1  running
  25800  python3.11.exe                  2.4        39.7  running
  13972  wallpaper64.exe                 1.3       110.2  running
   4064  NVDisplay.Container.exe         0.5        35.1  running
      4  System                          0.4        11.1  running
  15512  dwm.exe                         0.3       109.2  running
  11352  avp.exe                         0.2       370.3  running
   6080  svchost.exe                     0.1        36.1  running
   9328  WmiPrvSE.exe                    0.1        47.6  running
  24740  Spotify.exe                     0.1       376.9  running
```

### Simulación de cambio de contexto

```
--- Turno 1 ---
PID: 5936 | Proceso: rsEngineSvc.exe | Estado: Ejecutándose
PID: 25800 | Proceso: python3.11.exe | Estado: Listo
PID: 13972 | Proceso: wallpaper64.exe | Estado: Listo
PID: 4064 | Proceso: NVDisplay.Container.exe | Estado: Listo
PID: 4 | Proceso: System | Estado: Listo

--- Turno 4 ---
Cambio de contexto: se guarda wallpaper64.exe y se carga NVDisplay.Container.exe
PID: 5936 | Proceso: rsEngineSvc.exe | Estado: Listo
PID: 25800 | Proceso: python3.11.exe | Estado: Listo
PID: 13972 | Proceso: wallpaper64.exe | Estado: Bloqueado (esperando I/O)
PID: 4064 | Proceso: NVDisplay.Container.exe | Estado: Ejecutándose
PID: 4 | Proceso: System | Estado: Listo

--- Turno 5 ---
Cambio de contexto: se guarda NVDisplay.Container.exe y se carga System
PID: 5936 | Proceso: rsEngineSvc.exe | Estado: Listo
PID: 25800 | Proceso: python3.11.exe | Estado: Listo
PID: 13972 | Proceso: wallpaper64.exe | Estado: Listo
PID: 4064 | Proceso: NVDisplay.Container.exe | Estado: Listo
PID: 4 | Proceso: System | Estado: Ejecutándose
```

### Qué se observa

- En la columna *Estado SO* todos los procesos aparecen como `running`. Esto pasa porque Windows planifica hilos y no procesos, así que psutil no puede dar el estado real de cada proceso.
- En cada turno solo un proceso está *Ejecutándose* y los demás esperan en la cola de *Listos*. Cada vez que entra uno nuevo a la CPU hay un cambio de contexto.
- En el turno 4, `wallpaper64.exe` se bloquea esperando E/S. En el turno 5 termina su E/S y regresa a *Listo*.
```

## Captura de pantalla

<img width="618" height="504" alt="image" src="https://github.com/user-attachments/assets/34fb360c-4977-403f-b827-b1e44c328b16" />


## Multitarea: Windows vs Linux

| Aspecto | Windows | Linux |
|---|---|---|
| Qué planifica | Hilos | Tareas (procesos e hilos se manejan igual) |
| Algoritmo | Por prioridades (0 a 31), con Round Robin entre hilos de la misma prioridad | EEVDF (desde el kernel 6.6, antes CFS): reparte la CPU de forma justa según la prioridad *nice* |
| Tiempo de CPU (quantum) | Fijo, de unas decenas de milisegundos; la ventana activa recibe más | Variable, de pocos milisegundos; depende de cuántos procesos haya |
| Prioridades | Clases: Baja, Normal, Alta, Tiempo real, etc. | Valor *nice* de -20 (más prioridad) a 19 |
| Crear un proceso | `CreateProcess()` | `fork()` y después `exec()` |
| Estados que muestra psutil | Casi todos aparecen como `running` | El estado real: `running`, `sleeping`, `disk-sleep`, `stopped`, `zombie` |
| Herramienta para verlos | Administrador de tareas | `top`, `htop`, `ps` |

Al correr el programa se nota una diferencia: en Windows casi todos los procesos salen como `running`, porque Windows planifica **hilos** y no procesos. En Linux cada proceso muestra su estado real, y la mayoría aparecen como `sleeping` porque están esperando algo (una tecla, la red, el disco).

## Archivos

| Archivo | Descripción |
|---|---|
| `monitor.py` | Lista de procesos y simulación del cambio de contexto en consola |
| `interfaz.py` | Interfaz gráfica con barras de CPU y memoria |
| `requirements.txt` | Librerías necesarias |

## Autor

Reyes Garcia Miguel Angel

Torres Rodriguez Lizeth Danae

