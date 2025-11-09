import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario - Taller Mecánico")
        self.root.geometry("950x600")
        self.root.config(bg="#1C2833")
        self.root.resizable(False, False)

        # --- Conexión con la base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_inventario()

        # --- Título principal ---
        tk.Label(self.root, text="GESTIÓN DE INVENTARIO",
                 font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C").pack(pady=15)

        # --- Marco principal ---
        frame = tk.Frame(self.root, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Variables ---
        self.nombre = tk.StringVar()
        self.categoria = tk.StringVar()
        self.precio = tk.DoubleVar()
        self.stock = tk.IntVar()
        self.descripcion = tk.StringVar()

        # --- Campos de texto ---
        tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.nombre, font=("Arial", 12), width=25).grid(row=0, column=1, padx=10, pady=8)

        tk.Label(frame, text="Categoría:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.categoria, font=("Arial", 12), width=25).grid(row=0, column=3, padx=10, pady=8)

        tk.Label(frame, text="Precio ($):", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.precio, font=("Arial", 12), width=25).grid(row=1, column=1, padx=10, pady=8)

        tk.Label(frame, text="Stock:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=1, column=2, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.stock, font=("Arial", 12), width=25).grid(row=1, column=3, padx=10, pady=8)

        tk.Label(frame, text="Descripción:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.descripcion, font=("Arial", 12), width=60).grid(row=2, column=1, columnspan=3, padx=10, pady=8)

        # --- Botones ---
        boton_frame = tk.Frame(frame, bg="#212F3D")
        boton_frame.grid(row=3, column=0, columnspan=4, pady=10)

        botones = [
            ("Guardar", self.guardar_producto),
            ("Actualizar", self.actualizar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar", self.limpiar_campos),
            ("Regresar", self.volver_menu)
        ]

        for texto, comando in botones:
            tk.Button(boton_frame, text=texto, font=("Arial", 12, "bold"),
                      bg="#1ABC9C", fg="white", width=12, command=comando,
                      cursor="hand2").pack(side="left", padx=10)

        # --- Tabla de productos ---
        columnas = ("ID", "Nombre", "Categoría", "Precio", "Stock", "Descripción")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120 if col != "Descripción" else 200)
        self.tabla.grid(row=4, column=0, columnspan=4, pady=15, padx=10)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_producto)

        self.cargar_productos()

    # ---------------------- BASE DE DATOS ----------------------
    def crear_tabla_inventario(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL,
            stock INTEGER,
            descripcion TEXT
        )
        """)
        self.conexion.commit()

    def guardar_producto(self):
        if not self.nombre.get():
            messagebox.showwarning("Campos vacíos", "El nombre del producto es obligatorio")
            return
        self.cursor.execute("""
        INSERT INTO inventario (nombre, categoria, precio, stock, descripcion)
        VALUES (?, ?, ?, ?, ?)
        """, (self.nombre.get(), self.categoria.get(), self.precio.get(), self.stock.get(), self.descripcion.get()))
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        self.cargar_productos()
        self.limpiar_campos()

    def cargar_productos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.cursor.execute("SELECT * FROM inventario")
        for producto in self.cursor.fetchall():
            self.tabla.insert("", "end", values=producto)

    def seleccionar_producto(self, event):
        fila = self.tabla.focus()
        if fila:
            datos = self.tabla.item(fila)["values"]
            self.nombre.set(datos[1])
            self.categoria.set(datos[2])
            self.precio.set(datos[3])
            self.stock.set(datos[4])
            self.descripcion.set(datos[5])

    def actualizar_producto(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla")
            return
        id_producto = self.tabla.item(fila)["values"][0]
        self.cursor.execute("""
        UPDATE inventario SET nombre=?, categoria=?, precio=?, stock=?, descripcion=?
        WHERE id=?
        """, (self.nombre.get(), self.categoria.get(), self.precio.get(), self.stock.get(), self.descripcion.get(), id_producto))
        self.conexion.commit()
        messagebox.showinfo("Actualizado", "Producto actualizado correctamente")
        self.cargar_productos()
        self.limpiar_campos()

    def eliminar_producto(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla")
            return
        id_producto = self.tabla.item(fila)["values"][0]
        confirm = messagebox.askyesno("Eliminar", "¿Deseas eliminar este producto?")
        if confirm:
            self.cursor.execute("DELETE FROM inventario WHERE id=?", (id_producto,))
            self.conexion.commit()
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente")
            self.cargar_productos()
            self.limpiar_campos()

    def limpiar_campos(self):
        self.nombre.set("")
        self.categoria.set("")
        self.precio.set(0)
        self.stock.set(0)
        self.descripcion.set("")
        self.tabla.selection_remove(self.tabla.focus())

    def volver_menu(self):
        self.root.destroy()
        from menu_principal import MenuPrincipal
        nuevo_root = tk.Tk()
        MenuPrincipal(nuevo_root)
        nuevo_root.mainloop()


# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    root = tk.Tk()
    Inventario(root)
    root.mainloop()

