import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Facturacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Facturación - Taller Mecánico")
        self.root.geometry("950x600")
        self.root.config(bg="#1C2833")
        self.root.resizable(False, False)

        # --- Título ---
        titulo = tk.Label(self.root, text="FACTURACIÓN DE SERVICIOS",
                          font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C")
        titulo.pack(pady=15)

        # --- Frame principal ---
        frame = tk.Frame(self.root, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Variables ---
        self.id_orden = tk.StringVar()
        self.cliente = tk.StringVar()
        self.total = tk.StringVar()
        self.metodo_pago = tk.StringVar()

        # --- Conexión inicial ---
        self.crear_tabla()

        # --- Formulario ---
        tk.Label(frame, text="ID Orden:", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.id_orden, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Cliente:", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.cliente, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Total a Pagar ($):", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.total, width=30).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(frame, text="Método de Pago:", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        combo_metodo = ttk.Combobox(frame, textvariable=self.metodo_pago, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly", width=28)
        combo_metodo.grid(row=3, column=1, padx=10, pady=10)
        combo_metodo.current(0)

        # --- Botones ---
        tk.Button(frame, text="Registrar Factura", command=self.registrar_factura,
                  bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=4, column=0, padx=10, pady=15)

        tk.Button(frame, text="Mostrar Facturas", command=self.mostrar_facturas,
                  bg="#117A65", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=4, column=1, padx=10, pady=15)

        # --- Tabla de facturas ---
        self.tabla = ttk.Treeview(frame, columns=("id", "orden", "cliente", "total", "pago"), show="headings", height=10)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=20, pady=10)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("orden", text="ID Orden")
        self.tabla.heading("cliente", text="Cliente")
        self.tabla.heading("total", text="Total ($)")
        self.tabla.heading("pago", text="Método de Pago")

        self.tabla.column("id", width=50)
        self.tabla.column("orden", width=120)
        self.tabla.column("cliente", width=200)
        self.tabla.column("total", width=120)
        self.tabla.column("pago", width=150)

    # --- Crear tabla ---
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

    # --- Registrar Factura ---
    def registrar_factura(self):
        if not self.id_orden.get() or not self.cliente.get() or not self.total.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO facturas (id_orden, cliente, total, metodo_pago) VALUES (?, ?, ?, ?)", 
                           (self.id_orden.get(), self.cliente.get(), float(self.total.get()), self.metodo_pago.get()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Factura registrada correctamente")
            self.mostrar_facturas()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la factura: {e}")

    # --- Mostrar Facturas ---
    def mostrar_facturas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas")
        for fila in cursor.fetchall():
            self.tabla.insert("", "end", values=fila)
        conn.close()

    # --- Limpiar campos ---
    def limpiar_campos(self):
        self.id_orden.set("")
        self.cliente.set("")
        self.total.set("")
        self.metodo_pago.set("Efectivo")


# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Facturacion(root)
    root.mainloop()
