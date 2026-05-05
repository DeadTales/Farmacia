from ttkbootstrap.constants import *
from GUI.Views.LoginView import LogInView
from GUI.Views.HomeView import HomeView
from GUI.Views.VendorView import VendorView

class Router:
    def __init__(self, root):
        self.root = root
        self.current_win = None

        pass
    def show_login(self):
        self.clear_root()
        login = LogInView(self.root, self.show_home)
        
        login.pack(expand=True)

    def show_home(self):
        self.clear_root()

        self.current_win = HomeView(self.root, router=self)
        self.current_win.pack(fill="both", expand=True)
    
    def nav_to_home(self):
        pass
    
    def nav_to_users(self):
        pass

    def nav_to_clients(self):
        pass

    def nav_to_products(self):
        pass

    def nav_to_sales(self):
        pass

    def nav_to_vendor(self):
        if self.current_win:
            self.clear_win()
        
            view = VendorView(self.current_win.content_area)
            view.pack(fill="both", expand=True)

    def nav_to_purchase(self):
        pass
    
    def nav_to_reports(self):
        pass

    def clear_win(self):
        if self.current_win is not None:
            for widget in self.current_win.content_area.winfo_children():
                widget.destroy()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_win = None

    def get_dictionary(self):
        return {"Usuarios": lambda: self.nav_to_users(), "Clientes": lambda: self.nav_to_clients(), 
                    "Productos" : lambda: self.nav_to_products(), "Ventas": lambda: self.nav_to_sales(), 
                    "Proveedores": lambda: self.nav_to_vendor(), "Compras": lambda: self.nav_to_purchase(), 
                    "Reportes": lambda: self.nav_to_reports(), "Inicio": lambda: self.nav_to_home()}