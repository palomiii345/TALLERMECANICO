import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Clientes(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent, bg="#1C2833")
        self.main_app = main_app
        self.pack(fill="both", expand=True)

        # --- Conexión con la base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_clientes()

        # --- Título principal ---
        tk.Label(self, text="REGISTRO DE CLIENTES",
                 font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C").pack(pady=15)

        # --- Marco principal ---
        frame = tk.Frame(self, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Variables ---
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.telefono = tk.StringVar()
        self.correo = tk.StringVar()
        self.direccion = tk.StringVar()

        # --- Campos de texto ---
        tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.nombre, font=("Arial", 12), width=25).grid(row=0, column=1, padx=10, pady=8)

        tk.Label(frame, text="Apellido:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.apellido, font=("Arial", 12), width=25).grid(row=0, column=3, padx=10, pady=8)

        tk.Label(frame, text="Teléfono:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.telefono, font=("Arial", 12), width=25).grid(row=1, column=1, padx=10, pady=8)

        tk.Label(frame, text="Correo:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=1, column=2, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.correo, font=("Arial", 12), width=25).grid(row=1, column=3, padx=10, pady=8)

        tk.Label(frame, text="Dirección:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.direccion, font=("Arial", 12), width=60).grid(row=2, column=1, columnspan=3, padx=10, pady=8)

        # --- Botones de acción ---
        boton_frame = tk.Frame(frame, bg="#212F3D")
        boton_frame.grid(row=3, column=0, columnspan=4, pady=10)

        botones = [
            ("Guardar", self.guardar_cliente),
            ("Actualizar", self.actualizar_cliente),
            ("Eliminar", self.eliminar_cliente),
            ("Limpiar", self.limpiar_campos),
            ("Volver al Menú", self.volver_menu)
        ]

        for texto, comando in botones:
            tk.Button(boton_frame, text=texto, font=("Arial", 12, "bold"),
                      bg="#1ABC9C", fg="white", width=12, command=comando,
                      cursor="hand2").pack(side="left", padx=10)

        # --- Tabla de clientes ---
        columnas = ("ID", "Nombre", "Apellido", "Teléfono", "Correo", "Dirección")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=130 if col != "Dirección" else 200)

        self.tabla.grid(row=4, column=0, columnspan=4, pady=15, padx=10)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_cliente)

        self.cargar_clientes()

    # ---------------------- BASE DE DATOS ----------------------
    def crear_tabla_clientes(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            correo TEXT,
            direccion TEXT
        )
        """)
        self.conexion.commit()

    def guardar_cliente(self):
        if not self.nombre.get() or not self.apellido.get():
            messagebox.showwarning("Campos vacíos", "El nombre y apellido son obligatorios")
            return
        self.cursor.execute("INSERT INTO clientes (nombre, apellido, telefono, correo, direccion) VALUES (?, ?, ?, ?, ?)",
                            (self.nombre.get(), self.apellido.get(), self.telefono.get(), self.correo.get(), self.direccion.get()))
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        self.cargar_clientes()
        self.limpiar_campos()

    def cargar_clientes(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.cursor.execute("SELECT * FROM clientes")
        for cliente in self.cursor.fetchall():
            self.tabla.insert("", "end", values=cliente)

    def seleccionar_cliente(self, event):
        fila = self.tabla.focus()
        if fila:
            datos = self.tabla.item(fila)["values"]
            self.nombre.set(datos[1])
            self.apellido.set(datos[2])
            self.telefono.set(datos[3])
            self.correo.set(datos[4])
            self.direccion.set(datos[5])

    def actualizar_cliente(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona un cliente", "Debes seleccionar un cliente de la tabla")
            return
        id_cliente = self.tabla.item(fila)["values"][0]
        self.cursor.execute("""
        UPDATE clientes SET nombre=?, apellido=?, telefono=?, correo=?, direccion=?
        WHERE id=?
        """, (self.nombre.get(), self.apellido.get(), self.telefono.get(), self.correo.get(), self.direccion.get(), id_cliente))
        self.conexion.commit()
        messagebox.showinfo("Actualizado", "Cliente actualizado correctamente")
        self.cargar_clientes()
        self.limpiar_campos()

    def eliminar_cliente(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona un cliente", "Debes seleccionar un cliente de la tabla")
            return
        id_cliente = self.tabla.item(fila)["values"][0]
        confirm = messagebox.askyesno("Eliminar", "¿Deseas eliminar este cliente?")
        if confirm:
            self.cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
            self.conexion.commit()
            messagebox.showinfo("Eliminado", "Cliente eliminado correctamente")
            self.cargar_clientes()
            self.limpiar_campos()

    def limpiar_campos(self):
        self.nombre.set("")
        self.apellido.set("")
        self.telefono.set("")
        self.correo.set("")
        self.direccion.set("")
        self.tabla.selection_remove(self.tabla.focus())

    def volver_menu(self):
        self.main_app.cambiar_pantalla("menu")
