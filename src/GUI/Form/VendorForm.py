import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from Models.Vendor import Vendor
from Core.VendorManager import VendorManager
from Core.Commons import validate_email

class VendorFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, vendor_data:Vendor | None=None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = vendor_data
        self.create = True

        self.grab_set() 
        self.geometry("600x800")
        self.resizable(False, False)
        
        self.place_window_center()

        self.create_widgets(vendor_data)

    def create_widgets(self, data: Vendor):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        

        tb.Label(container, text="Datos del proveedor", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Entradas
        tb.Label(container, text="ID:").pack(anchor=W)
        self.ent_id = tb.Entry(container)
        self.ent_id.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre:").pack(anchor=W)
        self.ent_name = tb.Entry(container)
        self.ent_name.pack(fill=X, pady=5)


        tb.Label(container, text="Telefono:").pack(anchor=W)
        self.ent_phone = tb.Entry(container)
        self.ent_phone.pack(fill=X, pady=5)

        tb.Label(container, text="Email:").pack(anchor=W)
        self.ent_email = tb.Entry(container)

        v_email = (container.register(lambda p: validate_email(p, self.ent_email)), '%P') 
        self.ent_email.configure(validate="key", 
                                  validatecommand=v_email
                                )
        self.ent_email.pack(fill=X, pady=5)


        # Edicion
        if data:
            self.ent_id.insert(0, data.get_vendor_id())
            self.ent_id.configure(state="disabled")
            self.ent_name.insert(0, data.get_name())
            self.ent_phone.insert(0, data.get_phone())
            self.ent_email.insert(0, data.get_email())
            self.create = False

        # Botones
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)

        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)

    def send(self):
        
        payload = Vendor(
            vendor_id=self.ent_id.get().upper(),
            name=self.ent_name.get(),
            phone=self.ent_phone.get(),
            email=self.ent_email.get()
        )

        if self.callback(payload, self.create):
            self.destroy()