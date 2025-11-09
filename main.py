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

        # 🔹 Carga del icono (debe existir en la carpeta)
        icono = tk.PhotoImage(file="C:/Users/palom/OneDrive/Desktop/TALLERMECANICO/imagenes/iconoTOq.png")
        self.root.iconphoto(False, icono)


        # 🔹 Ajustar ventana a la pantalla completa
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state("zoomed")
        self.root.resizable(True, True)

        self.usuario_actual = None
        self.pantalla_actual = None
        self.mostrar_login()

    def cambiar_pantalla(self, nueva_pantalla, *args):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()

        self.pantalla_actual = tk.Frame(self.root)
        self.pantalla_actual.pack(fill="both", expand=True)

        if nueva_pantalla == "Login":
            Login(self.pantalla_actual, self)
        elif nueva_pantalla == "menu":
            MenuPrincipal(self.pantalla_actual, self)
        elif nueva_pantalla == "clientes":
            Clientes(self.pantalla_actual, self)
        elif nueva_pantalla == "vehiculos":
            Vehiculos(self.pantalla_actual, self)
        elif nueva_pantalla == "inventario":
            Inventario(self.pantalla_actual, self)
        elif nueva_pantalla == "ordenes":
            OrdenesServicio(self.pantalla_actual, self)
        elif nueva_pantalla == "facturacion":
            Facturacion(self.pantalla_actual, self)
        elif nueva_pantalla == "citas":
            Citas(self.pantalla_actual, self)
        elif nueva_pantalla == "reportes":
            Reportes(self.pantalla_actual, self)
        elif nueva_pantalla == "configuracion":
            Configuracion(self.pantalla_actual, self.usuario_actual, self)

    def mostrar_login(self):
        self.cambiar_pantalla("Login")

    def iniciar_sesion(self, usuario):
        self.usuario_actual = usuario
        self.cambiar_pantalla("menu")

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.cambiar_pantalla("Login")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
