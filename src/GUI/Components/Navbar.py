import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

from Core.Session import Session


class Navbar(tb.Frame):
    def __init__(self, master, router, **kwargs):
        super().__init__(master, bootstyle="primary", padding=5, **kwargs)
        self.router = router
        self.pack(side=TOP, fill=X)
        self.create_buttons()

    
    def load_icon(self, ruta, size=(24, 24)):
        try:
            img_open = Image.open(ruta)
            img_resized = img_open.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error cargando icono en {ruta}: {e}")
            return None

    def create_buttons(self):
                
        options = ["Inicio", "Usuarios", "Clientes", "Productos", "Ventas", "Proveedores", "Compras", "Reportes"]

        
        fns = self.router.get_dictionary()
        session = Session.get_session()
        
        for item in options:
            if item != "Inicio" and not session.has_permission(item):
                continue
            btn = tb.Button(
                self, 
                text=item, 
                bootstyle="secondary",
                command=lambda name=item: fns[name]()
            )
            btn.pack(side=LEFT, padx=2)

        # Botón Salir
        tb.Button(
            self, 
            text="Salir", 
            bootstyle="danger", 
            command=self.router.log_out
        ).pack(side=RIGHT, padx=5)
