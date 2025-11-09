import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sqlite3

class Login(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent, bg="#2E4053")
        self.main_app = main_app

        # Conexión a la base de datos
        self.conexion = sqlite3.connect("taller_mecanico.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla_usuarios()

        # --- Título ---
        tk.Label(self, text="Taller Mecánico", 
                 font=("Arial", 18, "bold"), 
                 bg="#2E4053", fg="white").pack(pady=10)

        # --- LOGO CIRCULAR ---
        try:
            imagen = Image.open("imagenes/iconoTOq.png").resize((100, 100))
            # Crear máscara circular
            mascara = Image.new("L", (100, 100), 0)
            draw = ImageDraw.Draw(mascara)
            draw.ellipse((0, 0, 100, 100), fill=255)
            imagen.putalpha(mascara)
            self.logo = ImageTk.PhotoImage(imagen)
            tk.Label(self, image=self.logo, bg="#2E4053").pack(pady=10)
        except Exception as e:
            tk.Label(self, text="(Logo no disponible)", bg="#2E4053", fg="lightgray").pack(pady=10)

        # --- Marco del formulario ---
        frame = tk.Frame(self, bg="#34495E", bd=2, relief="groove")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#34495E", fg="white").pack(pady=10)
        self.usuario_entry = tk.Entry(frame, font=("Arial", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#34495E", fg="white").pack(pady=10)
        self.contra_entry = tk.Entry(frame, font=("Arial", 12), show="*")
        self.contra_entry.pack(pady=5)

        # --- Botones ---
        tk.Button(frame, text="Iniciar Sesión", font=("Arial", 12, "bold"), 
                  bg="#1ABC9C", fg="white", command=self.verificar_login).pack(pady=10)

        tk.Button(frame, text="Registrar nuevo usuario", font=("Arial", 10), 
                  bg="#5DADE2", fg="white", command=self.abrir_registro).pack(pady=5)

        tk.Label(self, text="© 2025 Taller Mecánico - Sistema POS", 
                 font=("Arial", 9), bg="#2E4053", fg="lightgray").pack(side="bottom", pady=5)

        self.pack(fill="both", expand=True)

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


# ---------- CLASE DE REGISTRO DE NUEVOS USUARIOS ----------
class RegistroUsuario:
    def __init__(self, root, login_window):
        self.root = root
        self.root.title("Registrar Usuario")
        self.root.geometry("380x300")
        self.root.config(bg="#283747")
        self.root.resizable(False, False)

        self.login_window = login_window

        tk.Label(self.root, text="Registrar nuevo usuario", font=("Arial", 15, "bold"), 
                 bg="#283747", fg="white").pack(pady=15)

        tk.Label(self.root, text="Usuario:", font=("Arial", 12), bg="#283747", fg="white").pack(pady=5)
        self.usuario_entry = tk.Entry(self.root, font=("Arial", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 12), bg="#283747", fg="white").pack(pady=5)
        self.contra_entry = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.contra_entry.pack(pady=5)

        tk.Button(self.root, text="Registrar", bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"),
                  command=self.registrar_usuario).pack(pady=15)

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

