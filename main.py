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

        # ==============================
        # 🎨 Configuración del tema global
        # ==============================
        self.config_color_fondo = "#1C2833"      # Fondo oscuro
        self.config_color_secundario = "#212F3D" # Paneles oscuros
        self.config_color_boton = "#1ABC9C"      # Verde menta
        self.config_color_texto = "white"
        self.config_tamano_fuente = 12
        self.config_tamano_botones = 12

        # ==============================
        # Variables de control
        # ==============================
        self.usuario_actual = None
        self.menu_lateral = None
        self.pantalla_actual = None

        # ==============================
        # Contenedor principal
        # ==============================
        self.contenedor_principal = tk.Frame(self.root, bg=self.config_color_fondo)
        self.contenedor_principal.pack(fill="both", expand=True)

        # Frame donde cambian las pantallas
        self.frame_contenido = tk.Frame(self.contenedor_principal, bg=self.config_color_fondo)
        self.frame_contenido.pack(fill="both", expand=True, side="left")

        # ==============================
        # Botón Toggle menú lateral
        # ==============================
        self.boton_toggle = tk.Button(
            self.root, text="☰", font=("Arial", 14, "bold"),
            bg=self.config_color_boton, fg=self.config_color_fondo, width=3,
            relief="flat", command=self.toggle_menu
        )
        self.boton_toggle.place(x=1150, y=10)

        # Mostrar login al iniciar
        self.cambiar_pantalla("Login")

    # ==============================
    # Mostrar / ocultar menú lateral
    # ==============================
    def toggle_menu(self):
        if self.menu_lateral:
            if self.menu_lateral.winfo_ismapped():
                self.menu_lateral.pack_forget()
            else:
                self.menu_lateral.pack(side="left", fill="y")

    # ==============================
    # Cambiar pantallas dinámicamente
    # ==============================
    def cambiar_pantalla(self, nueva_pantalla):
        # Limpiar contenido anterior
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        # Crear menú lateral si hay sesión activa
        if self.usuario_actual and nueva_pantalla != "Login":
            if not self.menu_lateral:
                self.menu_lateral = MenuPrincipal(self.contenedor_principal, self)
                self.menu_lateral.pack(side="left", fill="y")
                self._aplicar_estilo_pantalla(self.menu_lateral)

        # Crear la pantalla correspondiente
        pantalla = None
        if nueva_pantalla == "Login":
            pantalla = Login(self.frame_contenido, self)
        elif nueva_pantalla == "clientes":
            pantalla = Clientes(self.frame_contenido, self)
        elif nueva_pantalla == "vehiculos":
            pantalla = Vehiculos(self.frame_contenido, self)
        elif nueva_pantalla == "inventario":
            pantalla = Inventario(self.frame_contenido, self)
        elif nueva_pantalla == "ordenes":
            pantalla = OrdenesServicio(self.frame_contenido, self)
        elif nueva_pantalla == "facturacion":
            pantalla = Facturacion(self.frame_contenido, self)
        elif nueva_pantalla == "citas":
            pantalla = Citas(self.frame_contenido, self)
        elif nueva_pantalla == "reportes":
            pantalla = Reportes(self.frame_contenido, self)
        elif nueva_pantalla == "configuracion":
            pantalla = Configuracion(self.frame_contenido, self.usuario_actual, self)

        # Mostrar pantalla y aplicar estilo
        self.pantalla_actual = pantalla
        if pantalla:
            pantalla.pack(fill="both", expand=True)
            self._aplicar_estilo_pantalla(pantalla)

    # ==============================
    # Aplicar tema (colores / fuentes)
    # ==============================
    def _aplicar_estilo_pantalla(self, frame):
        """Recorre todos los widgets y aplica el tema."""
        for widget in frame.winfo_children():
            try:
                if isinstance(widget, tk.Label):
                    widget.configure(
                        bg=self.config_color_fondo,
                        fg=self.config_color_boton,
                        font=("Arial", self.config_tamano_fuente)
                    )
                elif isinstance(widget, tk.Button):
                    widget.configure(
                        bg=self.config_color_boton,
                        fg=self.config_color_fondo,
                        font=("Arial", self.config_tamano_botones, "bold"),
                        relief="flat",
                        activebackground="#16A085",
                        activeforeground="white"
                    )
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=self.config_color_fondo)
                elif isinstance(widget, tk.Entry):
                    widget.configure(bg="#2C3E50", fg="white", insertbackground="white")
            except Exception:
                pass

            # Recursión: aplica estilo a hijos también
            if widget.winfo_children():
                self._aplicar_estilo_pantalla(widget)

    # ==============================
    # Manejo de sesión
    # ==============================
    def iniciar_sesion(self, usuario):
        self.usuario_actual = usuario
        self.cambiar_pantalla("clientes")  # pantalla inicial

    def cerrar_sesion(self):
        self.usuario_actual = None
        if self.menu_lateral:
            self.menu_lateral.destroy()
            self.menu_lateral = None

        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        self.cambiar_pantalla("Login")


# ==============================
# Ejecutar aplicación
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
