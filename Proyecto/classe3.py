# Este es un programa para gestionar un hospital con interfaz gráfica usando tkinter

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ---------- CLASE DOCTOR ----------
class Doctor:
    contador_id = 1  # Se usará para asignar un ID único a cada doctor

    def __init__(self, nombre, especialidad, edad, genero, turno, piso):
        self.id = Doctor.contador_id
        Doctor.contador_id += 1
        self.nombre = nombre
        self.especialidad = especialidad
        self.edad = edad
        self.genero = genero
        self.turno = turno
        self.piso = piso
        self.hora_entrada = datetime.now().strftime("%H:%M:%S")
        self.hora_salida = None

    def registrar_salida(self):
        self.hora_salida = datetime.now().strftime("%H:%M:%S")

# ---------- CLASE ENFERMERO ----------
class Enfermero:
    contador_id = 1

    def __init__(self, nombre, genero, turno, piso):
        self.id = Enfermero.contador_id
        Enfermero.contador_id += 1
        self.nombre = nombre
        self.genero = genero
        self.turno = turno
        self.piso = piso
        self.hora_entrada = datetime.now().strftime("%H:%M:%S")
        self.hora_salida = None

    def registrar_salida(self):
        self.hora_salida = datetime.now().strftime("%H:%M:%S")

# ---------- CLASE PACIENTE ----------
class Paciente:
    def __init__(self, nombre, edad, genero, camilla, piso, doctor, enfermero):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.camilla = camilla  # Número de camilla asignada
        self.piso = piso
        self.doctor = doctor  # Nombre del doctor asignado
        self.enfermero = enfermero  # Nombre del enfermero asignado
        self.hora_entrada = datetime.now().strftime("%H:%M:%S")
        self.fecha_entrada = datetime.now().strftime("%Y-%m-%d")
        self.hora_salida = None

    def registrar_salida(self):
        self.hora_salida = datetime.now().strftime("%H:%M:%S")

# ---------- CLASE PRINCIPAL ----------
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Hospitalaria")
        self.root.geometry("950x600")

        # Listas para almacenar los registros
        self.doctores = []
        self.enfermeros = []
        self.pacientes = []
        self.historial = []

        # Lista de camillas libres
        self.camillas_disponibles = list(range(1, 11))

        # MENÚ LATERAL (Botones)
        self.menu_lateral = tk.Frame(self.root, bg="lightblue", width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill="y")

        # ÁREA DINÁMICA donde se muestra cada sección
        self.area_dinamica = tk.Frame(self.root, bg="white")
        self.area_dinamica.pack(side=tk.RIGHT, fill="both", expand=True)

        # Botones del menú lateral
        tk.Button(self.menu_lateral, text="Registrar Doctor", width=18, command=self.menu_doctor).pack(pady=10)
        tk.Button(self.menu_lateral, text="Registrar Enfermero", width=18, command=self.menu_enfermero).pack(pady=10)
        tk.Button(self.menu_lateral, text="Pacientes", width=18, command=self.menu_pacientes).pack(pady=10)
        tk.Button(self.menu_lateral, text="Historial", width=18, command=self.menu_historial).pack(pady=10)
        tk.Button(self.menu_lateral, text="Salir", width=18, command=self.root.destroy).pack(side=tk.BOTTOM, pady=20)

        self.menu_doctor()

    def limpiar_area(self):
        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

    # ---------- MENÚ DOCTOR ----------
    def menu_doctor(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Doctor", font=("Arial", 16)).pack(pady=10)
        frame = tk.Frame(self.area_dinamica)
        frame.pack(pady=5)

        entrys = {}
        campos = ["Nombre", "Especialidad", "Edad", "Género (M/F/O)", "Turno", "Piso"]
        for i, campo in enumerate(campos):
            tk.Label(frame, text=campo + ":").grid(row=i, column=0, sticky="e")
            entrys[campo] = tk.Entry(frame)
            entrys[campo].grid(row=i, column=1)

        def guardar():
            try:
                d = Doctor(
                    entrys["Nombre"].get(),
                    entrys["Especialidad"].get(),
                    int(entrys["Edad"].get()),
                    entrys["Género (M/F/O)"].get(),
                    entrys["Turno"].get(),
                    entrys["Piso"].get()
                )
                self.doctores.append(d)
                self.refrescar_tabla_doctores()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.area_dinamica, text="Guardar", command=guardar).pack(pady=10)

        self.tabla_doctores = ttk.Treeview(self.area_dinamica,
            columns=("ID", "Nombre", "Especialidad", "Edad", "Género", "Turno", "Piso", "Entrada", "Salida"),
            show="headings")
        for col in self.tabla_doctores["columns"]:
            self.tabla_doctores.heading(col, text=col)
        self.tabla_doctores.pack(expand=True, fill="both", padx=10, pady=10)
        self.refrescar_tabla_doctores()

    def refrescar_tabla_doctores(self):
        self.tabla_doctores.delete(*self.tabla_doctores.get_children())
        for d in self.doctores:
            salida = d.hora_salida if d.hora_salida else "-"
            self.tabla_doctores.insert("", "end",
                values=(d.id, d.nombre, d.especialidad, d.edad, d.genero, d.turno, d.piso, d.hora_entrada, salida))

    # ---------- MENÚ ENFERMERO ----------
    def menu_enfermero(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Enfermero", font=("Arial", 16)).pack(pady=10)
        frame = tk.Frame(self.area_dinamica)
        frame.pack(pady=5)

        entrys = {}
        campos = ["Nombre", "Género (M/F/O)", "Turno", "Piso"]
        for i, campo in enumerate(campos):
            tk.Label(frame, text=campo + ":").grid(row=i, column=0, sticky="e")
            entrys[campo] = tk.Entry(frame)
            entrys[campo].grid(row=i, column=1)

        def guardar():
            try:
                e = Enfermero(
                    entrys["Nombre"].get(),
                    entrys["Género (M/F/O)"].get(),
                    entrys["Turno"].get(),
                    entrys["Piso"].get()
                )
                self.enfermeros.append(e)
                self.refrescar_tabla_enfermeros()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        tk.Button(self.area_dinamica, text="Guardar", command=guardar).pack(pady=10)

        self.tabla_enfermeros = ttk.Treeview(self.area_dinamica,
            columns=("ID", "Nombre", "Género", "Turno", "Piso", "Entrada", "Salida"),
            show="headings")
        for col in self.tabla_enfermeros["columns"]:
            self.tabla_enfermeros.heading(col, text=col)
        self.tabla_enfermeros.pack(expand=True, fill="both", padx=10, pady=10)
        self.refrescar_tabla_enfermeros()

    def refrescar_tabla_enfermeros(self):
        self.tabla_enfermeros.delete(*self.tabla_enfermeros.get_children())
        for e in self.enfermeros:
            salida = e.hora_salida if e.hora_salida else "-"
            self.tabla_enfermeros.insert("", "end",
                values=(e.id, e.nombre, e.genero, e.turno, e.piso, e.hora_entrada, salida))

    # ---------- AQUÍ FALTARÍAN PACIENTES E HISTORIAL ----------
    # Si necesitas incluirlos con comentarios, dímelo y te los genero completos.

# Ejecutamos la app
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
