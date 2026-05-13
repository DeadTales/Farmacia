import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from Core.UserManager import UserManager
from Core.Session import Session
from Models.User import User
from Models.UserType import UserType


class UserFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, user_data: User | None = None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = user_data
        self.create = True
        self.map_user_types = {}

        self.grab_set()
        self.geometry("520x520")
        self.resizable(False, False)
        self.place_window_center()
        self.create_widgets(user_data)

    def create_widgets(self, data: User):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        tb.Label(container, text="Datos del usuario", font=("Helvetica", 14, "bold")).pack(pady=10)

        tb.Label(container, text="Usuario:").pack(anchor=W)
        self.ent_nickname = tb.Entry(container)
        self.ent_nickname.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre:").pack(anchor=W)
        self.ent_first_name = tb.Entry(container)
        self.ent_first_name.pack(fill=X, pady=5)

        tb.Label(container, text="Apellidos:").pack(anchor=W)
        self.ent_last_name = tb.Entry(container)
        self.ent_last_name.pack(fill=X, pady=5)

        tb.Label(container, text="Contraseña:").pack(anchor=W)
        self.ent_pswd = tb.Entry(container, show="*")
        self.ent_pswd.pack(fill=X, pady=5)

        type_names = self.load_user_types()
        tb.Label(container, text="Tipo de usuario:").pack(anchor=W)
        self.ent_user_type = tb.Combobox(container, values=type_names, state=READONLY)
        self.ent_user_type.pack(fill=X, pady=5)

        if data:
            self.ent_nickname.insert(0, data.get_nickname())
            self.ent_nickname.configure(state=DISABLED)
            self.ent_first_name.insert(0, data.get_first_name())
            self.ent_last_name.insert(0, data.get_last_name())
            self.ent_pswd.configure(bootstyle="secondary")
            user_type = data.get_user_type()
            if user_type:
                self.ent_user_type.set(user_type.get_type_name())
            self.create = False

        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)

    def load_user_types(self):
        try:
            response = UserManager.get_user_types()
            user_types = response.get_data()
            if Session.get_session().has_role("gerente"):
                user_types = [item for item in user_types if (item.get_type_name() or "").strip().lower() == "encargado"]
            pairs = [(item.get_type_name(), item.get_type_id()) for item in user_types]
            self.map_user_types = dict(pairs)
            return [name for name, value in pairs]
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al cargar tipos de usuario {e}", "Error")
        return []

    def send(self):
        type_name = self.ent_user_type.get()
        payload = User(
            nickname=self.ent_nickname.get().strip(),
            first_name=self.ent_first_name.get().strip(),
            last_name=self.ent_last_name.get().strip(),
            pswd=self.ent_pswd.get(),
            user_type=UserType(type_id=self.map_user_types.get(type_name), name=type_name)
        )

        if self.callback(payload, self.create):
            self.destroy()
