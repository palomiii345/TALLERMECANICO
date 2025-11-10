import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Configuracion(tk.Frame):
    def __init__(self, master, usuario_actual, app_principal):
        super().__init__(master)
        self.usuario_actual = usuario_actual
        self.app_principal = app_principal
        self.configure(bg="#f8f8f8")

        # --- Variables de configuración ---
        self.color_fondo = tk.StringVar(value="Blanco")
        self.color_texto = tk.StringVar(value="Negro")
        self.tamano_fuente = tk.IntVar(value=12)
        self.tamano_botones = tk.IntVar(value=12)
        self.contraste = tk.StringVar(value="Claro")

        # --- Frame de perfil ---
        frame_perfil = ttk.LabelFrame(self, text="Perfil de Usuario")
        frame_perfil.pack(padx=10, pady=10, fill="x")

        # Mostrar usuario actual
        ttk.Label(frame_perfil, text=f"Usuario: {self.usuario_actual}").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Opcional: agregar campo de email o nombre
        ttk.Label(frame_perfil, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_var = tk.StringVar()
        self._cargar_email()
        ttk.Entry(frame_perfil, textvariable=self.email_var).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame_perfil, text="Actualizar Perfil", command=self.actualizar_perfil).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Frame de contraseña ---
        frame_contra = ttk.LabelFrame(self, text="Cambiar Contraseña")
        frame_contra.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_contra, text="Nueva Contraseña:").grid(row=0, column=0, padx=10, pady=5)
        self.nueva_contra = ttk.Entry(frame_contra, show="*")
        self.nueva_contra.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_contra, text="Confirmar Contraseña:").grid(row=1, column=0, padx=10, pady=5)
        self.confirmar_contra = ttk.Entry(frame_contra, show="*")
        self.confirmar_contra.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame_contra, text="Actualizar Contraseña", command=self.actualizar_contra).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Frame de apariencia ---
        frame_apariencia = ttk.LabelFrame(self, text="Apariencia / Accesibilidad")
        frame_apariencia.pack(padx=10, pady=10, fill="x")

        # Combobox de colores
        colores = ["Blanco", "Negro", "Azul", "Verde", "Amarillo", "Gris", "Rojo"]
        ttk.Label(frame_apariencia, text="Color de fondo:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Combobox(frame_apariencia, textvariable=self.color_fondo, values=colores, state="readonly").grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_apariencia, text="Color de texto:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Combobox(frame_apariencia, textvariable=self.color_texto, values=colores, state="readonly").grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame_apariencia, text="Tamaño de letra:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Spinbox(frame_apariencia, from_=8, to=24, textvariable=self.tamano_fuente, width=5).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame_apariencia, text="Tamaño botones:").grid(row=3, column=0, padx=10, pady=5)
        ttk.Spinbox(frame_apariencia, from_=8, to=24, textvariable=self.tamano_botones, width=5).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(frame_apariencia, text="Contraste:").grid(row=4, column=0, padx=10, pady=5)
        ttk.Combobox(frame_apariencia, textvariable=self.contraste, values=["Claro", "Oscuro"], state="readonly").grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(frame_apariencia, text="Aplicar Configuración", command=self.aplicar_configuracion).grid(row=5, column=0, columnspan=2, pady=10)

        # --- Botones de navegación ---
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=10)
        ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)
        ttk.Button(self, text="⬅️ Volver al Menú", command=self.volver_menu).pack(pady=5)

        self.pack(fill="both", expand=True)

    # ==============================
    # Funciones de base de datos
    # ==============================
    def conectar(self):
        return sqlite3.connect("taller_mecanico.db")

    def _cargar_email(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM usuarios WHERE usuario=?", (self.usuario_actual,))
            result = cursor.fetchone()
            if result:
                self.email_var.set(result[0])
            conn.close()
        except:
            self.email_var.set("")

    def actualizar_perfil(self):
        email = self.email_var.get()
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET email=? WHERE usuario=?", (email, self.usuario_actual))
            conn.commit()
            conn.close()
            messagebox.showinfo("Perfil", "Perfil actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el perfil: {e}")

    def actualizar_contra(self):
        nueva = self.nueva_contra.get()
        confirmar = self.confirmar_contra.get()
        if not nueva or not confirmar:
            messagebox.showwarning("Campos Vacíos", "Completa todos los campos")
            return
        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET contrasena=? WHERE usuario=?", (nueva, self.usuario_actual))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")
            self.nueva_contra.delete(0, tk.END)
            self.confirmar_contra.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e}")

    # ==============================
    # Aplicar configuración
    # ==============================
    def aplicar_configuracion(self):
        # Guardar en MainApp
        self.app_principal.config_color_fondo = self._traducir_color(self.color_fondo.get())
        self.app_principal.config_color_boton = self._traducir_color(self.color_texto.get())
        self.app_principal.config_tamano_fuente = self.tamano_fuente.get()
        self.app_principal.config_tamano_botones = self.tamano_botones.get()
        # Contraste
        if self.contraste.get() == "Oscuro":
            self.app_principal.config_color_fondo = "#333333"
            self.app_principal.config_color_boton = "#FFFFFF"
        else:
            self.app_principal.config_color_fondo = "#FFFFFF"
            self.app_principal.config_color_boton = "#000000"

        # Aplicar a toda la pantalla
        self.app_principal._aplicar_estilo_pantalla(self.app_principal.pantalla_actual)
        messagebox.showinfo("Configuración", "Preferencias aplicadas a todo el sistema")

    def _traducir_color(self, nombre):
        colores = {
            "Blanco": "#FFFFFF",
            "Negro": "#000000",
            "Azul": "#1E90FF",
            "Verde": "#32CD32",
            "Amarillo": "#FFD700",
            "Gris": "#A9A9A9",
            "Rojo": "#FF6347"
        }
        return colores.get(nombre, "#FFFFFF")

    # ==============================
    # Sesión y navegación
    # ==============================
    def cerrar_sesion(self):
        self.app_principal.cerrar_sesion()

    def volver_menu(self):
        self.app_principal.cambiar_pantalla("menu")

