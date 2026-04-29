from ttkbootstrap.constants import *
from GUI.Views.LoginView import LogInView
from GUI.Views.HomeView import HomeView

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


    def clear_win(self):
        if self.current_win is not None:
            for widget in self.current_win.content_area.winfo_children():
                widget.destroy()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_win = None