import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from postgrest.exceptions import APIError

from Core.UserManager import UserManager
from Core.Session import Session
from GUI.Form.UserForm import UserFormModal
from Models.User import User


class UserView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_id = ""
        self.can_manage = Session.get_session().has_role("admin")

        tb.Label(self, text="Gestion de Usuarios", font=("Helvetica", 20, "bold")).pack(pady=20)

        self.coldata = [
            {"text": "Usuario", "stretch": False},
            {"text": "Nombre", "stretch": True},
            {"text": "Apellidos", "stretch": True},
            {"text": "Tipo", "stretch": True},
        ]

        self.dt = Tableview(
            master=self,
            coldata=self.coldata,
            rowdata=self.get_rowdata(),
            paginated=True,
            searchable=True,
            bootstyle="info",
            pagesize=10,
            stripecolor=(None, "#5c5b5b"),
        )
        self.dt.align_column_center()
        self.dt.pack(fill=BOTH, expand=True, padx=20, pady=10)

        frame_actions = tb.Frame(self)
        frame_actions.pack(fill=X, padx=20, pady=10)
        tb.Button(frame_actions, text="Crear usuario", bootstyle="outline-success", command=self.create_user).pack(side=LEFT, padx=5)
        if self.can_manage:
            tb.Button(frame_actions, text="Editar usuario", bootstyle="outline-primary", command=self.edit_user).pack(side=LEFT, padx=5)
            tb.Button(frame_actions, text="Eliminar usuario", bootstyle="outline-danger", command=self.delete_user).pack(side=RIGHT, padx=5)

    def get_rowdata(self):
        try:
            response = UserManager.get_all_users()
            return [
                (
                    item.get_nickname(),
                    item.get_first_name(),
                    item.get_last_name(),
                    item.get_user_type().get_type_name() if item.get_user_type() else "",
                )
                for item in response.get_data()
            ]
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al cargar los datos {e}", "Error")
        return []

    def refresh_table(self):
        self.dt.build_table_data(self.coldata, self.get_rowdata())

    def save_info(self, data: User | None = None, create=True):
        try:
            response = UserManager.create_user(data) if create else UserManager.update_user(self.current_id, data)
            Messagebox.show_info(response.get_message(), "Exito")
            self.refresh_table()
            return True
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"{e}", "Error")
        return False

    def create_user(self):
        UserFormModal(self, "Crear usuario", self.save_info)

    def edit_user(self):
        if not self.can_manage:
            return
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Ningun usuario seleccionado", "Advertencia")
            return
        values = self.dt.view.item(selection[0], "values")
        self.current_id = values[0]
        try:
            response = UserManager.get_all_users()
            user = next((item for item in response.get_data() if item.get_nickname() == values[0]), None)
            UserFormModal(self, "Editar usuario", self.save_info, user)
        except Exception as e:
            Messagebox.show_error(f"No se pudo cargar el usuario {e}", "Error")

    def delete_user(self):
        if not self.can_manage:
            return
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Ningun usuario seleccionado", "Advertencia")
            return
        values = self.dt.view.item(selection[0], "values")
        answer = Messagebox.yesno(message=f"Desea eliminar el usuario: {values[0]}", title="Eliminar usuario", alert=True)
        if answer == "Sí":
            try:
                response = UserManager.delete_user(values[0])
                Messagebox.show_info(response.get_message(), "Exito")
                self.refresh_table()
            except Exception as e:
                Messagebox.show_error(f"{e}", "Error")
