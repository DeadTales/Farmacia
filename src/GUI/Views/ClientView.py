import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from postgrest.exceptions import APIError

from Core.ClientManager import ClientManager
from Core.Session import Session
from GUI.Form.ClientForm import ClientFormModal
from Models.Client import Client


class ClientView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_id = ""
        self.can_manage = Session.get_session().has_role("admin", "gerente")

        tb.Label(self, text="Gestion de Clientes", font=("Helvetica", 20, "bold")).pack(pady=20)

        self.coldata = [
            {"text": "Email", "stretch": False, "width": 220},
            {"text": "Nombre", "stretch": False, "width": 150},
            {"text": "Apellidos", "stretch": False, "width": 180},
            {"text": "RFC", "stretch": False},
            {"text": "Telefono", "stretch": False, "width": 130},
            {"text": "Puntos", "stretch": False},
            {"text": "Direccion", "stretch": True, "width": 520},
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
        self.center_columns()

        frame_actions = tb.Frame(self)
        frame_actions.pack(fill=X, padx=20, pady=10)
        tb.Button(frame_actions, text="Registrar cliente", bootstyle="outline-success", command=self.create_client).pack(side=LEFT, padx=5)
        if self.can_manage:
            tb.Button(frame_actions, text="Editar cliente", bootstyle="outline-primary", command=self.edit_client).pack(side=LEFT, padx=5)
            tb.Button(frame_actions, text="Eliminar cliente", bootstyle="outline-danger", command=self.delete_client).pack(side=RIGHT, padx=5)

    def get_rowdata(self):
        try:
            response = ClientManager.get_all_clients()
            return [
                (
                    item.get_email(),
                    item.get_first_name(),
                    item.get_last_name(),
                    item.get_rfc() or "",
                    item.get_phone(),
                    item.get_points(),
                    self.format_address(item.get_address()),
                )
                for item in response.get_data()
            ]
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al cargar los datos {e}", "Error")
        return []

    def format_address(self, address):
        if hasattr(address, "get_settlement"):
            settlement = address.get_settlement()
            city = settlement.get_cat_city() if settlement else None
            state = city.get_cat_state() if city else None
            parts = [
                address.get_street(),
                address.get_ext_num(),
                settlement.get_name() if settlement else "",
                city.get_name() if city else "",
                state.get_name() if state else "",
            ]
            return ", ".join([part for part in parts if part])
        if not isinstance(address, dict):
            return ""
        parts = [
            address.get("street", ""),
            address.get("external_number", ""),
            address.get("settlement", ""),
            address.get("city", ""),
            address.get("state", ""),
            address.get("postal_code", ""),
        ]
        return ", ".join([part for part in parts if part])

    def refresh_table(self):
        self.dt.build_table_data(self.coldata, self.get_rowdata())
        self.center_columns()

    def center_columns(self):
        for i in range(len(self.coldata)):
            self.dt.view.column(i, anchor=CENTER)
            self.dt.view.heading(i, anchor=CENTER)

    def save_info(self, data: Client | None = None, create=True):
        try:
            response = ClientManager.create_client(data) if create else ClientManager.update_client(self.current_id, data)
            Messagebox.show_info(response.get_message(), "Exito")
            self.refresh_table()
            return True
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"{e}", "Error")
        return False

    def create_client(self):
        ClientFormModal(self, "Registrar cliente", self.save_info)

    def edit_client(self):
        if not self.can_manage:
            return
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Ningun cliente seleccionado", "Advertencia")
            return
        values = self.dt.view.item(selection[0], "values")
        self.current_id = values[0]
        try:
            response = ClientManager.get_all_clients()
            client = next((item for item in response.get_data() if item.get_email() == values[0]), None)
            ClientFormModal(self, "Editar cliente", self.save_info, client)
        except Exception as e:
            Messagebox.show_error(f"No se pudo cargar el cliente {e}", "Error")

    def delete_client(self):
        if not self.can_manage:
            return
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Ningun cliente seleccionado", "Advertencia")
            return
        values = self.dt.view.item(selection[0], "values")
        answer = Messagebox.yesno(message=f"Desea eliminar el cliente: {values[0]}", title="Eliminar cliente", alert=True)
        if answer == "Sí":
            try:
                response = ClientManager.delete_client(values[0])
                Messagebox.show_info(response.get_message(), "Exito")
                self.refresh_table()
            except Exception as e:
                Messagebox.show_error(f"{e}", "Error")
