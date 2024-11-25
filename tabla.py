import tkinter as tk
from tkinter import ttk
from random import randint

# Generar datos simulados
def generate_processes():
    apps = ["WhatsApp", "Instagram", "YouTube", "Chrome", "Spotify", "TikTok"]
    processes = [{"name": app, "priority": randint(2, 5), "wait_time": 0, "state": "Suspendida"} for app in apps]
    return processes

# Actualizar estados basados en prioridad
def update_process_states():
    global processes

    # Asegurar que solo una aplicación tiene prioridad 1 y está en ejecución
    processes.sort(key=lambda x: x["priority"])  # Ordenar por prioridad
    execution_found = False

    for process in processes:
        if process["priority"] == 1 and not execution_found:
            process["state"] = "Ejecución"
            execution_found = True
        elif process["priority"] > 3:
            process["state"] = "Cerrada"
        else:
            process["state"] = "Suspendida"

# Planificador de procesos
def schedule_processes():
    global processes

    for process in processes[:]:  # Iterar sobre una copia de la lista
        # Incrementar tiempo de espera
        process["wait_time"] += 1

        # Si el tiempo de espera excede el máximo
        if process["wait_time"] > 5:
            process["wait_time"] = 0
            if process["priority"] == 1:
                # Si está en prioridad 1, pasa a "Cerrada" y se elimina del sistema activo
                process["state"] = "Cerrada"
                processes.remove(process)
                continue
            elif process["priority"] > 1:
                # Reducir prioridad por envejecimiento si no es prioridad 1
                process["priority"] = max(1, process["priority"] - 1)

    # Garantizar que solo una aplicación tiene prioridad 1
    enforce_single_priority_one()

    # Actualizar estados basados en prioridad
    update_process_states()

    # Actualizar tabla
    update_table()

    # Reprogramar el planificador
    root.after(2000, schedule_processes)

# Garantizar que solo una aplicación tiene prioridad 1
def enforce_single_priority_one():
    global processes
    priority_one_candidates = [p for p in processes if p["priority"] == 1]

    # Si hay más de un proceso con prioridad 1
    if len(priority_one_candidates) > 1:
        # Ordenar por mayor tiempo de espera y asignar prioridad 1 al primero
        priority_one_candidates.sort(key=lambda x: -x["wait_time"])
        for i, process in enumerate(priority_one_candidates):
            if i == 0:
                process["priority"] = 1
            else:
                process["priority"] = 2

# Actualizar tabla gráfica
def update_table():
    # Eliminar todas las filas actuales de la tabla
    table.delete(*table.get_children())

    # Insertar los procesos ordenados con los valores actualizados
    for process in processes:
        row_id = table.insert("", tk.END, values=(process["name"], process["priority"], process["wait_time"], process["state"]))
        # Resaltar el proceso en estado "Ejecución"
        if process["state"] == "Ejecución":
            table.item(row_id, tags=("ejecucion",))

    # Aplicar estilo para el estado "Ejecución"
    table.tag_configure("ejecucion", background="lightgreen")

# Configuración inicial
processes = generate_processes()
root = tk.Tk()
root.title("Simulación de Planificador de Procesos")

# Tabla
columns = ("Aplicación", "Prioridad", "Tiempo de espera", "Estado")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    table.heading(col, text=col)
table.pack(fill=tk.BOTH, expand=True)

# Iniciar planificador
schedule_processes()

root.mainloop()
