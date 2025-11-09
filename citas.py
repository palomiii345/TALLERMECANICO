import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class Citas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Citas - Taller Mecánico")
        self.root.geometry("950x600")
        self.root.config(bg="#1C2833")
        self.root.resizable(False, False)

        # --- Título ---
        titulo = tk.Label(self.root, text="AGENDAR CITAS DE SERVICIO",
                          font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C")
        titulo.pack(pady=15)

        # --- Frame principal ---
        frame = tk.Frame(self.root, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Variables ---
        self.cliente = tk.StringVar()
        self.fecha = tk.StringVar()
        self.hora = tk.StringVar()
        self.servicio = tk.StringVar()

        # --- Crear tabla SQLite ---
        self.crear_tabla()

        # --- Formulario ---
        tk.Label(frame, text="Cliente:", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.cliente, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Fecha (AAAA-MM-DD):", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.fecha, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="Hora (HH:MM):", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(frame, textvariable=self.hora, width=30).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(frame, text="Servicio:", font=("Arial", 12, "bold"), bg="#212F3D", fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        combo_servicio = ttk.Combobox(frame, textvariable=self.servicio,
                                      values=["Mantenimiento", "Cambio de aceite", "Frenos", "Suspensión", "Motor", "Diagnóstico"],
                                      state="readonly", width=28)
        combo_servicio.grid(row=3, column=1, padx=10, pady=10)
        combo_servicio.current(0)

        # --- Botones ---
        tk.Button(frame, text="Registrar Cita", command=self.registrar_cita,
                  bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=4, column=0, padx=10, pady=15)
        tk.Button(frame, text="Mostrar Citas", command=self.mostrar_citas,
                  bg="#117A65", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=4, column=1, padx=10, pady=15)
        tk.Button(frame, text="Eliminar Cita", command=self.eliminar_cita,
                  bg="#922B21", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=4, column=2, padx=10, pady=15)

        # --- Tabla ---
        self.tabla = ttk.Treeview(frame, columns=("id", "cliente", "fecha", "hora", "servicio"), show="headings", height=10)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=20, pady=10)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("cliente", text="Cliente")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("servicio", text="Servicio")

        self.tabla.column("id", width=50)
        self.tabla.column("cliente", width=200)
        self.tabla.column("fecha", width=100)
        self.tabla.column("hora", width=100)
        self.tabla.column("servicio", width=150)

    # --- Crear tabla SQLite ---
    def crear_tabla(self):
        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                hora TEXT,
                servicio TEXT
            )
        """)
        conn.commit()
        conn.close()

    # --- Registrar Cita ---
    def registrar_cita(self):
        if not self.cliente.get() or not self.fecha.get() or not self.hora.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Validar formato de fecha
            datetime.strptime(self.fecha.get(), "%Y-%m-%d")
            datetime.strptime(self.hora.get(), "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha u hora incorrecto (Ej: 2025-11-10 / 14:30)")
            return

        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO citas (cliente, fecha, hora, servicio) VALUES (?, ?, ?, ?)",
                       (self.cliente.get(), self.fecha.get(), self.hora.get(), self.servicio.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita registrada correctamente")
        self.mostrar_citas()
        self.limpiar_campos()

    # --- Mostrar Citas ---
    def mostrar_citas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conn = sqlite3.connect("taller_mecanico.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas")
        for fila in cursor.fetchall():
            self.tabla.insert("", "end", values=fila)
        conn.close()

    # --- Eliminar cita seleccionada ---
    def eliminar_cita(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para eliminar")
            return

        item = self.tabla.item(seleccion)
        id_cita = item["values"][0]

        confirmar = messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar esta cita?")
        if confirmar:
            conn = sqlite3.connect("taller_mecanico.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM citas WHERE id = ?", (id_cita,))
            conn.commit()
            conn.close()
            self.mostrar_citas()
            messagebox.showinfo("Eliminado", "Cita eliminada correctamente")

    # --- Limpiar campos ---
    def limpiar_campos(self):
        self.cliente.set("")
        self.fecha.set("")
        self.hora.set("")
        self.servicio.set("Mantenimiento")


# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Citas(root)
    root.mainloop()
