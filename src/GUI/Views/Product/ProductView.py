import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from GUI.Form.VendorForm import VendorFormModal
from Models.Vendor import Vendor
from Core.VendorManager import VendorManager
from Core.Response import Response


class ProductView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title_lbl = tb.Label(self, text="Gestión de Inventario", font=("Helvetica", 18, "bold"))
        self.title_lbl.pack(pady=10)

        # 1. Crear el Notebook (Pestañas)
        self.nb = tb.Notebook(self, bootstyle="primary")
        self.nb.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # 2. Definir los marcos para cada pestaña
        self.tab_products = tb.Frame(self.nb, padding=10)
        self.tab_medicines = tb.Frame(self.nb, padding=10)
        self.tab_marks = tb.Frame(self.nb, padding=10)

        # 3. Agregar pestañas al Notebook
        self.nb.add(self.tab_products, text="📦 Productos Generales")
        self.nb.add(self.tab_medicines, text="💊 Medicamentos")
        self.nb.add(self.tab_marks, text="🏷️ Marcas")

        # 4. Inicializar el contenido de cada pestaña
        self.setup_products_tab()
        self.setup_medicines_tab()
        self.setup_marks_tab()

    # --- PESTAÑA PRODUCTOS ---
    def setup_products_tab(self):
        columns = [
            {"text": "Barcode", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Stock", "stretch": False},
            {"text": "Categoría", "stretch": True}
        ]
        self.dt_prod = Tableview(master=self.tab_products, 
                                 coldata=columns, 
                                 paginated=True, 
                                 searchable=True, 
                                 bootstyle="info")
        
        self.dt_prod.pack(fill=BOTH, expand=True)
        
        btn_frame = tb.Frame(self.tab_products)
        btn_frame.pack(fill=X, pady=10)

        btn_new = tb.Button(
            btn_frame, 
            text="Crear nuevo producto",
            bootstyle="outline-success"
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar producto",
            bootstyle="outline-primary"
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar producto",
            bootstyle="outline-danger"
        )
        btn_delete.pack(side=RIGHT, pady=5)
    
    # --- PESTAÑA MEDICAMENTOS ---
    def setup_medicines_tab(self):
        # Aquí mostramos columnas específicas de MEDICINE + PRODUCT (JOIN)
        columns = [
            {"text": "Barcode", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Sustancia Activa", "stretch": True},
            {"text": "Concentración", "stretch": True},
            {"text": "Receta", "stretch": False}
        ]
        self.dt_med = Tableview(master=self.tab_medicines, 
                                coldata=columns, 
                                paginated=True, 
                                searchable=True, 
                                bootstyle="info")
        
        self.dt_med.pack(fill=BOTH, expand=True)

        btn_frame = tb.Frame(self.tab_medicines)
        btn_frame.pack(fill=X, pady=10)
        btn_new = tb.Button(
            btn_frame, 
            text="Crear medicamento",
            bootstyle="outline-success"
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar medicamento",
            bootstyle="outline-primary"
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar medicamento",
            bootstyle="outline-danger",
        )
        btn_delete.pack(side=RIGHT, pady=5)

    # --- PESTAÑA MARCAS ---
    def setup_marks_tab(self):
        columns = [
            {"text": "ID", "stretch": False},
            {"text": "Nombre de Marca", "stretch": True},
            {"text": "Proveedor (Vendor)", "stretch": True}
        ]
        self.dt_marks = Tableview(master=self.tab_marks, 
                                  coldata=columns, 
                                  paginated=True, 
                                  searchable=True, 
                                  bootstyle="info")
        
        self.dt_marks.pack(fill=BOTH, expand=True)

        btn_frame = tb.Frame(self.tab_marks)
        btn_frame.pack(fill=X, pady=10)
        btn_new = tb.Button(
            btn_frame, 
            text="Crear marca",
            bootstyle="outline-success"
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar marca",
            bootstyle="outline-primary"
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar marca",
            bootstyle="outline-danger",
        )
        btn_delete.pack(side=RIGHT, pady=5)