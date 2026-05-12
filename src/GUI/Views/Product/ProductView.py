import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from GUI.Form.Product import *
from Models.Vendor import Vendor
from Models.Product import *
from Core.Product import *
from Core.Response import Response

class ProductView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.current_id = ""

        self.title_lbl = tb.Label(self, text="Gestión de Inventario", font=("Helvetica", 18, "bold"))
        self.title_lbl.pack(pady=10)

        self.nb = tb.Notebook(self, bootstyle="primary")
        self.nb.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tab_products = tb.Frame(self.nb, padding=10)
        self.tab_medicines = tb.Frame(self.nb, padding=10)
        self.tab_marks = tb.Frame(self.nb, padding=10)

        self.nb.add(self.tab_products, text="Productos Generales")
        self.nb.add(self.tab_medicines, text="Medicamentos")
        self.nb.add(self.tab_marks, text="Marcas")

        self.setup_products_tab()
        self.setup_medicines_tab()
        self.setup_marks_tab()

        self.nb.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        selected_index = self.nb.index("current")

        if selected_index ==0:
            self.load_product()
        elif selected_index == 1:
            self.load_medicine()
        elif selected_index == 2:
            self.load_mark()

    def setup_products_tab(self):
        self.cols_products = [
            {"text": "Barcode", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Stock", "stretch": False},
            {"text": "Categoría", "stretch": True}
        ]
        self.dt_prod = Tableview(master=self.tab_products, 
                                 coldata=self.cols_products, 
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

    def setup_medicines_tab(self):
        self.cols_medicines = [
            {"text": "Barcode", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Sustancia Activa", "stretch": True},
            {"text": "Concentración", "stretch": True},
            {"text": "Receta", "stretch": False}
        ]
        self.dt_med = Tableview(master=self.tab_medicines, 
                                coldata=self.cols_medicines, 
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

    def setup_marks_tab(self):
        self.cols_marks = [
            {"text": "ID", "stretch": False},
            {"text": "Nombre de Marca", "stretch": True},
            {"text": "Proveedor", "stretch": True},
            {"text": "Vendor_ID", "stretch": False}
        ]

        self.dt_marks = Tableview(master=self.tab_marks, 
                                  coldata=self.cols_marks, 
                                  paginated=True, 
                                  searchable=True, 
                                  bootstyle="info")
        
        
        self.dt_marks.hide_selected_column(cid=3)
        self.dt_marks.pack(fill=BOTH, expand=True)

        btn_frame = tb.Frame(self.tab_marks)
        btn_frame.pack(fill=X, pady=10)
        btn_new = tb.Button(
            btn_frame, 
            text="Crear marca",
            bootstyle="outline-success",
            command=self.create_mark
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar marca",
            bootstyle="outline-primary",
            command=self.edit_mark
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar marca",
            bootstyle="outline-danger",
            command=self.delete_mark
        )
        btn_delete.pack(side=RIGHT, pady=5)

    
    #product_space
    def load_product():
        pass


    #medicine space
    def load_medicine():
        pass


    #mark space
    def load_mark(self):

        try:
            response = MarkManager.get_all_marks()

            rowdata = []

            for item in response.get_data():
                rowdata.append((
                        item.mark_id,
                        item.name,
                        item.vendor.get_name(),
                        item.vendor.get_vendor_id()
                    )
                )
            
            self.dt_marks.build_table_data(self.cols_marks, rowdata)
            self.dt_marks.hide_selected_column(cid=3)
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")
    
    
    def save_mark(self, data:Mark | None = None, create = True):
        try:
            if create:
                respone = MarkManager.create_mark(data)
            else:
                respone = MarkManager.update_mark(self.current_id, data)

            Messagebox.show_info(respone.get_message(), "Exito")
            self.load_mark()
            return True
        except ValueError as e:
            print(f"Error valor: {e}")
            Messagebox.show_error(e, "Error")
            return False
        except APIError as e:
            print(f"Error API: {e.message}")
            Messagebox.show_error(e.message, "Error")
            return False
        except Exception as e:
            print(f"Error Desconocido: {e}")
            Messagebox.show_error(f"{e}", "Error")
            return False        

    def create_mark(self):
        MarkFormModal(
            self, 
            "Crear marca", 
            self.save_mark
        )

    def edit_mark(self):
        selection = self.dt_marks.view.selection()

        if not selection:
            Messagebox.show_warning("Ninguna marca seleccionada", "Advertencia")
            return
        
        item_id = selection[0]
        values = self.dt_marks.view.item(item_id, 'values')
        self.current_id = values[0]

        # Reconstruimos el objeto con lo que ya hay en la tabla
        mark = Mark(
            mark_id = values[0],
            name = values[1],
            vendor = Vendor(name= values[2], vendor_id= values[3])
        )

        MarkFormModal(
            self,
            "Editar marca",
            self.save_mark,
            mark
        )



    def delete_mark(self):
        selection = self.dt_marks.view.selection()

        if not selection:
            Messagebox.show_warning(f"Ninguna marca seleccionada", "Advertencia")
            return

        item_id =  selection[0]

        values = self.dt_marks.view.item(item_id, 'values')

        answer = Messagebox.yesno(
            message=f"Desea eliminar la marca: {values[0]}",
            title="Eliminar marca",
            alert=True
        )

        if answer == "Sí":
            response = MarkManager.delete_mark(values[0])
            Messagebox.show_info(response.get_message(), "Exito")
            self.load_mark()
