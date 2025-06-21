import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

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
    def __init__(self, nombre, edad, genero, camilla, piso, hora_entrada):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.camilla = camilla
        self.piso = piso
        self.hora_entrada = hora_entrada
        self.hora_salida = None

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pacientes")
        self.root.geometry("800x500")
        self.root.config(bg="lightblue")

        self.doctor = None
        self.enfermero = None
        self.pacientes = []
        self.historial = []
        self.camillas_disponibles = list(range(1, 10))

        self.menu_lateral = tk.Frame(self.root, bg="lightblue", width=140)
        self.menu_lateral.pack(side="left", fill="y")

        self.area_dinamica = tk.Frame(self.root, bg="white")
        self.area_dinamica.pack(side="right", expand=True, fill="both")

        tk.Button(self.menu_lateral, text="Inicio", command=self.saludo_bienvenida, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Pacientes", command=self.seccion_pacientes, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Historial", command=self.ver_historial, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Registrar Doctor", command=self.registrar_doctor, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Registrar Enfermero", command=self.registrar_enfermero, width=15).pack(pady=10)
        tk.Button(self.menu_lateral, text="Estética", command=self.estetica_tres, width=15).pack(pady=10)
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

    def registrar_doctor(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Doctor", font=("Arial", 14)).pack(pady=10)

        nombre = simpledialog.askstring("Doctor", "Nombre del doctor:")
        especialidad = simpledialog.askstring("Doctor", "Especialidad:")
        edad = simpledialog.askinteger("Doctor", "Edad:")

        turno_win = tk.Toplevel(self.root)
        turno_win.title("Seleccionar Turno")
        turno_win.geometry("250x150")
        turno_var = tk.StringVar(value="Matutino")

        tk.Label(turno_win, text="Seleccione el turno:").pack(pady=5)
        for turno in ["Matutino", "Vespertino", "Nocturno"]:
            tk.Radiobutton(turno_win, text=turno, variable=turno_var, value=turno).pack(anchor="w", padx=20)

        def confirmar_turno():
            turno_win.destroy()
            self.doctor = Doctor(nombre, especialidad, edad, turno_var.get())
            messagebox.showinfo("Éxito", "Doctor registrado correctamente.")

        tk.Button(turno_win, text="Aceptar", command=confirmar_turno).pack(pady=10)
        turno_win.transient(self.root)
        turno_win.grab_set()
        self.root.wait_window(turno_win)

    def registrar_enfermero(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Registrar Enfermero", font=("Arial", 14)).pack(pady=10)

        nombre = simpledialog.askstring("Enfermero", "Nombre del enfermero(a):")
        if nombre:
            self.enfermero = Enfermero(nombre)
            messagebox.showinfo("Éxito", "Enfermero registrado correctamente.")

    def seccion_pacientes(self):
        self.limpiar_area()

        frame_botones = tk.Frame(self.area_dinamica, bg="white")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Registrar Paciente", command=self.agregar_paciente).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Dar de Alta", command=self.eliminar_paciente).pack(side="left", padx=5)

        self.label_camillas = tk.Label(self.area_dinamica, text=self.get_camillas_libres(), bg="white")
        self.label_camillas.pack(pady=10)

        self.tree = ttk.Treeview(self.area_dinamica,
                                 columns=("Nombre", "Edad", "Género", "Camilla", "Piso", "Entrada"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

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
        hora_entrada = datetime.now().strftime("%H:%M:%S")

        camilla = self.camillas_disponibles.pop(0)
        paciente = Paciente(nombre, edad, genero, camilla, piso, hora_entrada)
        self.pacientes.append(paciente)

        self.tree.insert("", "end",
                         values=(paciente.nombre, paciente.edad, paciente.genero, paciente.camilla,
                                 paciente.piso, paciente.hora_entrada))
        self.actualizar_camillas_libres()

    def eliminar_paciente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showinfo("Dar de Alta", "Selecciona un paciente para dar de alta.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Deseas dar de alta al paciente seleccionado?")
        if respuesta:
            item = seleccionado[0]
            valores = self.tree.item(item, "values")
            camilla = int(valores[3])
            self.camillas_disponibles.append(camilla)
            self.camillas_disponibles.sort()
            self.tree.delete(item)

            for p in self.pacientes:
                if p.camilla == camilla:
                    p.hora_salida = datetime.now().strftime("%H:%M:%S")
                    self.historial.append(p)
                    self.pacientes.remove(p)
                    break

            self.actualizar_camillas_libres()

    def ver_historial(self):
        self.limpiar_area()
        tk.Label(self.area_dinamica, text="Historial de Pacientes", font=("Arial", 14)).pack(pady=10)

        tree_historial = ttk.Treeview(self.area_dinamica,
                                      columns=("Nombre", "Edad", "Género", "Piso", "Entrada", "Salida"),
                                      show="headings")
        for col in tree_historial["columns"]:
            tree_historial.heading(col, text=col)
        tree_historial.pack(expand=True, fill="both", padx=10, pady=10)

        for p in self.historial:
            tree_historial.insert("", "end",
                                  values=(p.nombre, p.edad, p.genero, p.piso, p.hora_entrada, p.hora_salida))


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
