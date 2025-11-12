import tkinter as tk
from tkinter import colorchooser, messagebox

class Configuracion(tk.Frame):
    def __init__(self, parent, usuario, main_app):
        super().__init__(parent, bg=main_app.config_color_fondo)
        self.main_app = main_app
        self.usuario = usuario

        # Título
        tk.Label(
            self, text="Configuración del Sistema",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Botón para elegir color de fondo
        tk.Button(
            self, text="Cambiar color de fondo",
            bg=main_app.config_color_boton, fg="white",
            font=("Arial", 12),
            command=self.cambiar_color_fondo
        ).pack(pady=10)

        # Botón para elegir color de botones
        tk.Button(
            self, text="Cambiar color de botones",
            bg=main_app.config_color_boton, fg="white",
            font=("Arial", 12),
            command=self.cambiar_color_boton
        ).pack(pady=10)

        # Botón para aplicar los cambios
        tk.Button(
            self, text="Aplicar configuración",
            bg="#117A65", fg="white", font=("Arial", 12),
            command=self.aplicar_configuracion
        ).pack(pady=20)

    # ==============================
    # Funciones de configuración
    # ==============================
    def cambiar_color_fondo(self):
        color = colorchooser.askcolor(title="Seleccionar color de fondo")[1]
        if color:
            self.main_app.config_color_fondo = color
            self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)
            self.main_app.contenedor_principal.config(bg=color)
            self.config(bg=color)

    def cambiar_color_boton(self):
        color = colorchooser.askcolor(title="Seleccionar color de botones")[1]
        if color:
            self.main_app.config_color_boton = color
            self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)

    def aplicar_configuracion(self):
        messagebox.showinfo("Configuración", "Cambios aplicados correctamente.")
        self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)  