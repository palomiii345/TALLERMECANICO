import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class OrdenesServicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Órdenes de Servicio - Taller Mecánico")
        self.root.geometry("1000x650")
        self.root.config(bg="#1C2833")
        self.root.resizable(False, False)

        # --- Conexión con base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_ordenes()

        # --- Título principal ---
        tk.Label(self.root, text="GESTIÓN DE ÓRDENES DE SERVICIO",
                 font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C").pack(pady=15)

        # --- Marco principal ---
        frame = tk.Frame(self.root, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Variables ---
        self.id_cliente = tk.StringVar()
        self.id_vehiculo = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.piezas_usadas = tk.StringVar()
        self.costo = tk.DoubleVar()
        self.estado = tk.StringVar(value="Pendiente")

        # --- Campos de texto y combos ---
        tk.Label(frame, text="Cliente (ID):", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.id_cliente, font=("Arial", 12), width=25).grid(row=0, column=1, padx=10, pady=8)

        tk.Label(frame, text="Vehículo (ID):", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.id_vehiculo, font=("Arial", 12), width=25).grid(row=0, column=3, padx=10, pady=8)

        tk.Label(frame, text="Descripción del trabajo:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.descripcion, font=("Arial", 12), width=60).grid(row=1, column=1, columnspan=3, padx=10, pady=8)

        tk.Label(frame, text="Piezas usadas:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.piezas_usadas, font=("Arial", 12), width=60).grid(row=2, column=1, columnspan=3, padx=10, pady=8)

        tk.Label(frame, text="Costo total ($):", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        tk.Entry(frame, textvariable=self.costo, font=("Arial", 12), width=25).grid(row=3, column=1, padx=10, pady=8)

        tk.Label(frame, text="Estado:", font=("Arial", 12), bg="#212F3D", fg="white").grid(row=3, column=2, padx=10, pady=8, sticky="w")
        estado_combo = ttk.Combobox(frame, textvariable=self.estado, font=("Arial", 12), width=23, state="readonly",
                                    values=["Pendiente", "En proceso", "Completado"])
        estado_combo.grid(row=3, column=3, padx=10, pady=8)

        # --- Botones ---
        boton_frame = tk.Frame(frame, bg="#212F3D")
        boton_frame.grid(row=4, column=0, columnspan=4, pady=10)

        botones = [
            ("Guardar", self.guardar_orden),
            ("Actualizar", self.actualizar_orden),
            ("Eliminar", self.eliminar_orden),
            ("Limpiar", self.limpiar_campos),
            ("Regresar", self.volver_menu)
        ]

        for texto, comando in botones:
            tk.Button(boton_frame, text=texto, font=("Arial", 12, "bold"),
                      bg="#1ABC9C", fg="white", width=12, command=comando,
                      cursor="hand2").pack(side="left", padx=10)

        # --- Tabla de órdenes ---
        columnas = ("ID", "Cliente", "Vehículo", "Descripción", "Piezas", "Costo", "Estado")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=130 if col != "Descripción" else 200)
        self.tabla.grid(row=5, column=0, columnspan=4, pady=15, padx=10)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_orden)

        self.cargar_ordenes()

    # ---------------------- BASE DE DATOS ----------------------
    def crear_tabla_ordenes(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes_servicio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            id_vehiculo INTEGER,
            descripcion TEXT,
            piezas_usadas TEXT,
            costo REAL,
            estado TEXT
        )
        """)
        self.conexion.commit()

    def guardar_orden(self):
        if not self.id_cliente.get() or not self.descripcion.get():
            messagebox.showwarning("Campos obligatorios", "Debe ingresar al menos el cliente y la descripción")
            return
        self.cursor.execute("""
        INSERT INTO ordenes_servicio (id_cliente, id_vehiculo, descripcion, piezas_usadas, costo, estado)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (self.id_cliente.get(), self.id_vehiculo.get(), self.descripcion.get(),
              self.piezas_usadas.get(), self.costo.get(), self.estado.get()))
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Orden registrada correctamente")
        self.cargar_ordenes()
        self.limpiar_campos()

    def cargar_ordenes(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.cursor.execute("SELECT * FROM ordenes_servicio")
        for orden in self.cursor.fetchall():
            self.tabla.insert("", "end", values=orden)

    def seleccionar_orden(self, event):
        fila = self.tabla.focus()
        if fila:
            datos = self.tabla.item(fila)["values"]
            self.id_cliente.set(datos[1])
            self.id_vehiculo.set(datos[2])
            self.descripcion.set(datos[3])
            self.piezas_usadas.set(datos[4])
            self.costo.set(datos[5])
            self.estado.set(datos[6])

    def actualizar_orden(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona una orden", "Debes seleccionar una orden de la tabla")
            return
        id_orden = self.tabla.item(fila)["values"][0]
        self.cursor.execute("""
        UPDATE ordenes_servicio
        SET id_cliente=?, id_vehiculo=?, descripcion=?, piezas_usadas=?, costo=?, estado=?
        WHERE id=?
        """, (self.id_cliente.get(), self.id_vehiculo.get(), self.descripcion.get(),
              self.piezas_usadas.get(), self.costo.get(), self.estado.get(), id_orden))
        self.conexion.commit()
        messagebox.showinfo("Actualizado", "Orden actualizada correctamente")
        self.cargar_ordenes()
        self.limpiar_campos()

    def eliminar_orden(self):
        fila = self.tabla.focus()
        if not fila:
            messagebox.showwarning("Selecciona una orden", "Debes seleccionar una orden de la tabla")
            return
        id_orden = self.tabla.item(fila)["values"][0]
        confirm = messagebox.askyesno("Eliminar", "¿Deseas eliminar esta orden?")
        if confirm:
            self.cursor.execute("DELETE FROM ordenes_servicio WHERE id=?", (id_orden,))
            self.conexion.commit()
            messagebox.showinfo("Eliminado", "Orden eliminada correctamente")
            self.cargar_ordenes()
            self.limpiar_campos()

    def limpiar_campos(self):
        self.id_cliente.set("")
        self.id_vehiculo.set("")
        self.descripcion.set("")
        self.piezas_usadas.set("")
        self.costo.set(0)
        self.estado.set("Pendiente")
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
    OrdenesServicio(root)
    root.mainloop()
