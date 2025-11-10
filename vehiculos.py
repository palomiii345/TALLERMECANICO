import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Vehiculos(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.pack(fill="both", expand=True)

        # --- Conexión a la base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_vehiculos()

        # --- Título ---
        tk.Label(self, text="Registro de Vehículos", font=("Arial", 18, "bold"),
                 bg="#17202A", fg="#1ABC9C").pack(pady=10)

        # --- Marco del formulario ---
        frame_form = tk.Frame(self, bg="#1C2833", bd=2, relief="ridge")
        frame_form.pack(padx=10, pady=10, fill="x")

        # --- Campos del formulario ---
        tk.Label(frame_form, text="Cliente:", bg="#1C2833", fg="white", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.cliente_cb = ttk.Combobox(frame_form, width=27, state="readonly", font=("Arial", 11))
        self.cliente_cb.grid(row=0, column=1, padx=10, pady=5)
        self.cargar_clientes()

        tk.Label(frame_form, text="Marca:", bg="#1C2833", fg="white", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.marca_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.marca_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Modelo:", bg="#1C2833", fg="white", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.modelo_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.modelo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Año:", bg="#1C2833", fg="white", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.anio_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.anio_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Placas:", bg="#1C2833", fg="white", font=("Arial", 11)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.placas_entry = tk.Entry(frame_form, font=("Arial", 11), width=30)
        self.placas_entry.grid(row=4, column=1, padx=10, pady=5)

        # --- Botones ---
        tk.Button(frame_form, text="Registrar", bg="#1ABC9C", fg="white", font=("Arial", 11, "bold"),
                  command=self.registrar_vehiculo).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(frame_form, text="Eliminar", bg="#E74C3C", fg="white", font=("Arial", 11, "bold"),
                  command=self.eliminar_vehiculo).grid(row=5, column=1, padx=10, pady=10)
        tk.Button(frame_form, text="Actualizar lista", bg="#5DADE2", fg="white", font=("Arial", 11, "bold"),
                  command=self.mostrar_vehiculos).grid(row=5, column=2, padx=10, pady=10)

        # --- Tabla de vehículos ---
        self.tabla = ttk.Treeview(self, columns=("ID", "Cliente", "Marca", "Modelo", "Año", "Placas"), show="headings", height=10)
        self.tabla.pack(padx=15, pady=10, fill="x")

        for col in ("ID", "Cliente", "Marca", "Modelo", "Año", "Placas"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)
        self.tabla.column("ID", width=50)
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
