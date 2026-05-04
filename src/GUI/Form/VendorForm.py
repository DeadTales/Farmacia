import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from Models.Vendor import Vendor
from Core.VendorManager import VendorManager
#from Core.Commons import validate_number

class VendorFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, piece_data:Piece | None=None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = piece_data
        self.create = True

        self.grab_set() 
        self.geometry("600x800")
        self.resizable(False, False)
        
        self.place_window_center()

        self.create_widgets(piece_data)

    def create_widgets(self, data: Piece):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        v_number = container.register(validate_number)

        tb.Label(container, text="Datos de la pieza", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Entradas
        tb.Label(container, text="Folio:").pack(anchor=W)
        self.ent_folio = tb.Entry(container)
        self.ent_folio.pack(fill=X, pady=5)

        tb.Label(container, text="Descripción:").pack(anchor=W)
        self.ent_description = tb.Entry(container)
        self.ent_description.pack(fill=X, pady=5)


        tb.Label(container, text="Número de serie:").pack(anchor=W)
        self.ent_num = tb.Entry(container)
        self.ent_num.pack(fill=X, pady=5)

        tb.Label(container, text="Precio:").pack(anchor=W)
        self.ent_price = tb.Entry(container, validate="key", 
                                  validatecommand=(v_number, '%P'))
        self.ent_price.pack(fill=X, pady=5)

        tb.Label(container, text="Cantidad:").pack(anchor=W)
        self.ent_stock = tb.Spinbox(
            container,
            from_=0,
            to=1000,
            increment=1,
            bootstyle="info",
            validate="key",
            validatecommand=(v_number, '%P')
        )
        self.ent_stock.pack(fill=X, pady=5)

        # Edicion
        if data:
            self.ent_folio.insert(0, data.folio)
            self.ent_description.insert(0, data.description)
            self.ent_num.insert(0, data.serial_number)
            self.ent_price.insert(0, data.price)
            self.ent_stock.insert(0, data.stock)
            self.create = False

        # Botones
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)

        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)

    def send(self):
        
        payload = Piece(
            folio=self.ent_folio.get(),
            description=self.ent_description.get(),
            serial_number=self.ent_num.get(),
            price=float(self.ent_price.get()),
            stock=int(self.ent_stock.get())
        )

        if self.callback(payload, self.create):
            self.destroy()