import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Reportes(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.pack(fill="both", expand=True)
        self.config(bg="#1C2833")

        # --- Título ---
        titulo = tk.Label(self, text="REPORTE GENERAL DEL TALLER",
                          font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C")
        titulo.pack(pady=15)

        # --- Frame principal ---
        frame = tk.Frame(self, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Botones de acciones ---
        botones = [
            ("Reporte de Ventas", self.reporte_ventas, "#1ABC9C"),
            ("Servicios Realizados", self.reporte_servicios, "#117A65"),
            ("Piezas Más Usadas", self.reporte_inventario, "#884EA0")
        ]
        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(frame, text=texto, command=comando,
                      bg=color, fg="white", font=("Arial", 12, "bold"), width=20).grid(row=0, column=i, padx=15, pady=15)

        # --- Tabla para mostrar resultados ---
        self.tabla = ttk.Treeview(frame, columns=("col1", "col2", "col3"), show="headings", height=15)
        self.tabla.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        for col, ancho in zip(("col1", "col2", "col3"), (250, 250, 250)):
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=ancho)

    # --- Función: limpiar tabla ---
    def limpiar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    # --- Reporte de Ventas ---
    def reporte_ventas(self):
        self.limpiar_tabla()
        try:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(total) FROM facturas")
            datos = cursor.fetchone()
            total_facturas = datos[0] if datos[0] else 0
            total_ventas = datos[1] if datos[1] else 0.0
            self.tabla.heading("col1", text="Tipo de Dato")
            self.tabla.heading("col2", text="Cantidad")
            self.tabla.heading("col3", text="Total ($)")
            self.tabla.insert("", "end", values=("Facturas Registradas", total_facturas, f"{total_ventas:.2f}"))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

    # --- Reporte de Servicios ---
    def reporte_servicios(self):
        self.limpiar_tabla()
        try:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("SELECT servicio, COUNT(*) FROM ordenes_servicio GROUP BY servicio")
            resultados = cursor.fetchall()
            self.tabla.heading("col1", text="Servicio")
            self.tabla.heading("col2", text="Veces Realizado")
            self.tabla.heading("col3", text="")
            if resultados:
                for fila in resultados:
                    self.tabla.insert("", "end", values=(fila[0], fila[1], ""))
            else:
                self.tabla.insert("", "end", values=("Sin datos", "", ""))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

    # --- Reporte de Inventario (piezas más usadas) ---
    def reporte_inventario(self):
        self.limpiar_tabla()
        try:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, cantidad FROM inventario ORDER BY cantidad ASC LIMIT 10")
            resultados = cursor.fetchall()
            self.tabla.heading("col1", text="Pieza / Refacción")
            self.tabla.heading("col2", text="Existencia Actual")
            self.tabla.heading("col3", text="")
            if resultados:
                for fila in resultados:
                    self.tabla.insert("", "end", values=fila)
            else:
                self.tabla.insert("", "end", values=("Sin datos", "", ""))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")
