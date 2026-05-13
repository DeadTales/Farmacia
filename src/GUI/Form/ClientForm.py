import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from Core.Commons import validate_email, validate_number
from Models.Client import Client
from Services.AddressApiService import AddressApiService


class ClientFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, client_data: Client | None = None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = client_data
        self.create = True

        self.grab_set()
        self.geometry("720x880")
        self.minsize(680, 720)
        self.resizable(True, True)
        self.place_window_center()
        self.create_widgets(client_data)

    def create_widgets(self, data: Client):
        outer = tb.Frame(self)
        outer.pack(fill=BOTH, expand=True)

        canvas = tb.Canvas(outer, highlightthickness=0)
        scrollbar = tb.Scrollbar(outer, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        container = tb.Frame(canvas, padding=20)
        window_id = canvas.create_window((0, 0), window=container, anchor=NW)
        container.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        canvas.bind("<Enter>", lambda event: canvas.bind("<MouseWheel>", self._on_mousewheel))
        canvas.bind("<Leave>", lambda event: canvas.unbind("<MouseWheel>"))
        container.bind("<Enter>", lambda event: canvas.bind("<MouseWheel>", self._on_mousewheel))
        container.bind("<Leave>", lambda event: canvas.unbind("<MouseWheel>"))
        self._scroll_canvas = canvas

        tb.Label(container, text="Datos del cliente", font=("Helvetica", 14, "bold")).pack(pady=10)

        tb.Label(container, text="Email:").pack(anchor=W)
        self.ent_email = tb.Entry(container)
        self.ent_email.configure(validate="key", validatecommand=(container.register(lambda p: validate_email(p, self.ent_email)), "%P"))
        self.ent_email.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre:").pack(anchor=W)
        self.ent_first_name = tb.Entry(container)
        self.ent_first_name.pack(fill=X, pady=5)

        tb.Label(container, text="Apellidos:").pack(anchor=W)
        self.ent_last_name = tb.Entry(container)
        self.ent_last_name.pack(fill=X, pady=5)

        tb.Label(container, text="RFC:").pack(anchor=W)
        self.ent_rfc = tb.Entry(container)
        self.ent_rfc.pack(fill=X, pady=5)

        tb.Label(container, text="Telefono:").pack(anchor=W)
        self.ent_phone = tb.Entry(container)
        self.ent_phone.pack(fill=X, pady=5)

        tb.Label(container, text="Puntos:").pack(anchor=W)
        self.ent_points = tb.Spinbox(container, from_=0, to=999999, validate="key", validatecommand=(container.register(validate_number), "%P"))
        self.ent_points.pack(fill=X, pady=5)

        tb.Separator(container).pack(fill=X, pady=12)
        tb.Label(container, text="Direccion", font=("Helvetica", 12, "bold")).pack(anchor=W, pady=4)

        cp_frame = tb.Frame(container)
        cp_frame.pack(fill=X, pady=5)
        tb.Label(cp_frame, text="C.P.:").pack(side=LEFT)
        self.ent_cp = tb.Entry(cp_frame, width=12)
        self.ent_cp.pack(side=LEFT, padx=5)
        tb.Button(cp_frame, text="Buscar", bootstyle="info-outline", command=self.search_postal_code).pack(side=LEFT, padx=5)

        tb.Label(container, text="Estado:").pack(anchor=W)
        self.ent_state = tb.Entry(container)
        self.ent_state.pack(fill=X, pady=5)

        tb.Label(container, text="Municipio / ciudad:").pack(anchor=W)
        self.ent_city = tb.Entry(container)
        self.ent_city.pack(fill=X, pady=5)

        tb.Label(container, text="Colonia:").pack(anchor=W)
        self.ent_settlement = tb.Combobox(container, values=[])
        self.ent_settlement.pack(fill=X, pady=5)

        tb.Label(container, text="Calle:").pack(anchor=W)
        self.ent_street = tb.Entry(container)
        self.ent_street.pack(fill=X, pady=5)

        numbers = tb.Frame(container)
        numbers.pack(fill=X, pady=5)
        tb.Label(numbers, text="Num. ext.:").pack(side=LEFT)
        self.ent_ext_num = tb.Entry(numbers, width=16)
        self.ent_ext_num.pack(side=LEFT, padx=5)
        tb.Label(numbers, text="Num. int.:").pack(side=LEFT, padx=(10, 0))
        self.ent_int_num = tb.Entry(numbers, width=16)
        self.ent_int_num.pack(side=LEFT, padx=5)

        if data:
            self.ent_email.insert(0, data.get_email())
            self.ent_email.configure(state=DISABLED)
            self.ent_first_name.insert(0, data.get_first_name())
            self.ent_last_name.insert(0, data.get_last_name())
            self.ent_rfc.insert(0, data.get_rfc() or "")
            self.ent_phone.insert(0, data.get_phone())
            self.ent_points.delete(0, END)
            self.ent_points.insert(0, data.get_points() or 0)
            self.fill_address(data.get_address())
            self.create = False

        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)

    def search_postal_code(self):
        try:
            data = AddressApiService.get_by_postal_code(self.ent_cp.get())
            if not data["settlements"]:
                Messagebox.show_warning("No se encontro informacion para ese codigo postal", "Advertencia")
                return
            self.ent_state.delete(0, END)
            self.ent_state.insert(0, data["state"])
            self.ent_city.delete(0, END)
            self.ent_city.insert(0, data.get("city") or data.get("municipality") or "")
            self.ent_settlement.configure(values=data["settlements"])
            self.ent_settlement.set(data["settlements"][0])
        except Exception as e:
            Messagebox.show_error(f"No se pudo consultar el codigo postal: {e}", "Error")

    def fill_address(self, address):
        if hasattr(address, "get_settlement"):
            settlement = address.get_settlement()
            city = settlement.get_cat_city() if settlement else None
            state = city.get_cat_state() if city else None
            self.ent_state.insert(0, state.get_name() if state else "")
            self.ent_city.insert(0, city.get_name() if city else "")
            settlement_name = settlement.get_name() if settlement else ""
            self.ent_settlement.configure(values=[settlement_name] if settlement_name else [])
            self.ent_settlement.set(settlement_name)
            self.ent_street.insert(0, address.get_street() or "")
            self.ent_ext_num.insert(0, address.get_ext_num() or "")
            self.ent_int_num.insert(0, address.get_inter_num() or "")
            return
        if not isinstance(address, dict):
            return
        self.ent_cp.insert(0, address.get("postal_code", ""))
        self.ent_state.insert(0, address.get("state", ""))
        self.ent_city.insert(0, address.get("city", ""))
        settlement = address.get("settlement", "")
        self.ent_settlement.configure(values=[settlement] if settlement else [])
        self.ent_settlement.set(settlement)
        self.ent_street.insert(0, address.get("street", ""))
        self.ent_ext_num.insert(0, address.get("external_number", ""))
        self.ent_int_num.insert(0, address.get("internal_number", ""))

    def send(self):
        address = {
            "postal_code": self.ent_cp.get().strip(),
            "state": self.ent_state.get().strip(),
            "city": self.ent_city.get().strip(),
            "settlement": self.ent_settlement.get().strip(),
            "street": self.ent_street.get().strip(),
            "external_number": self.ent_ext_num.get().strip(),
            "internal_number": self.ent_int_num.get().strip(),
        }
        payload = Client(
            email=self.ent_email.get().strip(),
            first_name=self.ent_first_name.get().strip(),
            last_name=self.ent_last_name.get().strip(),
            rfc=self.ent_rfc.get().strip().upper(),
            phone=self.ent_phone.get().strip(),
            points=int(self.ent_points.get() or 0),
            address=address
        )

        if self.callback(payload, self.create):
            self.destroy()

    def _on_mousewheel(self, event):
        canvas = getattr(self, "_scroll_canvas", None)
        if canvas and canvas.winfo_exists():
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
