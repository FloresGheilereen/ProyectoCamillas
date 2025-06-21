import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class Doctor:
    def __init__(self, nombre, especialidad, edad, genero, turno, piso):
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

class Enfermero:
    def __init__(self, nombre, genero, turno, piso):
        self.nombre = nombre
        self.genero = genero
        self.turno = turno
        self.piso = piso
        self.hora_entrada = datetime.now().strftime("%H:%M:%S")
        self.hora_salida = None

    def registrar_salida(self):
        self.hora_salida = datetime.now().strftime("%H:%M:%S")

class Paciente:
    def __init__(self, nombre, edad, genero, camilla, piso, doctor, enfermero):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.camilla = camilla
        self.piso = piso
        self.doctor = doctor
        self.enfermero = enfermero
        self.hora_entrada = datetime.now().strftime("%H:%M:%S")
        self.fecha_entrada = datetime.now().strftime("%Y-%m-%d")  # para filtro por fecha
        self.hora_salida = None

    def registrar_salida(self):
        self.hora_salida = datetime.now().strftime("%H:%M:%S")

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Hospitalaria")
        self.root.geometry("900x600")

        # Datos
        self.doctores = []
        self.enfermeros = []
        self.pacientes = []
        self.historial = []
        self.camillas_disponibles = list(range(1, 11))

        # UI general
        self.menu_lateral = tk.Frame(self.root, bg="lightblue", width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill="y")

        self.area_dinamica = tk.Frame(self.root, bg="white")
        self.area_dinamica.pack(side=tk.RIGHT, fill="both", expand=True)

        # Botones menú
        tk.Button(self.menu_lateral, text="Registrar Doctor", width=18, command=self.menu_doctor).pack(pady=10)
        tk.Button(self.menu_lateral, text="Registrar Enfermero", width=18, command=self.menu_enfermero).pack(pady=10)
        tk.Button(self.menu_lateral, text="Pacientes", width=18, command=self.menu_pacientes).pack(pady=10)
        tk.Button(self.menu_lateral, text="Historial Pacientes", width=18, command=self.menu_historial).pack(pady=10)
        tk.Button(self.menu_lateral, text="Salir", width=18, command=self.root.destroy).pack(side=tk.BOTTOM, pady=20)

        self.menu_doctor()  # Mostrar inicio

    def limpiar_area(self):
        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

    def menu_doctor(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Doctor", font=("Arial", 16)).pack(pady=10)

        # Campos
        frame = tk.Frame(self.area_dinamica)
        frame.pack(pady=5)

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        entry_nombre = tk.Entry(frame)
        entry_nombre.grid(row=0, column=1)

        tk.Label(frame, text="Especialidad:").grid(row=1, column=0, sticky="e")
        entry_esp = tk.Entry(frame)
        entry_esp.grid(row=1, column=1)

        tk.Label(frame, text="Edad:").grid(row=2, column=0, sticky="e")
        entry_edad = tk.Entry(frame)
        entry_edad.grid(row=2, column=1)

        tk.Label(frame, text="Género (M/F/O):").grid(row=3, column=0, sticky="e")
        entry_genero = tk.Entry(frame)
        entry_genero.grid(row=3, column=1)

        tk.Label(frame, text="Turno:").grid(row=4, column=0, sticky="e")
        turno_var = tk.StringVar(value="Matutino")
        ttk.Combobox(frame, textvariable=turno_var, values=["Matutino", "Vespertino", "Nocturno"], state="readonly").grid(row=4, column=1)

        tk.Label(frame, text="Piso asignado:").grid(row=5, column=0, sticky="e")
        entry_piso = tk.Entry(frame)
        entry_piso.grid(row=5, column=1)

        def guardar_doctor():
            nombre = entry_nombre.get().strip()
            especialidad = entry_esp.get().strip()
            try:
                edad = int(entry_edad.get())
            except:
                messagebox.showerror("Error", "Edad inválida")
                return
            genero = entry_genero.get().strip().upper()
            if genero not in ["M", "F", "O"]:
                messagebox.showerror("Error", "Género debe ser M, F o O")
                return
            genero_full = {"M": "Masculino", "F": "Femenino", "O": "Otro"}[genero]
            turno = turno_var.get()
            piso = entry_piso.get().strip()
            if not nombre or not especialidad or not piso:
                messagebox.showerror("Error", "Completa todos los campos")
                return

            doc = Doctor(nombre, especialidad, edad, genero_full, turno, piso)
            self.doctores.append(doc)
            messagebox.showinfo("Guardado", f"Doctor {nombre} registrado.")

            self.refrescar_tabla_doctores()
            # Limpiar campos
            entry_nombre.delete(0, tk.END)
            entry_esp.delete(0, tk.END)
            entry_edad.delete(0, tk.END)
            entry_genero.delete(0, tk.END)
            entry_piso.delete(0, tk.END)

        tk.Button(self.area_dinamica, text="Guardar Doctor", command=guardar_doctor).pack(pady=10)

        # Tabla de doctores
        self.tabla_doctores = ttk.Treeview(self.area_dinamica,
                                           columns=("Nombre", "Especialidad", "Edad", "Género", "Turno", "Piso", "Entrada", "Salida"),
                                           show="headings")
        for col in self.tabla_doctores["columns"]:
            self.tabla_doctores.heading(col, text=col)
        self.tabla_doctores.pack(expand=True, fill="both", padx=10, pady=10)

        self.refrescar_tabla_doctores()

    def refrescar_tabla_doctores(self):
        if hasattr(self, "tabla_doctores"):
            self.tabla_doctores.delete(*self.tabla_doctores.get_children())
            for d in self.doctores:
                salida = d.hora_salida if d.hora_salida else "-"
                self.tabla_doctores.insert("", "end",
                                          values=(d.nombre, d.especialidad, d.edad, d.genero, d.turno, d.piso, d.hora_entrada, salida))

    def menu_enfermero(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Enfermero", font=("Arial", 16)).pack(pady=10)

        # Campos
        frame = tk.Frame(self.area_dinamica)
        frame.pack(pady=5)

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        entry_nombre = tk.Entry(frame)
        entry_nombre.grid(row=0, column=1)

        tk.Label(frame, text="Género (M/F/O):").grid(row=1, column=0, sticky="e")
        entry_genero = tk.Entry(frame)
        entry_genero.grid(row=1, column=1)

        tk.Label(frame, text="Turno:").grid(row=2, column=0, sticky="e")
        turno_var = tk.StringVar(value="Matutino")
        ttk.Combobox(frame, textvariable=turno_var, values=["Matutino", "Vespertino", "Nocturno"], state="readonly").grid(row=2, column=1)

        tk.Label(frame, text="Piso asignado:").grid(row=3, column=0, sticky="e")
        entry_piso = tk.Entry(frame)
        entry_piso.grid(row=3, column=1)

        def guardar_enfermero():
            nombre = entry_nombre.get().strip()
            genero = entry_genero.get().strip().upper()
            if genero not in ["M", "F", "O"]:
                messagebox.showerror("Error", "Género debe ser M, F o O")
                return
            genero_full = {"M": "Masculino", "F": "Femenino", "O": "Otro"}[genero]
            turno = turno_var.get()
            piso = entry_piso.get().strip()
            if not nombre or not piso:
                messagebox.showerror("Error", "Completa todos los campos")
                return

            enf = Enfermero(nombre, genero_full, turno, piso)
            self.enfermeros.append(enf)
            messagebox.showinfo("Guardado", f"Enfermero {nombre} registrado.")

            self.refrescar_tabla_enfermeros()
            # Limpiar campos
            entry_nombre.delete(0, tk.END)
            entry_genero.delete(0, tk.END)
            entry_piso.delete(0, tk.END)

        tk.Button(self.area_dinamica, text="Guardar Enfermero", command=guardar_enfermero).pack(pady=10)

        # Tabla de enfermeros
        self.tabla_enfermeros = ttk.Treeview(self.area_dinamica,
                                             columns=("Nombre", "Género", "Turno", "Piso", "Entrada", "Salida"),
                                             show="headings")
        for col in self.tabla_enfermeros["columns"]:
            self.tabla_enfermeros.heading(col, text=col)
        self.tabla_enfermeros.pack(expand=True, fill="both", padx=10, pady=10)

        self.refrescar_tabla_enfermeros()

    def refrescar_tabla_enfermeros(self):
        if hasattr(self, "tabla_enfermeros"):
            self.tabla_enfermeros.delete(*self.tabla_enfermeros.get_children())
            for e in self.enfermeros:
                salida = e.hora_salida if e.hora_salida else "-"
                self.tabla_enfermeros.insert("", "end",
                                            values=(e.nombre, e.genero, e.turno, e.piso, e.hora_entrada, salida))

    def menu_pacientes(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Pacientes", font=("Arial", 16)).pack(pady=10)

        btn_frame = tk.Frame(self.area_dinamica)
        btn_frame.pack()

        tk.Button(btn_frame, text="Agregar Paciente", command=self.agregar_paciente).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar Paciente", command=self.eliminar_paciente).pack(side=tk.LEFT, padx=5)

        self.label_camillas = tk.Label(self.area_dinamica, text=self.get_camillas_libres())
        self.label_camillas.pack(pady=10)

        self.tree_pacientes = ttk.Treeview(self.area_dinamica,
                                          columns=("Nombre", "Edad", "Género", "Camilla", "Piso", "Doctor", "Enfermero", "Entrada"),
                                          show="headings")
        for col in self.tree_pacientes["columns"]:
            self.tree_pacientes.heading(col, text=col)
        self.tree_pacientes.pack(expand=True, fill="both", padx=10, pady=10)

        self.refrescar_tabla_pacientes()

    def get_camillas_libres(self):
        return f"Camillas libres: {', '.join(str(c) for c in self.camillas_disponibles)}"

    def refrescar_tabla_pacientes(self):
        if hasattr(self, "tree_pacientes"):
            self.tree_pacientes.delete(*self.tree_pacientes.get_children())
            for p in self.pacientes:
                self.tree_pacientes.insert("", "end",
                                          values=(p.nombre, p.edad, p.genero, p.camilla, p.piso, p.doctor, p.enfermero, p.hora_entrada))

    def agregar_paciente(self):
        if not self.camillas_disponibles:
            messagebox.showwarning("Sin camillas", "Todas las camillas están ocupadas.")
            return

        nombre = simpledialog.askstring("Paciente", "Nombre del paciente:")
        if not nombre:
            return
        edad = simpledialog.askinteger("Paciente", "Edad del paciente:")
        if edad is None:
            return
        genero_input = simpledialog.askstring("Paciente", "Género del paciente (M/F/O):")
        if not genero_input or genero_input.strip().upper() not in ["M", "F", "O"]:
            messagebox.showerror("Error", "Género inválido")
            return
        genero = {"M": "Masculino", "F": "Femenino", "O": "Otro"}[genero_input.strip().upper()]

        piso = simpledialog.askstring("Paciente", "¿En qué piso estará? (Dejar vacío para asignar automático):")
        piso = piso.strip() if piso else ""

        # Si no pone piso, intentar asignar según doctor/enfermero disponible
        if not piso:
            # Tomamos primer doctor con camilla disponible
            pisos_disponibles = {d.piso for d in self.doctores} & {e.piso for e in self.enfermeros}
            if pisos_disponibles:
                piso = list(pisos_disponibles)[0]
            else:
                piso = "General"

        # Buscar doctor y enfermero para ese piso
        doctor = next((d.nombre for d in self.doctores if d.piso == piso), "Ninguno")
        enfermero = next((e.nombre for e in self.enfermeros if e.piso == piso), "Ninguno")

        camilla = self.camillas_disponibles.pop(0)

        paciente = Paciente(nombre, edad, genero, camilla, piso, doctor, enfermero)
        self.pacientes.append(paciente)
        self.historial.append(paciente)
        self.refrescar_tabla_pacientes()
        self.label_camillas.config(text=self.get_camillas_libres())

    def eliminar_paciente(self):
        seleccion = self.tree_pacientes.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Selecciona un paciente para eliminar")
            return
        item = self.tree_pacientes.item(seleccion[0])
        nombre = item["values"][0]
        paciente = next((p for p in self.pacientes if p.nombre == nombre), None)
        if paciente:
            paciente.registrar_salida()
            self.pacientes.remove(paciente)
            self.camillas_disponibles.append(paciente.camilla)
            self.camillas_disponibles.sort()
            self.refrescar_tabla_pacientes()
            self.label_camillas.config(text=self.get_camillas_libres())

    def menu_historial(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Historial de Pacientes", font=("Arial", 16)).pack(pady=10)

        # Filtros
        filtros_frame = tk.Frame(self.area_dinamica)
        filtros_frame.pack(pady=5, fill="x")

        tk.Label(filtros_frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        entry_nombre = tk.Entry(filtros_frame)
        entry_nombre.grid(row=0, column=1)

        tk.Label(filtros_frame, text="Género:").grid(row=0, column=2, sticky="e")
        genero_var = tk.StringVar(value="Todos")
        genero_combo = ttk.Combobox(filtros_frame, textvariable=genero_var, values=["Todos", "Masculino", "Femenino", "Otro"], state="readonly")
        genero_combo.grid(row=0, column=3)

        tk.Label(filtros_frame, text="Piso:").grid(row=0, column=4, sticky="e")
        entry_piso = tk.Entry(filtros_frame)
        entry_piso.grid(row=0, column=5)

        tk.Label(filtros_frame, text="Fecha (YYYY-MM-DD):").grid(row=0, column=6, sticky="e")
        entry_fecha = tk.Entry(filtros_frame)
        entry_fecha.grid(row=0, column=7)

        def aplicar_filtros():
            nombre_f = entry_nombre.get().strip().lower()
            genero_f = genero_var.get()
            piso_f = entry_piso.get().strip().lower()
            fecha_f = entry_fecha.get().strip()

            filtrados = self.historial
            if nombre_f:
                filtrados = [p for p in filtrados if nombre_f in p.nombre.lower()]
            if genero_f != "Todos":
                filtrados = [p for p in filtrados if p.genero == genero_f]
            if piso_f:
                filtrados = [p for p in filtrados if piso_f in p.piso.lower()]
            if fecha_f:
                # Validar formato fecha
                try:
                    datetime.strptime(fecha_f, "%Y-%m-%d")
                    filtrados = [p for p in filtrados if p.fecha_entrada == fecha_f]
                except:
                    messagebox.showerror("Error", "Fecha inválida. Usa formato YYYY-MM-DD.")
                    return

            self.refrescar_tabla_historial(filtrados)

        tk.Button(filtros_frame, text="Buscar", command=aplicar_filtros).grid(row=0, column=8, padx=5)

        # Tabla historial
        self.tabla_historial = ttk.Treeview(self.area_dinamica,
                                            columns=("Nombre", "Edad", "Género", "Camilla", "Piso", "Doctor", "Enfermero", "Entrada", "Salida"),
                                            show="headings")
        for col in self.tabla_historial["columns"]:
            self.tabla_historial.heading(col, text=col)
        self.tabla_historial.pack(expand=True, fill="both", padx=10, pady=10)

        self.refrescar_tabla_historial(self.historial)

    def refrescar_tabla_historial(self, datos):
        if hasattr(self, "tabla_historial"):
            self.tabla_historial.delete(*self.tabla_historial.get_children())
            for p in datos:
                salida = p.hora_salida if p.hora_salida else "-"
                self.tabla_historial.insert("", "end",
                                           values=(p.nombre, p.edad, p.genero, p.camilla, p.piso, p.doctor, p.enfermero, p.hora_entrada, salida))

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
