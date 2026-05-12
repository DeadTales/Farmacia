import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from Models.Product.Mark import Mark
from Models.Vendor import Vendor
from Core.VendorManager import VendorManager

class MarkFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, mark_data:Mark | None=None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = mark_data
        self.create = True

        self.grab_set() 
        self.geometry("600x800")
        self.resizable(False, False)
        
        self.place_window_center()

        self.create_widgets(mark_data)

    def create_widgets(self, data: Mark):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        

        tb.Label(container, text="Datos de la marca", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Entradas
        tb.Label(container, text="ID:").pack(anchor=W)
        self.ent_id = tb.Entry(container)
        self.ent_id.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre:").pack(anchor=W)
        self.ent_name = tb.Entry(container)
        self.ent_name.pack(fill=X, pady=5)

        self.map_vendors = {}
        list_vendors = []
        texts = []
        try:
            response = VendorManager.get_all_vendors()

            if response:
                for item in response.get_data():
                    list_vendors.append((
                            item.name,
                            item.vendor_id
                        )
                    )

                texts = [text for text, value in list_vendors]
                self.map_vendors = dict(list_vendors)

        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")


        tb.Label(container, text="Proveedor:").pack(anchor=W)
        self.ent_vendor = tb.Combobox(
            container, 
            values=texts,
            state=READONLY
        )
        self.ent_vendor.pack(fill=X, pady=5)

        # Edicion
        if data:
            self.ent_id.insert(0, data.get_mark_id())
            self.ent_id.configure(state=DISABLED)
            self.ent_name.insert(0, data.get_name())
            vendor_name = data.vendor.get_name()
            
            if vendor_name:
                idx = texts.index(vendor_name)
                self.ent_vendor.current(idx) 
            self.create = False

        # Botones
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)

        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)


    def send(self):
        vendor_name = self.ent_vendor.get()

        payload = Mark(
            mark_id= None if not self.ent_id.get() else self.ent_id.get(),
            name=self.ent_name.get(),
            vendor = Vendor(
                vendor_id = self.map_vendors.get(vendor_name), 
                name= vendor_name
            )
        )

        if self.callback(payload, self.create):
            self.destroy()