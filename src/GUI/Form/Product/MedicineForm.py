
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from Models.Product import *
from Core.Product import *
from Core.Commons import validate_number

class MedicineFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, medicine_data: Medicine | None = None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = medicine_data
        self.create = True

        self.grab_set()
        self.geometry("600x900")
        self.resizable(False, False)
        self.place_window_center()

        self.create_widgets(medicine_data)

    def create_widgets(self, data: Medicine):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        tb.Label(container, text="Datos del Medicamento", font=("Helvetica", 14, "bold")).pack(pady=10)

        # --- CAMPOS HEREDADOS DE PRODUCT ---
        tb.Label(container, text="Código de barras:").pack(anchor=W)
        self.ent_id = tb.Entry(container)
        self.ent_id.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre Comercial:").pack(anchor=W)
        self.ent_name = tb.Entry(container)
        self.ent_name.pack(fill=X, pady=5)

        tb.Label(container, text="Descripción:").pack(anchor=W)
        self.ent_description = tb.Entry(container)
        self.ent_description.pack(fill=X, pady=5)

        # --- CAMPOS ESPECÍFICOS DE MEDICINE ---
        tb.Label(container, text="Sustancia Activa:").pack(anchor=W)
        self.ent_active = tb.Entry(container)
        self.ent_active.pack(fill=X, pady=5)

        tb.Label(container, text="Concentración (ej. 500mg):").pack(anchor=W)
        self.ent_concentration = tb.Entry(container)
        self.ent_concentration.pack(fill=X, pady=5)

        tb.Label(container, text="Presentación:").pack(anchor=W)
        self.ent_presentation = tb.Combobox(container, values=["Tabletas", "Jarabe", "Inyectable", "Cápsulas", "Pomada"], state=READONLY)
        self.ent_presentation.pack(fill=X, pady=5)

        self.var_prescription = tb.BooleanVar()
        self.chk_prescription = tb.Checkbutton(container, text="Requiere Receta Médica", variable=self.var_prescription, bootstyle="round-toggle")
        self.chk_prescription.pack(anchor=W, pady=10)

        # --- STOCK ---
        v_number = container.register(validate_number)
        tb.Label(container, text="Stock:").pack(anchor=W)
        self.ent_stock = tb.Spinbox(container, from_=0, to=1000, validate="key", validatecommand=(v_number, '%P'))
        self.ent_stock.pack(fill=X, pady=5)

        tb.Label(container, text="Precio:").pack(anchor=W)
        self.ent_price = tb.Entry(container, validate="key", validatecommand=(v_number, '%P'))
        self.ent_price.pack(fill=X, pady=5)

        self.FIXED_CATEGORY_ID = 1
        self.FIXED_CATEGORY_NAME = "Medicamentos"
            
        tb.Label(container, text="Categoría:").pack(anchor=W)
        lbl_cat = tb.Label(container, text=self.FIXED_CATEGORY_NAME, bootstyle="secondary")
        lbl_cat.pack(anchor=W, pady=5)

        # --- MARCAS ---
        self.map_marks = {}
        texts_marks = []
        try:
            resp_mark = MarkManager.get_all_marks()
            if resp_mark:
                list_m = [(item.name, item.mark_id) for item in resp_mark.get_data()]
                texts_marks = [t for t, v in list_m]
                self.map_marks = dict(list_m)
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")

        tb.Label(container, text="Marca:").pack(anchor=W)
        self.ent_mark = tb.Combobox(container, values=texts_marks, state=READONLY)
        self.ent_mark.pack(fill=X, pady=5)

        # --- LÓGICA DE EDICIÓN ---
        if data:
            self.ent_id.insert(0, data.barcode)
            self.ent_id.configure(state=DISABLED)
            self.ent_name.insert(0, data.name)
            self.ent_description.insert(0, data.description)
            self.ent_active.insert(0, data.active_ingredient)
            self.ent_concentration.insert(0, data.concentration)
            self.ent_presentation.set(data.presentation)
            self.var_prescription.set(data.prescription)
            self.ent_stock.delete(0, END)
            self.ent_stock.insert(0, data.stock)
            self.ent_price.insert(0, data.price or 0)
   
            if data.mark: self.ent_mark.set(data.mark.get_name())
            
            self.create = False

        # Botones
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)

    def send(self):
        mark_name = self.ent_mark.get()

        # Creamos el objeto Medicine con TODOS los parámetros
        payload = Medicine(
            barcode=self.ent_id.get(),
            name=self.ent_name.get(),
            description=self.ent_description.get(),
            stock=int(float(self.ent_stock.get() or 0)),
            price=float(self.ent_price.get() or 0),
            mark=Mark(
                mark_id=self.map_marks.get(mark_name), 
                name=mark_name
            ),
            is_active=True,
            
            active_ingredient=self.ent_active.get(),
            concentration=self.ent_concentration.get(),
            presentation=self.ent_presentation.get(),
            prescription=self.var_prescription.get()
        )

        if self.callback(payload, self.create):
            self.destroy()
