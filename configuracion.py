import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from Login import Login

class Configuracion:
    def __init__(self, master, usuario_actual):
        self.master = master
        self.master.title("Configuración / Perfil de Usuario")
        self.master.geometry("500x400")
        self.master.configure(bg="#f8f8f8")

        self.usuario_actual = usuario_actual

        ttk.Label(master, text="⚙️ Configuración del Usuario", font=("Arial", 18, "bold")).pack(pady=15)
        ttk.Label(master, text=f"Usuario activo: {self.usuario_actual}", font=("Arial", 12)).pack(pady=5)

        # Frame de configuración
        frame = ttk.Frame(master)
        frame.pack(pady=20)

        ttk.Label(frame, text="Nueva Contraseña:").grid(row=0, column=0, padx=10, pady=10)
        self.nueva_contra = ttk.Entry(frame, show="*")
        self.nueva_contra.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Confirmar Contraseña:").grid(row=1, column=0, padx=10, pady=10)
        self.confirmar_contra = ttk.Entry(frame, show="*")
        self.confirmar_contra.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(frame, text="Actualizar Contraseña", command=self.actualizar_contra).grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Separator(master, orient="horizontal").pack(fill="x", padx=30, pady=20)

        ttk.Button(master, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=10)
        ttk.Button(master, text="⬅️ Volver al Menú", command=self.volver_menu).pack(pady=5)

    def conectar(self):
        return sqlite3.connect("taller_mecanico.db")

    def actualizar_contra(self):
        nueva = self.nueva_contra.get()
        confirmar = self.confirmar_contra.get()

        if not nueva or not confirmar:
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasena=? WHERE usuario=?", (nueva, self.usuario_actual))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
        self.nueva_contra.delete(0, tk.END)
        self.confirmar_contra.delete(0, tk.END)

    def cerrar_sesion(self):
        confirmar = messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar sesión?")
        if confirmar:
            self.master.destroy()
            
            root = tk.Tk()
            Login(root)
            root.mainloop()

    def volver_menu(self):
        self.master.destroy()
        from menu_principal import MenuPrincipal
        root = tk.Tk()
        MenuPrincipal(root, self.usuario_actual)
        root.mainloop()
