import tkinter as tk
from tkinter import messagebox

from Login import Login
from clientes import Clientes
from vehiculos import Vehiculos

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Taller Mecánico")
        self.root.geometry("950x600")
        self.root.config(bg="#1C2833")
        self.root.resizable(False, False)

        # --- Título del sistema ---
        titulo = tk.Label(self.root, text="SISTEMA DE GESTIÓN - TALLER MECÁNICO",
                          font=("Arial", 18, "bold"), bg="#1C2833", fg="#1ABC9C")
        titulo.pack(pady=15)

        # --- Marco principal ---
        frame = tk.Frame(self.root, bg="#212F3D", bd=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Sección de botones (menú) ---
        tk.Label(frame, text="Módulos del Sistema", font=("Arial", 14, "bold"),
                 bg="#212F3D", fg="white").pack(pady=10)

        botones = [
            ("Clientes", self.abrir_clientes),
            ("Vehículos", self.abrir_vehiculos),
            ("Inventario", self.abrir_inventario),
            ("Órdenes de Servicio", self.abrir_ordenes),
            ("Facturación", self.abrir_facturacion),
            ("Citas", self.abrir_citas),
            ("Reportes", self.abrir_reportes),
            ("Configuración / Perfil", self.abrir_configuracion),
            ("Cerrar Sesión", self.cerrar_sesion)
        ]

        for texto, comando in botones:
            boton = tk.Button(frame, text=texto, font=("Arial", 12, "bold"),
                              bg="#1ABC9C", fg="white", width=25, height=2,
                              command=comando, relief="ridge", cursor="hand2")
            boton.pack(pady=8)

        # --- Información inferior ---
        tk.Label(self.root, text="© 2025 Taller Mecánico - Sistema POS",
                 font=("Arial", 9), bg="#1C2833", fg="gray").pack(side="bottom", pady=5)

    # ---------- Funciones para abrir pantallas (a crear después) ----------
    def abrir_clientes(self):

     nueva_ventana = tk.Toplevel(self.root)
     Clientes(nueva_ventana)

    def abrir_vehiculos(self):
      nueva_ventana = tk.Toplevel(self.root)
      Vehiculos(nueva_ventana)

    def abrir_inventario(self):
        messagebox.showinfo("Inventario", "Aquí se mostrará el inventario de refacciones")

    def abrir_ordenes(self):
        messagebox.showinfo("Órdenes", "Aquí se registrarán las órdenes de servicio")

    def abrir_facturacion(self):
        messagebox.showinfo("Facturación", "Aquí se generarán las facturas de servicios")

    def abrir_citas(self):
        messagebox.showinfo("Citas", "Aquí se agendarán citas y servicios")

    def abrir_reportes(self):
        messagebox.showinfo("Reportes", "Aquí se mostrarán reportes de ventas y servicios")

    def abrir_configuracion(self):
        messagebox.showinfo("Configuración", "Aquí podrás cambiar datos de usuario o contraseña")

    def cerrar_sesion(self):
        confirmacion = messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?")
        if confirmacion:
            self.root.destroy()
          #  from login import Login
            nuevo_root = tk.Tk()
            Login(nuevo_root)
            nuevo_root.mainloop()


# --- PRUEBA DIRECTA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
