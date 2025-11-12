import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Vehiculos(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.pack(fill="both", expand=True)
        self.config(bg="#1C2833")

        # --- Conexión a la base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_vehiculos()

        # --- Título ---
        tk.Label(self, text="GESTIÓN DE VEHÍCULOS", font=("Arial", 18, "bold"),
                 bg="#1C2833", fg="#1ABC9C").pack(pady=15)

        # --- Marco del formulario ---
        frame_form = tk.Frame(self, bg="#212F3D", bd=2, relief="ridge")
        frame_form.pack(padx=20, pady=10, fill="x")

        # --- Campos del formulario ---
        etiquetas = ["Cliente:", "Marca:", "Modelo:", "Año:", "Placas:"]
        for i, texto in enumerate(etiquetas):
            tk.Label(frame_form, text=texto, bg="#212F3D", fg="white",
                     font=("Arial", 12, "bold")).grid(row=i, column=0, padx=10, pady=8, sticky="w")

        # --- Combobox de clientes ---
        self.cliente_cb = ttk.Combobox(frame_form, width=28, state="readonly", font=("Arial", 11))
        self.cliente_cb.grid(row=0, column=1, padx=10, pady=8)
        self.cargar_clientes()

        # --- Entradas ---
        self.marca_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.marca_entry.grid(row=1, column=1, padx=10, pady=8)

        self.modelo_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.modelo_entry.grid(row=2, column=1, padx=10, pady=8)

        self.anio_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.anio_entry.grid(row=3, column=1, padx=10, pady=8)

        self.placas_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.placas_entry.grid(row=4, column=1, padx=10, pady=8)

        # --- Botones ---
        boton_frame = tk.Frame(frame_form, bg="#212F3D")
        boton_frame.grid(row=5, column=0, columnspan=2, pady=10)

        botones = [
            ("Registrar", self.registrar_vehiculo, "#1ABC9C"),
            ("Eliminar", self.eliminar_vehiculo, "#922B21"),
            ("Actualizar Lista", self.mostrar_vehiculos, "#117A65")
        ]

        for texto, comando, color in botones:
            tk.Button(boton_frame, text=texto, command=comando,
                      bg=color, fg="white", font=("Arial", 12, "bold"),
                      width=16, cursor="hand2").pack(side="left", padx=10)

        # --- Tabla de vehículos ---
        tabla_frame = tk.Frame(self, bg="#1C2833")
        tabla_frame.pack(padx=20, pady=15, fill="both", expand=True)

        self.tabla = ttk.Treeview(tabla_frame, columns=("ID", "Cliente", "Marca", "Modelo", "Año", "Placas"),
                                  show="headings", height=12)
        self.tabla.pack(fill="both", expand=True)

        for col in ("ID", "Cliente", "Marca", "Modelo", "Año", "Placas"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120 if col != "ID" else 50)

        self.mostrar_vehiculos()

    # --- Funciones de base de datos ---
    def crear_tabla_vehiculos(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                marca TEXT,
                modelo TEXT,
                anio TEXT,
                placas TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id)
            )
        ''')
        self.conexion.commit()

    def cargar_clientes(self):
        self.cursor.execute("SELECT id, nombre FROM clientes")
        clientes = self.cursor.fetchall()
        self.lista_clientes = {nombre: id_cliente for id_cliente, nombre in clientes}
        self.cliente_cb["values"] = list(self.lista_clientes.keys())

    def registrar_vehiculo(self):
        cliente_nombre = self.cliente_cb.get()
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        anio = self.anio_entry.get()
        placas = self.placas_entry.get()

        if not cliente_nombre or not marca or not modelo or not placas:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios")
            return

        id_cliente = self.lista_clientes.get(cliente_nombre)
        self.cursor.execute("INSERT INTO vehiculos (id_cliente, marca, modelo, anio, placas) VALUES (?, ?, ?, ?, ?)",
                            (id_cliente, marca, modelo, anio, placas))
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Vehículo registrado correctamente")
        self.limpiar_campos()
        self.mostrar_vehiculos()

    def mostrar_vehiculos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        self.cursor.execute("""
            SELECT v.id, c.nombre, v.marca, v.modelo, v.anio, v.placas
            FROM vehiculos v
            JOIN clientes c ON v.id_cliente = c.id
        """)
        for fila in self.cursor.fetchall():
            self.tabla.insert("", "end", values=fila)

    def eliminar_vehiculo(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un vehículo para eliminar")
            return

        id_vehiculo = self.tabla.item(seleccionado, "values")[0]
        confirmar = messagebox.askyesno("Eliminar", "¿Deseas eliminar este vehículo?")
        if confirmar:
            self.cursor.execute("DELETE FROM vehiculos WHERE id=?", (id_vehiculo,))
            self.conexion.commit()
            self.mostrar_vehiculos()

    def limpiar_campos(self):
        self.marca_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.anio_entry.delete(0, tk.END)
        self.placas_entry.delete(0, tk.END)
        self.cliente_cb.set("")
