import tkinter as tk
from tkinter import messagebox

class MenuPrincipal(tk.Frame):
    def __init__(self, root, main_app):
        super().__init__(root, bg="#212F3D")
        self.main_app = main_app
        self.menu_lateral_abierto = True

        # --- Botón toggle del menú ---
        self.boton_toggle = tk.Button(self, text="☰", font=("Arial", 14, "bold"),
                                      bg="#1ABC9C", fg="white", width=3,
                                      command=self.toggle)
        self.boton_toggle.pack(pady=10)

        # --- Botones del menú ---
        self.botones = [
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

        self.botones_widgets = []
        for texto, comando in self.botones:
            b = tk.Button(self, text=texto, font=("Arial", 12, "bold"),
                          bg="#1ABC9C", fg="white", width=20, height=2,
                          command=comando, relief="raised", cursor="hand2",
                          activebackground="#117A65", activeforeground="white")
            b.pack(pady=5)
            self.botones_widgets.append(b)

    # ---------- Método toggle público ----------
    def toggle(self):
        if self.menu_lateral_abierto:
            self.pack_forget()
            self.menu_lateral_abierto = False
        else:
            self.pack(side="left", fill="y")
            self.menu_lateral_abierto = True

    # ---------- Funciones de navegación ----------
    def abrir_clientes(self):
        self.main_app.cambiar_pantalla("clientes")

    def abrir_vehiculos(self):
        self.main_app.cambiar_pantalla("vehiculos")

    def abrir_inventario(self):
        self.main_app.cambiar_pantalla("inventario")

    def abrir_ordenes(self):
        self.main_app.cambiar_pantalla("ordenes")

    def abrir_facturacion(self):
        self.main_app.cambiar_pantalla("facturacion")

    def abrir_citas(self):
        self.main_app.cambiar_pantalla("citas")

    def abrir_reportes(self):
        self.main_app.cambiar_pantalla("reportes")

    def abrir_configuracion(self):
        self.main_app.cambiar_pantalla("configuracion")

    def cerrar_sesion(self):
        confirmacion = messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?")
        if confirmacion:
            self.main_app.cerrar_sesion()
