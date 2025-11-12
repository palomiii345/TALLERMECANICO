import tkinter as tk
from tkinter import colorchooser, messagebox


class Configuracion(tk.Frame):
    def __init__(self, parent, usuario, main_app):
        super().__init__(parent, bg=main_app.config_color_fondo)
        self.main_app = main_app
        self.usuario = usuario

        # Variables de configuración
        self.tamano_fuente = tk.IntVar(value=main_app.config_tamano_fuente)
        self.tamano_boton = tk.IntVar(value=main_app.config_tamano_botones)
        self.modo_oscuro = tk.BooleanVar(value=False)

        # ======== CONTENEDOR CENTRAL ========
        contenedor = tk.Frame(self, bg=main_app.config_color_fondo)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")  # Centrado exacto

        # ======== TÍTULO =========
        tk.Label(
            contenedor,
            text="⚙️ Configuración del Sistema",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(0, 30))

        # ======== SECCIÓN DE COLORES =========
        frame_colores = tk.LabelFrame(
            contenedor, text="Personalización de colores",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            font=("Segoe UI", 12, "bold"),
            padx=20, pady=15
        )
        frame_colores.pack(fill="x", pady=10)

        tk.Button(
            frame_colores, text="Cambiar color de fondo",
            bg=main_app.config_color_boton, fg="white",
            font=("Segoe UI", 11, "bold"),
            width=25, height=1,
            command=self.cambiar_color_fondo
        ).pack(pady=6)

        tk.Button(
            frame_colores, text="Cambiar color de botones",
            bg=main_app.config_color_boton, fg="white",
            font=("Segoe UI", 11, "bold"),
            width=25, height=1,
            command=self.cambiar_color_boton
        ).pack(pady=6)

        # ======== SECCIÓN DE ACCESIBILIDAD =========
        frame_accesibilidad = tk.LabelFrame(
            contenedor, text="Accesibilidad visual",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            font=("Segoe UI", 12, "bold"),
            padx=20, pady=15
        )
        frame_accesibilidad.pack(fill="x", pady=10)

        # Tamaño del texto
        tk.Label(
            frame_accesibilidad, text="Tamaño del texto:",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_texto,
            font=("Segoe UI", 11)
        ).pack(pady=(5, 2))

        tk.Scale(
            frame_accesibilidad, from_=8, to=24, orient="horizontal",
            variable=self.tamano_fuente,
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            highlightthickness=0,
            troughcolor=main_app.config_color_secundario,
            command=lambda v: self.actualizar_preview()
        ).pack(pady=(0, 10))

        # Tamaño de botones
        tk.Label(
            frame_accesibilidad, text="Tamaño de los botones:",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_texto,
            font=("Segoe UI", 11)
        ).pack(pady=(5, 2))

        tk.Scale(
            frame_accesibilidad, from_=8, to=24, orient="horizontal",
            variable=self.tamano_boton,
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            highlightthickness=0,
            troughcolor=main_app.config_color_secundario,
            command=lambda v: self.actualizar_preview()
        ).pack(pady=(0, 10))

        # Modo oscuro
        tk.Checkbutton(
            frame_accesibilidad,
            text="Activar modo oscuro",
            variable=self.modo_oscuro,
            onvalue=True, offvalue=False,
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_texto,
            selectcolor=main_app.config_color_fondo,
            font=("Segoe UI", 11),
            command=self.actualizar_preview
        ).pack(pady=5)

        # ======== VISTA PREVIA =========
        preview_frame = tk.LabelFrame(
            contenedor, text="Vista previa",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton,
            font=("Segoe UI", 12, "bold"),
            padx=20, pady=15
        )
        preview_frame.pack(fill="x", pady=15)

        self.preview_label = tk.Label(
            preview_frame,
            text="Texto de ejemplo",
            bg=main_app.config_color_fondo,
            fg=main_app.config_color_texto,
            font=("Segoe UI", self.tamano_fuente.get(), "bold")
        )
        self.preview_label.pack(pady=10)

        self.preview_button = tk.Button(
            preview_frame,
            text="Botón de ejemplo",
            bg=main_app.config_color_boton,
            fg="white",
            font=("Segoe UI", self.tamano_boton.get(), "bold"),
            width=20, height=1
        )
        self.preview_button.pack(pady=5)

        # ======== BOTÓN DE APLICAR =========
        tk.Button(
            contenedor,
            text="💾 Aplicar configuración",
            bg="#117A65", fg="white",
            font=("Segoe UI", 12, "bold"),
            width=30, height=2,
            command=self.aplicar_configuracion
        ).pack(pady=25)

    # ==============================
    # FUNCIONES DE CONFIGURACIÓN
    # ==============================
    def cambiar_color_fondo(self):
        color = colorchooser.askcolor(title="Seleccionar color de fondo")[1]
        if color:
            self.main_app.config_color_fondo = color
            self.config(bg=color)
            self.actualizar_preview()

    def cambiar_color_boton(self):
        color = colorchooser.askcolor(title="Seleccionar color de botones")[1]
        if color:
            self.main_app.config_color_boton = color
            self.actualizar_preview()

    def actualizar_preview(self, *args):
        """Actualiza la vista previa visualmente en tiempo real."""
        # Modo oscuro
        if self.modo_oscuro.get():
            fondo = "#1C1C1C"
            texto = "white"
            boton = "#00BCD4"
        else:
            fondo = self.main_app.config_color_fondo
            texto = "black"
            boton = self.main_app.config_color_boton

        # Aplicar cambios a los elementos de vista previa
        self.preview_label.config(
            bg=fondo,
            fg=texto,
            font=("Segoe UI", self.tamano_fuente.get(), "bold")
        )
        self.preview_button.config(
            bg=boton,
            fg="white",
            font=("Segoe UI", self.tamano_boton.get(), "bold")
        )
        self.config(bg=fondo)

    def aplicar_configuracion(self):
        """Guarda y aplica los cambios globales en la aplicación."""
        self.main_app.config_tamano_fuente = self.tamano_fuente.get()
        self.main_app.config_tamano_botones = self.tamano_boton.get()

        if self.modo_oscuro.get():
            self.main_app.config_color_fondo = "#1C1C1C"
            self.main_app.config_color_boton = "#00BCD4"
            self.main_app.config_color_texto = "white"
        else:
            self.main_app.config_color_fondo = "#F2F4F4"
            self.main_app.config_color_boton = "#1ABC9C"
            self.main_app.config_color_texto = "black"

        self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)
        self.main_app.contenedor_principal.config(bg=self.main_app.config_color_fondo)
        self.config(bg=self.main_app.config_color_fondo)
        messagebox.showinfo("Configuración", "Cambios aplicados correctamente.")
