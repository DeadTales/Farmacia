import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from postgrest.exceptions import APIError

from Models.Product import *
from Core.Product import *
from Core.Commons import validate_number

class ProductFormModal(tb.Toplevel):
    def __init__(self, parent, title, callback, product_data:Product | None=None):
        super().__init__(title=title, transient=parent)
        self.parent = parent
        self.callback = callback
        self.initial_data = product_data
        self.create = True

        self.grab_set() 
        self.geometry("600x800")
        self.resizable(False, False)
        
        self.place_window_center()

        self.create_widgets(product_data)

    def create_widgets(self, data: Product):
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        tb.Label(container, text="Datos del producto", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Entradas
        tb.Label(container, text="Código de barras:").pack(anchor=W)
        self.ent_id = tb.Entry(container)
        self.ent_id.pack(fill=X, pady=5)

        tb.Label(container, text="Nombre:").pack(anchor=W)
        self.ent_name = tb.Entry(container)
        self.ent_name.pack(fill=X, pady=5)

        tb.Label(container, text="Descripción:").pack(anchor=W)
        self.ent_description = tb.Entry(container)
        self.ent_description.pack(fill=X, pady=5)


        v_number = container.register(validate_number)

        tb.Label(container, text="Stock:").pack(anchor=W)
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

        self.map_categories = {}
        list_categories = []
        texts_categories = []
        try:
            response = CategoryManager.get_generic_categories()

            if response:
                for item in response.get_data():
                    list_categories.append((
                            item.name,
                            item.category_id
                        )
                    )

                texts_categories = [text for text, value in list_categories]
                self.map_categories = dict(list_categories)

        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")


        tb.Label(container, text="Categoria:").pack(anchor=W)
        self.ent_category = tb.Combobox(
            container, 
            values=texts_categories,
            state=READONLY
        )
        self.ent_category.pack(fill=X, pady=5)


        self.map_marks = {}
        list_marks = []
        texts_marks = []
        try:
            response = MarkManager.get_all_marks()

            if response:
                for item in response.get_data():
                    list_marks.append((
                            item.name,
                            item.mark_id
                        )
                    )

                texts_marks = [text for text, value in list_marks]
                self.map_marks= dict(list_marks)

        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")

        tb.Label(container, text="Marca:").pack(anchor=W)
        self.ent_mark = tb.Combobox(
            container, 
            values=texts_marks,
            state=READONLY
        )
        self.ent_mark.pack(fill=X, pady=5)

        # Edicion
        if data:
            self.ent_id.insert(0, data.get_barcode())
            self.ent_id.configure(state=DISABLED)
            self.ent_name.insert(0, data.get_name())
            self.ent_description.insert(0, data.get_description())
            self.ent_stock.insert(0, data.get_stock())

            category_name = data.category.get_name()
            if category_name:
                idx = texts_categories.index(category_name)
                self.ent_category.current(idx) 
            
            mark_name = data.mark.get_name()
            if mark_name:
                idx = texts_marks.index(mark_name)
                self.ent_mark.current(idx)

            self.create = False

        # Botones
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=20)

        tb.Button(btn_frame, text="Guardar", bootstyle="success", command=self.send).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", bootstyle="danger-outline", command=self.destroy).pack(side=LEFT, padx=5)


    def send(self):
        category_name = self.ent_category.get()
        mark_name = self.ent_mark.get()

        payload = Product(
            barcode = None if not self.ent_id.get() else self.ent_id.get(),
            name = self.ent_name.get(),
            description = self.ent_description.get(),
            
            category = Category(
                category_id = self.map_categories.get(category_name), 
                name= category_name
            ),

            mark= Mark(
                mark_id = self.map_categories.get(mark_name),
                name = mark_name
            ),
            is_active = True
        )

        if self.callback(payload, self.create):
            self.destroy()