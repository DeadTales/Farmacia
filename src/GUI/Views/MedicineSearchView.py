import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from postgrest.exceptions import APIError

from Core.Product.ProductManager import ProductManager


class MedicineSearchView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        tb.Label(self, text="Busqueda de Productos", font=("Helvetica", 20, "bold")).pack(pady=20)

        self.coldata = [
            {"text": "Codigo", "stretch": False},
            {"text": "Nombre", "stretch": True},
            {"text": "Descripcion", "stretch": True},
            {"text": "Categoria", "stretch": True},
            {"text": "Stock", "stretch": False},
            {"text": "Precio", "stretch": False},
            {"text": "Marca", "stretch": True},
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

    def get_rowdata(self):
        try:
            response = ProductManager.get_all_products()
            return [
                (
                    item.barcode,
                    item.name,
                    item.description,
                    item.category.get_name() if item.category else "",
                    item.stock,
                    f"$ {float(item.price or 0):.2f}",
                    item.mark.get_name() if item.mark else "",
                )
                for item in response.get_data()
            ]
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al cargar los medicamentos {e}", "Error")
        return []
