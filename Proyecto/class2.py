import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta

# ----------------------- CLASES ---------------------------

class Paciente:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

class Doctor:
    def __init__(self, nombre, especialidad, edad, turno):
        self.nombre = nombre
        self.especialidad = especialidad
        self.edad = edad
        self.turno = turno

class Enfermero:
    def __init__(self, nombre, edad, turno):
        self.nombre = nombre
        self.edad = edad
        self.turno = turno

class Area:
    def __init__(self, nombre):
        self.nombre = nombre
        self.camillas = [False for _ in range(5)]

# ------------------- DATOS DE EJEMPLO --------------------

doctores = [
    Doctor("Dra. García", "Pediatría", 45, "Mañana"),
    Doctor("Dr. López", "Cardiología", 50, "Tarde"),
    Doctor("Dra. Ruiz", "Neurología", 38, "Noche")
]

areas = [
    Area("Pediatría"),
    Area("Cardiología"),
    Area("Neurología")
]

movimientos = []

# ------------------- INTERFAZ GRÁFICA ---------------------

ventana = tk.Tk()
ventana.title("Control de Pacientes - Hospital")
ventana.geometry("1000x600")

# Tabla de registros
tabla = ttk.Treeview(ventana)
tabla["columns"] = ("Fecha", "Paciente", "Edad", "Doctor", "Especialidad", "Área", "Camilla")
tabla.heading("#0", text="ID")
tabla.column("#0", width=30)

for col in tabla["columns"]:
    tabla.heading(col, text=col)

tabla.pack(expand=True, fill="both")

# ---------- FORMULARIO PARA REGISTRAR NUEVOS PACIENTES ------------

formulario = tk.Frame(ventana)
formulario.pack(pady=10)

# Entradas para datos
entradas = {
    "Paciente": tk.Entry(formulario),
    "Edad Paciente": tk.Entry(formulario),
    "Doctor": tk.Entry(formulario),
    "Edad Doctor": tk.Entry(formulario),
    "Especialidad": tk.Entry(formulario),
    "Turno Doctor": tk.Entry(formulario),
    "Área": ttk.Combobox(formulario, values=[a.nombre for a in areas]),
    "Camilla": ttk.Combobox(formulario, values=[str(i+1) for i in range(5)])
}

# Mostrar etiquetas y cajas de texto
for i, (campo, entrada) in enumerate(entradas.items()):
    tk.Label(formulario, text=campo + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entrada.grid(row=i, column=1, padx=5, pady=2)

# Función para registrar paciente
def registrar_paciente():
    nombre = entradas["Paciente"].get()
    edad = entradas["Edad Paciente"].get()
    doc_nombre = entradas["Doctor"].get()
    doc_edad = entradas["Edad Doctor"].get()
    especialidad = entradas["Especialidad"].get()
    turno = entradas["Turno Doctor"].get()
    area_nombre = entradas["Área"].get()
    camilla_num = int(entradas["Camilla"].get()) - 1

    paciente = Paciente(nombre, int(edad))
    doctor = Doctor(doc_nombre, especialidad, int(doc_edad), turno)
    area = next((a for a in areas if a.nombre == area_nombre), None)

    if area and not area.camillas[camilla_num]:
        area.camillas[camilla_num] = True
        fecha = datetime.now().strftime("%Y-%m-%d")
        movimientos.append((fecha, paciente, doctor, area.nombre, camilla_num + 1))

        tabla.insert("", "end", text=str(len(movimientos)), values=(
            fecha, paciente.nombre, paciente.edad,
            doctor.nombre, doctor.especialidad,
            area.nombre, camilla_num + 1
        ))
    else:
        tk.messagebox.showwarning("Advertencia", "Camilla ocupada o área inválida")

# Botón para registrar
tk.Button(formulario, text="Registrar Paciente", command=registrar_paciente).grid(row=len(entradas), columnspan=2, pady=10)

# -------- BOTÓN PARA VER CAMILLAS OCUPADAS ------------

def mostrar_camillas():
    camilla_ventana = tk.Toplevel()
    camilla_ventana.title("Estado de camillas")

    for area in areas:
        estado = [f"Camilla {i+1}: {'Ocupada' if c else 'Libre'}" for i, c in enumerate(area.camillas)]
        tk.Label(camilla_ventana, text=f"Área: {area.nombre}", font=("Arial", 12, "bold")).pack()
        for linea in estado:
            tk.Label(camilla_ventana, text=linea).pack()

tk.Button(ventana, text="Ver camillas ocupadas", command=mostrar_camillas).pack(pady=10)

ventana.mainloop()
