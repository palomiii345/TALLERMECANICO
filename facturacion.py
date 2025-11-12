import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class Facturacion(tk.Frame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent, bg="#1C2833")
        self.main_app = main_app

        # --- COLORES GLOBALES ---
        color_fondo = "#1C2833"
        color_secundario = "#212F3D"
        color_boton = "#1ABC9C"
        color_texto = "white"

        # --- TÍTULO ---
        tk.Label(self, text="FACTURACIÓN DE SERVICIOS",
                 font=("Arial", 18, "bold"),
                 bg=color_fondo, fg=color_boton).pack(pady=15)

        # --- FRAME PRINCIPAL ---
        frame = tk.Frame(self, bg=color_secundario, bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- VARIABLES ---
        self.id_orden = tk.StringVar()
        self.cliente = tk.StringVar()
        self.total = tk.StringVar()
        self.metodo_pago = tk.StringVar(value="Efectivo")

        # --- CONEXIÓN A BD ---
        self.crear_tabla()

        # --- FORMULARIO ---
        campos = [
            ("ID Orden:", self.id_orden),
            ("Cliente:", self.cliente),
            ("Total a Pagar ($):", self.total)
        ]

        for i, (texto, var) in enumerate(campos):
            tk.Label(frame, text=texto, font=("Arial", 12, "bold"),
                     bg=color_secundario, fg=color_texto).grid(row=i, column=0, padx=10, pady=10, sticky="w")
            tk.Entry(frame, textvariable=var, font=("Arial", 12),
                     width=30, bg="#566573", fg="white",
                     insertbackground="white", relief="flat").grid(row=i, column=1, padx=10, pady=10)

        # --- MÉTODO DE PAGO ---
        tk.Label(frame, text="Método de Pago:", font=("Arial", 12, "bold"),
                 bg=color_secundario, fg=color_texto).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        combo_metodo = ttk.Combobox(frame, textvariable=self.metodo_pago,
                                    values=["Efectivo", "Tarjeta", "Transferencia"],
                                    state="readonly", width=28)
        combo_metodo.grid(row=3, column=1, padx=10, pady=10)
        combo_metodo.current(0)

        # --- BOTONES ---
        boton_frame = tk.Frame(frame, bg=color_secundario)
        boton_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(boton_frame, text="Registrar Factura", command=self.registrar_factura,
                  bg=color_boton, fg="white", font=("Arial", 12, "bold"),
                  width=18, cursor="hand2", relief="flat").pack(side="left", padx=10)

        tk.Button(boton_frame, text="Mostrar Facturas", command=self.mostrar_facturas,
                  bg="#117A65", fg="white", font=("Arial", 12, "bold"),
                  width=18, cursor="hand2", relief="flat").pack(side="left", padx=10)

        tk.Button(boton_frame, text="🖨️ Imprimir Factura", command=self.imprimir_factura,
                  bg="#F39C12", fg="white", font=("Arial", 12, "bold"),
                  width=18, cursor="hand2", relief="flat").pack(side="left", padx=10)

        # --- TABLA ---
        columnas = ("id", "orden", "cliente", "total", "pago")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=20, pady=15, sticky="nsew")

        for col, texto in zip(columnas, ["ID", "ID Orden", "Cliente", "Total ($)", "Método de Pago"]):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=150, anchor="center")

        # --- ESTILO TREEVIEW OSCURO ---
        estilo = ttk.Style()
        estilo.configure("Treeview",
                         background=color_fondo,
                         foreground="white",
                         rowheight=25,
                         fieldbackground=color_fondo,
                         font=("Arial", 10))
        estilo.configure("Treeview.Heading",
                         background=color_boton,
                         foreground=color_fondo,
                         font=("Arial", 11, "bold"))
        estilo.map("Treeview",
                   background=[("selected", "#117A65")])

        # --- CARGAR DATOS ---
        self.mostrar_facturas()

        # Expandir filas/columnas
        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)

    # ---------------- FUNCIONES BD ----------------
    def crear_tabla(self):
        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_orden TEXT,
                cliente TEXT,
                total REAL,
                metodo_pago TEXT
            )
        """)
        conn.commit()
        conn.close()

    def registrar_factura(self):
        if not self.id_orden.get() or not self.cliente.get() or not self.total.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO facturas (id_orden, cliente, total, metodo_pago)
                VALUES (?, ?, ?, ?)
            """, (self.id_orden.get(), self.cliente.get(), float(self.total.get()), self.metodo_pago.get()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Factura registrada correctamente")
            self.mostrar_facturas()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la factura: {e}")

    def mostrar_facturas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas")
        for fila in cursor.fetchall():
            self.tabla.insert("", "end", values=fila)
        conn.close()

    def limpiar_campos(self):
        self.id_orden.set("")
        self.cliente.set("")
        self.total.set("")
        self.metodo_pago.set("Efectivo")

    # ---------------- BOTÓN IMPRIMIR ----------------
    def imprimir_factura(self):
        """Abre ventana con los datos de la factura seleccionada."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una factura de la tabla")
            return

        datos = self.tabla.item(seleccion)["values"]

        ventana_impresion = tk.Toplevel(self)
        ventana_impresion.title(f"Factura ID {datos[0]}")
        ventana_impresion.geometry("400x300")
        ventana_impresion.config(bg="#F2F4F4")

        tk.Label(ventana_impresion, text="FACTURA DE SERVICIO", font=("Arial", 16, "bold"),
                 bg="#F2F4F4").pack(pady=10)

        etiquetas = ["ID Factura:", "ID Orden:", "Cliente:", "Total ($):", "Método de Pago:"]
        for etiqueta, valor in zip(etiquetas, datos):
            tk.Label(ventana_impresion, text=f"{etiqueta} {valor}", font=("Arial", 12),
                     bg="#F2F4F4").pack(anchor="w", padx=20, pady=5)

        # Botón simulado de imprimir
        tk.Button(ventana_impresion, text="Imprimir", font=("Arial", 12, "bold"),
                  bg="#117A65", fg="white", width=15,
                  command=lambda: messagebox.showinfo("Imprimir", "Se envió a imprimir")).pack(pady=20)


# --- PRUEBA INDEPENDIENTE ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Facturación - Prueba independiente")
    root.geometry("950x600")
    app = Facturacion(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

