import tkinter as tk
from Login import Login
from menu_principal import MenuPrincipal
from clientes import Clientes
from vehiculos import Vehiculos
from inventario import Inventario
from ordenes_servicio import OrdenesServicio
from facturacion import Facturacion
from citas import Citas
from reportes import Reportes
from configuracion import Configuracion

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Punto de Venta - Taller Mecánico")
        self.root.geometry("1024x768")
        self.root.state("zoomed")

        # Configuración de accesibilidad
        self.config_color_fondo = "#FFFFFF"
        self.config_color_boton = "#000000"
        self.config_tamano_fuente = 12
        self.config_tamano_botones = 12

        # Variables de control
        self.usuario_actual = None
        self.menu_lateral = None

        # Contenedor principal (menu + contenido)
        self.contenedor_principal = tk.Frame(self.root)
        self.contenedor_principal.pack(fill="both", expand=True)

        # Frame de contenido
        self.frame_contenido = tk.Frame(self.contenedor_principal, bg="#f0f0f0")
        self.frame_contenido.pack(fill="both", expand=True, side="left")

        # Botón toggle siempre visible
        self.boton_toggle = tk.Button(self.root, text="☰", font=("Arial", 14, "bold"),
                                      bg="#1ABC9C", fg="white", width=3,
                                      command=self.toggle_menu)
        self.boton_toggle.place(x=10, y=10)  # esquina superior izquierda

        # Mostrar login al inicio
        self.cambiar_pantalla("Login")

    # ==============================
    # Toggle menú lateral
    # ==============================
    def toggle_menu(self):
        if self.menu_lateral:
            if self.menu_lateral.winfo_viewable():
                self.menu_lateral.pack_forget()
            else:
                self.menu_lateral.pack(side="left", fill="y")

    # ==============================
    # Cambiar pantallas
    # ==============================
    def cambiar_pantalla(self, nueva_pantalla):
        # Limpiar contenido actual
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Crear menú lateral si ya hay sesión y no existe
        if self.usuario_actual and nueva_pantalla != "Login":
            if not self.menu_lateral:
                self.menu_lateral = MenuPrincipal(self.contenedor_principal, self)
                self.menu_lateral.pack(side="left", fill="y")

        # Cargar la pantalla correspondiente
        if nueva_pantalla == "Login":
            Login(self.frame_contenido, self)
        elif nueva_pantalla == "clientes":
            Clientes(self.frame_contenido, self)
        elif nueva_pantalla == "vehiculos":
            Vehiculos(self.frame_contenido, self)
        elif nueva_pantalla == "inventario":
            Inventario(self.frame_contenido, self)
        elif nueva_pantalla == "ordenes":
            OrdenesServicio(self.frame_contenido, self)
        elif nueva_pantalla == "facturacion":
            Facturacion(self.frame_contenido, self)
        elif nueva_pantalla == "citas":
            Citas(self.frame_contenido, self)
        elif nueva_pantalla == "reportes":
            Reportes(self.frame_contenido, self)
        elif nueva_pantalla == "configuracion":
            Configuracion(self.frame_contenido, self.usuario_actual, self)

        # Aplicar estilo
        self._aplicar_estilo_pantalla(self.frame_contenido)

    # ==============================
    # Aplicar estilo recursivamente
    # ==============================
    def _aplicar_estilo_pantalla(self, frame):
        for widget in frame.winfo_children():
            try:
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.config_color_fondo, fg=self.config_color_boton,
                                     font=("Arial", self.config_tamano_fuente))
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=self.config_color_boton, fg=self.config_color_fondo,
                                     font=("Arial", self.config_tamano_botones))
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=self.config_color_fondo)
            except:
                pass
            if widget.winfo_children():
                self._aplicar_estilo_pantalla(widget)

    # ==============================
    # Sesión
    # ==============================
    def iniciar_sesion(self, usuario):
        self.usuario_actual = usuario
        self.cambiar_pantalla("clientes")  # Pantalla inicial tras login

    def cerrar_sesion(self):
        self.usuario_actual = None
        if self.menu_lateral:
            self.menu_lateral.destroy()
            self.menu_lateral = None

        # Volver a login
        self.frame_contenido = tk.Frame(self.contenedor_principal, bg="#f0f0f0")
        self.frame_contenido.pack(fill="both", expand=True, side="left")
        self.cambiar_pantalla("Login")


# ==============================
# Ejecutar app
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


