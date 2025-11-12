import tkinter as tk
from tkinter import ttk

class Configuracion(tk.Frame):
    def __init__(self, master, usuario, main_app):
        super().__init__(master, bg=main_app.config_color_fondo)
        self.main_app = main_app
        self.usuario = usuario

        # ======= TÍTULO =======
        titulo = tk.Label(
            self, text="Configuración del Sistema",
            font=("Arial", 20, "bold"),
            fg=main_app.config_color_boton,
            bg=main_app.config_color_fondo
        )
        titulo.pack(pady=20)

        # ========================
        # SECCIÓN DE APARIENCIA
        # ========================
        frame_apariencia = tk.LabelFrame(
            self, text="Apariencia", font=("Arial", 14, "bold"),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton,
            padx=20, pady=10
        )
        frame_apariencia.pack(padx=40, pady=15, fill="x")

        # --- Modo oscuro ---
        self.var_modo_oscuro = tk.BooleanVar(value=main_app.config_modo_oscuro)
        chk_modo_oscuro = tk.Checkbutton(
            frame_apariencia, text="Activar modo oscuro",
            variable=self.var_modo_oscuro,
            command=self.cambiar_modo_oscuro,
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton,
            selectcolor=main_app.config_color_secundario,
            font=("Arial", 12)
        )
        chk_modo_oscuro.pack(anchor="w", pady=5)

        # --- Brillo ---
        lbl_brillo = tk.Label(
            frame_apariencia, text="Brillo", font=("Arial", 12),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton
        )
        lbl_brillo.pack(anchor="w", pady=(10, 0))
        self.slider_brillo = tk.Scale(
            frame_apariencia, from_=0.5, to=1.5, resolution=0.1,
            orient="horizontal", length=200,
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton,
            highlightthickness=0, command=self.cambiar_brillo
        )
        self.slider_brillo.set(main_app.config_brillo)
        self.slider_brillo.pack(anchor="w", pady=5)

        # --- Contraste ---
        lbl_contraste = tk.Label(
            frame_apariencia, text="Contraste", font=("Arial", 12),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton
        )
        lbl_contraste.pack(anchor="w", pady=(10, 0))
        self.slider_contraste = tk.Scale(
            frame_apariencia, from_=0.5, to=1.5, resolution=0.1,
            orient="horizontal", length=200,
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton,
            highlightthickness=0, command=self.cambiar_contraste
        )
        self.slider_contraste.set(main_app.config_contraste)
        self.slider_contraste.pack(anchor="w", pady=5)

        # --- Tamaño de letra ---
        lbl_fuente = tk.Label(
            frame_apariencia, text="Tamaño de letra", font=("Arial", 12),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton
        )
        lbl_fuente.pack(anchor="w", pady=(10, 0))
        self.slider_fuente = tk.Scale(
            frame_apariencia, from_=10, to=20, orient="horizontal",
            length=200, bg=main_app.config_color_fondo,
            fg=main_app.config_color_boton, highlightthickness=0,
            command=self.cambiar_fuente
        )
        self.slider_fuente.set(main_app.config_tamano_fuente)
        self.slider_fuente.pack(anchor="w", pady=5)

        # ========================
        # SECCIÓN DE NOTIFICACIONES
        # ========================
        frame_notif = tk.LabelFrame(
            self, text="Notificaciones", font=("Arial", 14, "bold"),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton,
            padx=20, pady=10
        )
        frame_notif.pack(padx=40, pady=15, fill="x")

        lbl_notif = tk.Label(
            frame_notif, text="Modo de notificación:",
            font=("Arial", 12),
            bg=main_app.config_color_fondo, fg=main_app.config_color_boton
        )
        lbl_notif.pack(anchor="w", pady=5)

        self.var_notificacion = tk.StringVar(value=main_app.config_notificacion_modo)

        modos = [("🔈 Sonido activado", "sonido"),
                 ("📳 Vibración", "vibracion"),
                 ("🔇 Silencio", "silencio")]

        for texto, valor in modos:
            tk.Radiobutton(
                frame_notif, text=texto, variable=self.var_notificacion,
                value=valor, command=self.cambiar_modo_notificacion,
                bg=main_app.config_color_fondo,
                fg=main_app.config_color_boton,
                selectcolor=main_app.config_color_secundario,
                font=("Arial", 12)
            ).pack(anchor="w", pady=3)

        # ========================
        # BOTÓN GUARDAR
        # ========================
        boton_guardar = tk.Button(
            self, text="Guardar cambios",
            bg=main_app.config_color_boton,
            fg=main_app.config_color_fondo,
            font=("Arial", 13, "bold"),
            relief="flat",
            command=self.guardar_configuracion
        )
        boton_guardar.pack(pady=20)

    # ========================
    # FUNCIONES DE CONFIGURACIÓN
    # ========================

    def cambiar_modo_oscuro(self):
        self.main_app.config_modo_oscuro = self.var_modo_oscuro.get()
        if self.main_app.config_modo_oscuro:
            self.main_app.config_color_fondo = "#1C2833"
            self.main_app.config_color_secundario = "#212F3D"
            self.main_app.config_color_boton = "#1ABC9C"
            self.main_app.config_color_texto = "white"
        else:
            self.main_app.config_color_fondo = "#F8F9F9"
            self.main_app.config_color_secundario = "#D5DBDB"
            self.main_app.config_color_boton = "#2E4053"
            self.main_app.config_color_texto = "black"

        self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)
        if self.main_app.menu_lateral:
            self.main_app._aplicar_estilo_pantalla(self.main_app.menu_lateral)

    def cambiar_brillo(self, valor):
        self.main_app.config_brillo = float(valor)
        print(f"Brillo ajustado a: {valor}")

    def cambiar_contraste(self, valor):
        self.main_app.config_contraste = float(valor)
        print(f"Contraste ajustado a: {valor}")

    def cambiar_fuente(self, valor):
        self.main_app.config_tamano_fuente = int(valor)
        self.main_app.config_tamano_botones = int(valor)
        self.main_app._aplicar_estilo_pantalla(self.main_app.frame_contenido)
        if self.main_app.menu_lateral:
            self.main_app._aplicar_estilo_pantalla(self.main_app.menu_lateral)

    def cambiar_modo_notificacion(self):
        modo = self.var_notificacion.get()
        self.main_app.config_notificacion_modo = modo
        if modo == "sonido":
            print("Modo de notificación: sonido activado")
        elif modo == "vibracion":
            print("Modo de notificación: vibración activada (simulada)")
        elif modo == "silencio":
            print("Modo de notificación: desactivado")

    def guardar_configuracion(self):
        print("\n=== Configuración guardada ===")
        print(f"Modo oscuro: {self.main_app.config_modo_oscuro}")
        print(f"Brillo: {self.main_app.config_brillo}")
        print(f"Contraste: {self.main_app.config_contraste}")
        print(f"Tamaño de letra: {self.main_app.config_tamano_fuente}")
        print(f"Notificación: {self.main_app.config_notificacion_modo}")
        print("==============================")
