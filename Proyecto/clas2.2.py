
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
        self.root.title("Gestión de Pacientes")
        self.pacientes = []
        self.camillas_disponibles = list(range(1, 10))

        self.obtener_datos_personal()
        self.setup_ui()

    def obtener_datos_personal(self):
        self.root.withdraw()

        nombre_doctor = simpledialog.askstring("Doctor", "Nombre del doctor:")
        especialidad = simpledialog.askstring("Doctor", "Especialidad:")
        edad_doctor = simpledialog.askinteger("Doctor", "Edad del doctor:")
        turno = simpledialog.askstring("Doctor", "Turno (Matutino/Vespertino/Nocturno):")
        self.doctor = Doctor(nombre_doctor, especialidad, edad_doctor, turno)

        nombre_enfermero = simpledialog.askstring("Enfermero", "Nombre del enfermero(a):")
        self.enfermero = Enfermero(nombre_enfermero)

        self.root.deiconify()

    def setup_ui(self):
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_agregar_paciente = tk.Button(left_frame, text="Llamar Paciente", command=self.agregar_paciente)
        self.btn_agregar_paciente.pack()

        self.btn_eliminar_paciente = tk.Button(left_frame, text="Eliminar Paciente", command=self.eliminar_paciente)
        self.btn_eliminar_paciente.pack(pady=5)

        self.label_camillas = tk.Label(left_frame, text=self.get_camillas_libres())
        self.label_camillas.pack(pady=10)

        self.tree = ttk.Treeview(
            self.root,
            columns=("Nombre", "Edad", "Género", "Camilla", "Piso", "Doctor", "Enfermero"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(side=tk.RIGHT, padx=10, pady=10)

    def get_camillas_libres(self):
        return f"Camillas libres: {', '.join(str(c) for c in self.camillas_disponibles)}"

    def actualizar_camillas_libres(self):
        self.label_camillas.config(text=self.get_camillas_libres())

    def convertir_genero(self, genero):
        genero = genero.strip().upper()
        if genero == "M":
            return "Masculino"
        elif genero == "F":
            return "Femenino"
        else:
            return "Otro"

    def agregar_paciente(self):
        if not self.camillas_disponibles:
            messagebox.showwarning("Sin camillas", "Todas las camillas están ocupadas.")
            return

        nombre = simpledialog.askstring("Paciente", "Nombre del paciente:")
        edad = simpledialog.askinteger("Paciente", "Edad del paciente:")
        genero_input = simpledialog.askstring("Paciente", "Género del paciente (Masculino7Femenino):")
        genero = self.convertir_genero(genero_input)
        piso = simpledialog.askstring("Paciente", "¿En qué piso estará?")

        camilla = self.camillas_disponibles.pop(0)
        paciente = Paciente(
            nombre,
            edad,
            genero,
            camilla,
            piso,
            self.doctor.nombre,
            self.enfermero.nombre
        )
        self.pacientes.append(paciente)

        self.tree.insert(
            "",
            "end",
            values=(
                paciente.nombre,
                paciente.edad,
                paciente.genero,
                paciente.camilla,
                paciente.piso,
                paciente.doctor,
                paciente.enfermero
            )
        )
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
