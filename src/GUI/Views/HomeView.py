import ttkbootstrap as tb


class HomeView(tb.Frame):
    def __init__(self, master, router, **kwargs):
        super().__init__(master, **kwargs)
        self.router = router
        
        #el router es para pasarlo al navbar y permitir acceder a propiedades de la clase Router
        
        # Este es el contenedor donde realmente cambiarán las tablas/formularios
        self.content_area = tb.Frame(self, padding=20)
        self.content_area.pack(fill="both", expand=True)
        
        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        tb.Label(
            self.content_area, 
            text="Bienvenido Farmacias Sí", 
            font=("Helvetica", 20)
        ).pack(pady=50)
