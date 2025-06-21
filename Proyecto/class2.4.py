import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Doctor:
    def __init__(self, nombre, especialidad, edad, turno):
        self.nombre = nombre
        self.especialidad = especialidad
        self.edad = edad
        self.turno = turno

class Enfermero:
    def __init__(self, nombre):
        self.nombre = nombre

class Paciente:
    def __init__(self, nombre, edad, genero, camilla, piso, doctor, enfermero):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.camilla = camilla
        self.piso = piso
        self.doctor = doctor
        self.enfermero = enfermero

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz para prácticas")
        self.root.geometry("800x500")
        self.root.config(bg="lightblue")

        self.pacientes = []
        self.camillas_disponibles = list(range(1, 10))

        self.menu_lateral = tk.Frame(self.root, bg="lightblue", width=140)
        self.menu_lateral.pack(side="left", fill="y")

        self.area_dinamica = tk.Frame(self.root, bg="white")
        self.area_dinamica.pack(side="right", expand=True, fill="both")

        tk.Button(self.menu_lateral, text="Inicio", command=self.saludo_bienvenida, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Datos del alumno", command=self.opciones_alumnos, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Estética", command=self.estetica_tres, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Pacientes", command=self.seccion_pacientes, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Salir", command=self.root.destroy, width=15).pack(pady=30)

        self.saludo_bienvenida()

    def limpiar_area(self):
        for widget in self.area_dinamica.winfo_children():
            widget.destroy()

    def saludo_bienvenida(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Hola, es un gusto tenerte aquí", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.area_dinamica, text="Mostrar mensaje de bienvenida",
                  command=lambda: messagebox.showinfo("Bienvenida", "Hola, bienvenido al programa")).pack()

    def opciones_alumnos(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Datos del alumno", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.area_dinamica, text="Nombre del alumno:").pack()
        campo_texto_uno = tk.Entry(self.area_dinamica)
        campo_texto_uno.pack(pady=5)

        tk.Label(self.area_dinamica, text="Elige tu nivel:").pack()
        opcion_elegida = tk.StringVar(value="Cirujano")
        for nivel in ["Cirujano", "Medico", "Enfermero"]:
            tk.Radiobutton(self.area_dinamica, text=nivel, variable=opcion_elegida, value=nivel).pack()

        tk.Label(self.area_dinamica, text="En qué especialidad estás?:").pack()
        combo = ttk.Combobox(self.area_dinamica,
                             values=["Cardiólogo", "Cirugía general", "Dermatólogo", "Neurología", "Oftalmología",
                                     "Pediatra"])
        combo.pack()
        combo.current(0)

        def guardar_opciones():
            ventana = tk.Toplevel(self.root)
            ventana.title("Tabla de Pacientes")

            tabla = ttk.Treeview(ventana, columns=("ID", "Paciente", "Edad", "Tratamiento", "Fecha", "Hora"), show="headings")
            for col in tabla["columns"]:
                tabla.heading(col, text=col)
            tabla.insert("", "end", values=("1", "Juan", "25", "Consulta general", "04/06/2025", "10:00"))
            tabla.insert("", "end", values=("2", "Maria", "30", "Dermatología", "04/06/2025", "11:00"))
            tabla.insert("", "end", values=("3", "Pedro", "22", "Neurología", "04/06/2025", "12:00"))
            tabla.pack(expand=True, fill="both")

        tk.Button(self.area_dinamica, text="Mostrar datos", command=guardar_opciones).pack(pady=10)

    def estetica_tres(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Configuraciones de estética", font=("Arial", 14)).pack(pady=10)
        colores = ["lightblue", "lightgreen", "lightyellow", "lightgray"]
        tk.Label(self.area_dinamica, text="Cambiar fondo:").pack()

        def cambiar_color(c):
            self.root.config(bg=c)
            self.menu_lateral.config(bg=c)

        for c in colores:
            tk.Button(self.area_dinamica, text=c, bg=c, width=20, command=lambda col=c: cambiar_color(col)).pack(pady=2)

    def seccion_pacientes(self):
        self.limpiar_area()
        self.obtener_datos_personal()

        frame_botones = tk.Frame(self.area_dinamica, bg="white")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Llamar Paciente", command=self.agregar_paciente).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar Paciente", command=self.eliminar_paciente).pack(side="left", padx=5)

        self.label_camillas = tk.Label(self.area_dinamica, text=self.get_camillas_libres(), bg="white")
        self.label_camillas.pack(pady=10)

        self.tree = ttk.Treeview(self.area_dinamica,
                                 columns=("Nombre", "Edad", "Género", "Camilla", "Piso", "Doctor", "Enfermero"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def obtener_datos_personal(self):
        if hasattr(self, "doctor"):
            return  # Ya se ingresaron

        nombre_doctor = simpledialog.askstring("Doctor", "Nombre del doctor:")
        especialidad = simpledialog.askstring("Doctor", "Especialidad:")
        edad_doctor = simpledialog.askinteger("Doctor", "Edad del doctor:")

        turno_win = tk.Toplevel(self.root)
        turno_win.title("Seleccionar Turno")
        turno_win.geometry("250x150")

        turno_var = tk.StringVar(value="Matutino")

        tk.Label(turno_win, text="Seleccione el turno del doctor:").pack(pady=5)
        for turno in ["Matutino", "Vespertino", "Nocturno"]:
            tk.Radiobutton(turno_win, text=turno, variable=turno_var, value=turno).pack(anchor="w", padx=20)

        def confirmar_turno():
            turno_win.destroy()
            self.doctor = Doctor(nombre_doctor, especialidad, edad_doctor, turno_var.get())
            nombre_enfermero = simpledialog.askstring("Enfermero", "Nombre del enfermero(a):")
            self.enfermero = Enfermero(nombre_enfermero)

        tk.Button(turno_win, text="Aceptar", command=confirmar_turno).pack(pady=10)

        turno_win.transient(self.root)
        turno_win.grab_set()
        self.root.wait_window(turno_win)

    def get_camillas_libres(self):
        return f"Camillas libres: {', '.join(str(c) for c in self.camillas_disponibles)}"

    def actualizar_camillas_libres(self):
        self.label_camillas.config(text=self.get_camillas_libres())

    def convertir_genero(self, genero):
        genero = genero.strip().upper()
        return "Masculino" if genero == "M" else "Femenino" if genero == "F" else "Otro"

    def agregar_paciente(self):
        if not self.camillas_disponibles:
            messagebox.showwarning("Sin camillas", "Todas las camillas están ocupadas.")
            return

        nombre = simpledialog.askstring("Paciente", "Nombre del paciente:")
        edad = simpledialog.askinteger("Paciente", "Edad del paciente:")
        genero_input = simpledialog.askstring("Paciente", "Género del paciente (M/F/Otro):")
        genero = self.convertir_genero(genero_input)
        piso = simpledialog.askstring("Paciente", "¿En qué piso estará?")

        camilla = self.camillas_disponibles.pop(0)
        paciente = Paciente(nombre, edad, genero, camilla, piso, self.doctor.nombre, self.enfermero.nombre)
        self.pacientes.append(paciente)

        self.tree.insert("", "end",
                         values=(paciente.nombre, paciente.edad, paciente.genero, paciente.camilla, paciente.piso,
                                 paciente.doctor, paciente.enfermero))
        self.actualizar_camillas_libres()

    def eliminar_paciente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showinfo("Eliminar", "Selecciona un paciente para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Deseas eliminar al paciente seleccionado?")
        if respuesta:
            item = seleccionado[0]
            valores = self.tree.item(item, "values")
            camilla = int(valores[3])
            self.camillas_disponibles.append(camilla)
            self.camillas_disponibles.sort()
            self.tree.delete(item)
            self.pacientes = [p for p in self.pacientes if p.camilla != camilla]
            self.actualizar_camillas_libres()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
