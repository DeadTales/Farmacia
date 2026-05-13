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
            {"text": "Descripción", "stretch": True},
            {"text": "Stock", "stretch": False},
            {"text": "Categoría", "stretch": True},
            {"text": "Marca", "stretch": True},
        ]

        self.dt_prod = Tableview(master=self.tab_products, 
                                 coldata=self.cols_products, 
                                 paginated=True, 
                                 searchable=True, 
                                 bootstyle="info")
        
        self.dt_prod.pack(fill=BOTH, expand=True)
        
        for i in range(len(self.cols_products)):
            self.dt_prod.view.column(i, anchor=CENTER)
            self.dt_prod.view.heading(i, anchor=CENTER)
        
        btn_frame = tb.Frame(self.tab_products)
        btn_frame.pack(fill=X, pady=10)

        btn_new = tb.Button(
            btn_frame, 
            text="Crear nuevo producto",
            bootstyle="outline-success",
            command=self.create_product
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar producto",
            bootstyle="outline-primary",
            command=self.edit_product
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar producto",
            bootstyle="outline-danger",
            command=self.delete_product
        )
        btn_delete.pack(side=RIGHT, pady=5)

    def setup_medicines_tab(self):
        self.cols_medicines = [
        {"text": "Barcode", "width": 120, "stretch": False},
        {"text": "Nombre", "width": 180, "stretch": True},
        {"text": "Descripción", "width": 200, "stretch": True},
        {"text": "Sustancia Activa", "width": 150, "stretch": False},
        {"text": "Concentración", "width": 100, "stretch": False},
        {"text": "Presentación", "width": 120, "stretch": False},
        {"text": "Stock", "width": 60, "stretch": False},
        {"text": "Receta", "width": 60, "stretch": False},
        {"text": "Mark", "width": 120, "stretch": False},
        ]

        self.dt_med = Tableview(master=self.tab_medicines, 
                                coldata=self.cols_medicines, 
                                paginated=True, 
                                searchable=True, 
                                bootstyle="info",
                                autofit=False)
        
        self.dt_med.pack(fill=BOTH, expand=True)
        self.dt_med.view.configure(selectmode="browse")
        
        for i in range(len(self.cols_medicines)):
                self.dt_med.view.column(i, anchor=CENTER)
                self.dt_med.view.heading(i, anchor=CENTER)


        btn_frame = tb.Frame(self.tab_medicines)
        btn_frame.pack(fill=X, pady=10)
        btn_new = tb.Button(
            btn_frame, 
            text="Crear medicamento",
            bootstyle="outline-success",
            command= self.create_medicine
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            btn_frame, 
            text="Editar medicamento",
            bootstyle="outline-primary",
            command= self.edit_medicine
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            btn_frame,
            text="Eliminar medicamento",
            bootstyle="outline-danger",
            command= self.delete_medicine
        )
        btn_delete.pack(side=RIGHT, pady=5)

    def setup_marks_tab(self):
        self.cols_marks = [
            {"text": "ID", "stretch": True},
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

        for i in range(len(self.cols_marks)):
            self.dt_marks.view.column(i, anchor=CENTER)
            self.dt_marks.view.heading(i, anchor=CENTER)

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
    def load_product(self):
        try:
            response = ProductManager.get_generic_product()

            rowdata = []

            for item in response.get_data():
                rowdata.append((
                        item.barcode,
                        item.name,
                        item.description,
                        item.stock,
                        item.category.get_name(),
                        item.mark.get_name()
                    )
                )
            
            self.dt_prod.build_table_data(self.cols_products, rowdata)
            
            for i in range(len(self.cols_products)):
                self.dt_prod.view.column(i, anchor=CENTER)
                self.dt_prod.view.heading(i, anchor=CENTER)
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")

    def save_product(self, data:Product | None = None, create = True):
        try:
            if create:
                respone = ProductManager.create_product(data)
            else:
                respone = ProductManager.update_product(self.current_id, data)

            Messagebox.show_info(respone.get_message(), "Exito")
            self.load_product()
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

    def create_product(self):
        ProductFormModal(
            self, 
            "Crear producto", 
            self.save_product
        )

    def edit_product(self):
        selection = self.dt_prod.view.selection()

        if not selection:
            Messagebox.show_warning("Ningun producto seleccionado", "Advertencia")
            return
        
        item_id = selection[0]
        values = self.dt_prod.view.item(item_id, 'values')
        self.current_id = values[0]

        # Reconstruimos el objeto con lo que ya hay en la tabla
        product = Product(
            barcode = values[0],
            name = values[1],
            description = values[2],
            stock = values[3],
            category = Category(name= values[4]),
            mark= Mark(name = values[5]),
            is_active = True
        )

        ProductFormModal(
            self,
            "Editar producto",
            self.save_product,
            product
        )

    def delete_product(self):
        selection = self.dt_prod.view.selection()

        if not selection:
            Messagebox.show_warning(f"Ningun producto seleccionado", "Advertencia")
            return

        item_id =  selection[0]

        values = self.dt_prod.view.item(item_id, 'values')

        answer = Messagebox.yesno(
            message=f"Desea eliminar el producto: {values[0]}",
            title="Eliminar producto",
            alert=True
        )

        if answer == "Sí":
            response = ProductManager.delete_product(values[0])
            Messagebox.show_info(response.get_message(), "Exito")
            self.load_product()


    # medicine space
    def load_medicine(self):
        try:
            response = MedicineManager.get_all_medicines()
            rowdata = []

            for item in response.get_data():
                rowdata.append((
                    item.barcode,
                    item.name,
                    item.description,
                    item.active_ingredient,
                    item.concentration,
                    item.presentation,
                    item.stock,
                    "Sí" if item.prescription else "No",
                    item.mark.get_name() if item.mark else "N/A"
                ))
            
            self.dt_med.build_table_data(self.cols_medicines, rowdata)
            
            # Forzar centrado de columnas
            for i in range(len(self.cols_medicines)):
                self.dt_med.view.column(i, anchor=CENTER)
                self.dt_med.view.heading(i, anchor=CENTER)

        except APIError as e:
            Messagebox.show_error(e.message, "Error de Base de Datos")
        except Exception as e:
            Messagebox.show_error(f"Error al cargar medicinas: {e}", "Error")

    def save_medicine(self, data: Medicine | None = None, create=True):
        try:
            if create:
                response = MedicineManager.create_medicine(data)
            else:
                response = MedicineManager.update_medicine(self.current_id, data)

            Messagebox.show_info(response.get_message(), "Éxito")
            self.load_medicine()
            return True
        except Exception as e:
            Messagebox.show_error(f"Error al guardar", "Error")
            return False

    def create_medicine(self):
        MedicineFormModal(
            self, 
            "Crear Medicamento", 
            self.save_medicine
        )

    def edit_medicine(self):
        selection = self.dt_med.view.selection()
        if not selection:
            Messagebox.show_warning("Seleccione una medicina", "Advertencia")
            return
        
        item_id = selection[0]
        values = self.dt_med.view.item(item_id, 'values')
        self.current_id = values[0] # Barcode

        response = MedicineManager.get_one_medicine(self.current_id)
        medicine = response.get_data()

        MedicineFormModal(
            self,
            "Editar Medicamento",
            self.save_medicine,
            medicine
        )

    def delete_medicine(self):
        selection = self.dt_med.view.selection()
        if not selection:
            Messagebox.show_warning("Seleccione una medicina", "Advertencia")
            return

        values = self.dt_med.view.item(selection[0], 'values')
        barcode = values[0]
        nombre = values[1]

        answer = Messagebox.yesno(
            message=f"¿Desea eliminar el medicamento: {nombre} ({barcode})?",
            title="Confirmar Eliminación",
            alert=True
        )

        if answer == "Sí":
            response = MedicineManager.delete_medicine(barcode)
            Messagebox.show_info(response.get_message(), "Éxito")
            self.load_medicine()

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
            
            for i in range(len(self.cols_marks)):
                self.dt_marks.view.column(i, anchor=CENTER)
                self.dt_marks.view.heading(i, anchor=CENTER)
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