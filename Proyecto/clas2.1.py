import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Doctor:
    def __init__(self, nombre, especialidad, edad, turno):
        self.nombre = nombre
        self.especialidad = especialidad
        self.edad = edad
        self.turno = turno

class Paciente:
    def __init__(self, nombre, edad, genero, camilla):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.camilla = camilla

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pacientes")
        self.pacientes = []
        self.camillas_disponibles = list(range(1, 10))

        self.obtener_datos_doctor()

        self.setup_ui()

    def obtener_datos_doctor(self):
        self.root.withdraw()

        nombre = simpledialog.askstring("Doctor", "Nombre del doctor:")
        especialidad = simpledialog.askstring("Doctor", "Especialidad:")
        edad = simpledialog.askinteger("Doctor", "Edad del doctor:")
        turno = simpledialog.askstring("Doctor", "Turno (Matutino/Vespertino/Nocturno):")

        self.doctor = Doctor(nombre, especialidad, edad, turno)

        self.root.deiconify()

    def setup_ui(self):
        # Marco izquierdo con botón
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_agregar_paciente = tk.Button(left_frame, text="Llamar Paciente", command=self.agregar_paciente)
        self.btn_agregar_paciente.pack()

        self.btn_eliminar_paciente = tk.Button(left_frame, text="Eliminar Paciente", command=self.eliminar_paciente)
        self.btn_eliminar_paciente.pack(pady=5)

        # Tabla
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Edad", "Género", "Camilla"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Camilla", text="Camilla")
        self.tree.pack(side=tk.RIGHT, padx=10, pady=10)

    def agregar_paciente(self):
        if not self.camillas_disponibles:
            messagebox.showwarning("Sin camillas", "Todas las camillas están ocupadas.")
            return

        nombre = simpledialog.askstring("Paciente", "Nombre del paciente:")
        edad = simpledialog.askinteger("Paciente", "Edad del paciente:")
        genero = simpledialog.askstring("Paciente", "Género del paciente (Masculino/Femenino):")

        camilla = self.camillas_disponibles.pop(0)
        paciente = Paciente(nombre, edad, genero, camilla)
        self.pacientes.append(paciente)

        self.tree.insert("", "end", values=(paciente.nombre, paciente.edad, paciente.genero, paciente.camilla))

    def eliminar_paciente(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showinfo("Eliminar", "Selecciona un paciente para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar al paciente?")
        if respuesta:
            item = seleccionado[0]
            valores = self.tree.item(item, "values")
            camilla = int(valores[3])
            self.camillas_disponibles.append(camilla)
            self.camillas_disponibles.sort()

            self.tree.delete(item)
            # Remover también de la lista interna
            self.pacientes = [p for p in self.pacientes if p.camilla != camilla]

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
