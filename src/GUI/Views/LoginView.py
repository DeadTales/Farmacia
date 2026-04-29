import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from tkinter import messagebox
from Services.AuthService import verify_credentials
from Core.Session import Session

class LogInView(tkb.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, padding=30)
        self.on_login_success = on_login_success
        
        # --- UI ---
        tkb.Label(self, text="FARMACIAS Sí", font=("Helvetica", 16, "bold"), bootstyle=PRIMARY).pack(pady=10)
        
        tkb.Label(self, text="Nombre de Usuario:").pack(anchor=W)
        self.user_entry = tkb.Entry(self, font=("Helvetica", 12), placeholder= "Usuario")
        self.user_entry.pack(fill=X, pady=10)
        
        tkb.Label(self, text="Contraseña:").pack(anchor=W)
        self.pass_entry = tkb.Entry(self, show="*", font=("Helvetica", 12))
        self.pass_entry.pack(fill=X, pady=10)

        self.btn_login = tkb.Button(
            self, text="Iniciar Sesión", bootstyle=SUCCESS, 
            command=self.try_login, width=20
        )
        self.btn_login.pack(pady=20)

    def try_login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        
        try:
            user_data = verify_credentials(user, pw)
            Session().start_session(user_data)
            self.on_login_success()

        except ValueError as e:
            messagebox.showerror("Acceso Denegado", str(e))
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error tecnico", "No se pudo conectar con el servicio")
            