import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sqlite3

class Login(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.main_app = main_app

        # --- Colores dinámicos tomados de configuración ---
        color_fondo = getattr(main_app, "config_color_fondo", "#1C2833")
        color_boton = getattr(main_app, "config_color_boton", "#1ABC9C")
        color_texto = getattr(main_app, "config_color_texto", "white")
        color_secundario = getattr(main_app, "config_color_secundario", "#212F3D")

        self.configure(bg=color_fondo)

        # --- Conexión a la base de datos ---
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_usuarios()

        # --- Título principal ---
        tk.Label(self, text="Taller Mecánico",
                 font=("Arial", 22, "bold"),
                 bg=color_fondo, fg=color_boton).pack(pady=20)

        # --- LOGO circular ---
        try:
            imagen = Image.open("imagenes/iconoTOq.png").resize((120, 120))
            mascara = Image.new("L", (120, 120), 0)
            draw = ImageDraw.Draw(mascara)
            draw.ellipse((0, 0, 120, 120), fill=255)
            imagen.putalpha(mascara)
            self.logo = ImageTk.PhotoImage(imagen)
            tk.Label(self, image=self.logo, bg=color_fondo).pack(pady=5)
        except Exception:
            tk.Label(self, text="(Logo no disponible)", bg=color_fondo, fg=color_texto).pack(pady=10)

        # --- Marco del formulario ---
        frame = tk.Frame(self, bg=color_secundario, bd=3, relief="ridge")
        frame.pack(padx=40, pady=20)

        # --- Campo Usuario ---
        tk.Label(frame, text="Usuario:", font=("Arial", 12, "bold"),
                 bg=color_secundario, fg=color_texto).pack(pady=(15, 5))
        self.usuario_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        self.usuario_entry.pack(pady=5)

        # --- Campo Contraseña ---
        tk.Label(frame, text="Contraseña:", font=("Arial", 12, "bold"),
                 bg=color_secundario, fg=color_texto).pack(pady=(10, 5))
        self.contra_entry = tk.Entry(frame, font=("Arial", 12), show="*", width=25)
        self.contra_entry.pack(pady=5)

        # --- Botones ---
        tk.Button(frame, text="Iniciar Sesión", font=("Arial", 12, "bold"),
                  bg=color_boton, fg=color_fondo, activebackground="#117A65",
                  command=self.verificar_login, width=20).pack(pady=15)

        tk.Button(frame, text="Registrar nuevo usuario", font=("Arial", 10, "bold"),
                  bg="#5DADE2", fg="white", activebackground="#3498DB",
                  command=self.abrir_registro, width=25).pack(pady=(0, 15))

        # --- Pie de página ---
       # tk.Label(self, text=" 2025 Taller Mecánico - Sistema POS",
               #  font=("Arial", 9), bg=color_fondo, fg=color_texto).pack(side="bottom", pady=10)

       # self.pack(fill="both", expand=True)

    # ---------- FUNCIONES DE BASE DE DATOS ----------
    def crear_tabla_usuarios(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                contrasena TEXT
            )
        ''')
        self.conexion.commit()

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contra_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos")
            return

        self.cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?", (usuario, contrasena))
        resultado = self.cursor.fetchone()

        if resultado:
            messagebox.showinfo("Bienvenido", f"Acceso concedido: {usuario}")
            self.main_app.iniciar_sesion(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_registro(self):
        ventana_registro = tk.Toplevel(self)
        RegistroUsuario(ventana_registro, self)


# ---------- CLASE DE REGISTRO ----------
class RegistroUsuario:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Registrar Usuario")
        self.root.geometry("380x300")

        # --- Colores heredados de configuración ---
        main_app = getattr(login_window, "main_app", None)
        color_fondo = getattr(main_app, "config_color_fondo", "#1C2833")
        color_boton = getattr(main_app, "config_color_boton", "#1ABC9C")
        color_texto = getattr(main_app, "config_color_texto", "white")
        color_secundario = getattr(main_app, "config_color_secundario", "#212F3D")

        self.root.config(bg=color_fondo)
        self.root.resizable(False, False)

        tk.Label(self.root, text="Registro de nuevo usuario",
                 font=("Arial", 16, "bold"), bg=color_fondo, fg=color_boton).pack(pady=15)

        tk.Label(self.root, text="Usuario:", font=("Arial", 12, "bold"),
                 bg=color_fondo, fg=color_texto).pack(pady=5)
        self.usuario_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 12, "bold"),
                 bg=color_fondo, fg=color_texto).pack(pady=5)
        self.contra_entry = tk.Entry(self.root, font=("Arial", 12), show="*", width=25)
        self.contra_entry.pack(pady=5)

        tk.Button(self.root, text="Registrar", bg=color_boton, fg=color_fondo,
                  font=("Arial", 12, "bold"), activebackground="#117A65",
                  command=self.registrar_usuario, width=18).pack(pady=20)

    def registrar_usuario(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contra_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos")
            return

        try:
            self.login_window.cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                                             (usuario, contrasena))
            self.login_window.conexion.commit()
            messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
            self.root.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")
