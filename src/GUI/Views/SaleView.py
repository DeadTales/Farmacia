import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from postgrest.exceptions import APIError

from Core.ClientManager import ClientManager
from Core.Commons import validate_number
from Core.Product.ProductManager import ProductManager
from Core.SaleManager import SaleManager
from GUI.Form.ClientForm import ClientFormModal
from Models.Client import Client
from Models.Product.Product import Product
from Models.Transaction.TransactionDetail import TransactionDetail


class SaleView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.clients = {}
        self.products = {}
        self.cart: list[TransactionDetail] = []

        tb.Label(self, text="Caja de Venta", font=("Helvetica", 20, "bold")).pack(pady=12)

        self.build_client_section()
        self.build_product_section()
        self.build_cart_section()
        self.refresh_clients()
        self.refresh_products()
        self.refresh_cart()

    def build_client_section(self):
        frame = tb.Labelframe(self, text="Cliente", padding=10)
        frame.pack(fill=X, padx=20, pady=8)

        tb.Label(frame, text="Cliente registrado:").pack(side=LEFT, padx=5)
        self.cmb_client = tb.Combobox(frame, values=[], state=READONLY, width=48)
        self.cmb_client.pack(side=LEFT, padx=5)
        tb.Button(frame, text="Registrar cliente", bootstyle="outline-success", command=self.create_client).pack(side=LEFT, padx=5)

        self.var_invoice = tb.BooleanVar(value=False)
        self.var_send_email = tb.BooleanVar(value=False)
        tb.Checkbutton(frame, text="Factura", variable=self.var_invoice, bootstyle="round-toggle").pack(side=LEFT, padx=8)
        tb.Checkbutton(frame, text="Enviar correo", variable=self.var_send_email, bootstyle="round-toggle").pack(side=LEFT, padx=8)

    def build_product_section(self):
        frame = tb.Labelframe(self, text="Agregar producto", padding=10)
        frame.pack(fill=X, padx=20, pady=8)

        tb.Label(frame, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.cmb_product = tb.Combobox(frame, values=[], state=READONLY, width=46)
        self.cmb_product.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

        v_number = frame.register(validate_number)
        tb.Label(frame, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_amount = tb.Spinbox(frame, from_=1, to=999, width=8, validate="key", validatecommand=(v_number, "%P"))
        self.ent_amount.grid(row=0, column=3, padx=5, pady=5)
        self.ent_amount.delete(0, END)
        self.ent_amount.insert(0, "1")

        self.lbl_price = tb.Label(frame, text="Precio: $ 0.00")
        self.lbl_price.grid(row=0, column=4, padx=5, pady=5)
        self.cmb_product.bind("<<ComboboxSelected>>", self.update_selected_price)

        tb.Button(frame, text="Agregar", bootstyle="success", command=self.add_product).grid(row=0, column=5, padx=5, pady=5)
        frame.columnconfigure(1, weight=1)

    def build_cart_section(self):
        self.coldata = [
            {"text": "Codigo", "stretch": False},
            {"text": "Producto", "stretch": True},
            {"text": "Cantidad", "stretch": False},
            {"text": "Precio", "stretch": False},
            {"text": "Subtotal", "stretch": False},
        ]
        self.dt = Tableview(
            master=self,
            coldata=self.coldata,
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="info",
            pagesize=8,
            stripecolor=(None, "#5c5b5b"),
        )
        self.dt.align_column_center()
        self.dt.pack(fill=BOTH, expand=True, padx=20, pady=10)

        frame = tb.Frame(self)
        frame.pack(fill=X, padx=20, pady=8)
        tb.Button(frame, text="Quitar producto", bootstyle="outline-danger", command=self.remove_product).pack(side=LEFT, padx=5)
        tb.Button(frame, text="Vaciar", bootstyle="outline-secondary", command=self.clear_cart).pack(side=LEFT, padx=5)

        self.lbl_subtotal = tb.Label(frame, text="Subtotal: $ 0.00", font=("Helvetica", 12, "bold"))
        self.lbl_subtotal.pack(side=RIGHT, padx=8)
        tb.Button(frame, text="Cobrar", bootstyle="success", command=self.finish_sale).pack(side=RIGHT, padx=5)

    def refresh_clients(self):
        try:
            response = ClientManager.get_all_clients()
            clients = response.get_data()
            pairs = [(f"{item.email} - {item.first_name} {item.last_name}", item) for item in clients]
            self.clients = dict(pairs)
            self.cmb_client.configure(values=[text for text, value in pairs])
        except Exception as e:
            Messagebox.show_error(f"Error al cargar clientes {e}", "Error")

    def refresh_products(self):
        try:
            response = ProductManager.get_all_products()
            products = [item for item in response.get_data() if int(item.stock or 0) > 0]
            pairs = [(f"{item.barcode} - {item.name} | Stock: {item.stock} | $ {float(item.price or 0):.2f}", item) for item in products]
            self.products = dict(pairs)
            self.cmb_product.configure(values=[text for text, value in pairs])
        except Exception as e:
            Messagebox.show_error(f"Error al cargar productos {e}", "Error")

    def refresh_cart(self):
        rowdata = [
            (
                detail.product.barcode,
                detail.product.name,
                detail.amount,
                f"$ {float(detail.unit_price):.2f}",
                f"$ {detail.get_subtotal():.2f}",
            )
            for detail in self.cart
        ]
        self.dt.build_table_data(self.coldata, rowdata)
        self.lbl_subtotal.configure(text=f"Subtotal: $ {self.get_total():.2f}")

    def add_product(self):
        product = self.products.get(self.cmb_product.get())
        if not product:
            Messagebox.show_warning("Selecciona un producto", "Advertencia")
            return
        amount = int(float(self.ent_amount.get() or 0))
        price = float(product.price or 0)
        if amount <= 0 or price <= 0:
            Messagebox.show_warning("Cantidad y precio de producto deben ser mayores a cero", "Advertencia")
            return
        if amount > int(product.stock or 0):
            Messagebox.show_warning(f"Stock insuficiente. Disponible: {product.stock}", "Advertencia")
            return

        existing = next((item for item in self.cart if item.product.barcode == product.barcode), None)
        if existing:
            new_amount = existing.amount + amount
            if new_amount > int(product.stock or 0):
                Messagebox.show_warning(f"Stock insuficiente. Disponible: {product.stock}", "Advertencia")
                return
            existing.amount = new_amount
            existing.unit_price = price
        else:
            self.cart.append(TransactionDetail(amount=amount, unit_price=price, product=Product(
                barcode=product.barcode,
                name=product.name,
                description=product.description,
                stock=product.stock,
                category=product.category,
                mark=product.mark,
                is_active=product.is_active,
                price=product.price,
            )))
        self.refresh_cart()

    def update_selected_price(self, event=None):
        product = self.products.get(self.cmb_product.get())
        self.lbl_price.configure(text=f"Precio: $ {float(product.price or 0):.2f}" if product else "Precio: $ 0.00")

    def remove_product(self):
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Selecciona un producto del carrito", "Advertencia")
            return
        values = self.dt.view.item(selection[0], "values")
        self.cart = [item for item in self.cart if item.product.barcode != values[0]]
        self.refresh_cart()

    def clear_cart(self):
        self.cart = []
        self.refresh_cart()

    def get_total(self):
        return sum(detail.get_subtotal() for detail in self.cart)

    def get_selected_client(self):
        return self.clients.get(self.cmb_client.get())

    def finish_sale(self):
        client = self.get_selected_client()
        if not client:
            Messagebox.show_warning("Selecciona un cliente registrado o registra uno nuevo antes de cobrar", "Advertencia")
            return
        if self.var_send_email.get() and not self.var_invoice.get():
            Messagebox.show_warning("Para enviar correo primero activa Factura", "Advertencia")
            return

        try:
            response = SaleManager.register_sale(
                client=client,
                details=self.cart,
                invoice=self.var_invoice.get(),
                send_email=self.var_send_email.get(),
            )
            data = response.get_data()
            message = (
                f"{response.get_message()}\n"
                f"Total: $ {data['total']:.2f}\n"
                f"Puntos actuales: {data['new_points']}"
            )
            if data["discount"]:
                message += f"\nDescuento aplicado: $ {data['discount']:.2f}"
            if data["invoice_path"]:
                message += f"\nFactura: {data['invoice_path']}"
            Messagebox.show_info(message, "Exito")
            self.clear_cart()
            self.refresh_clients()
            self.refresh_products()
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"{e}", "Error")

    def create_client(self):
        ClientFormModal(self, "Registrar cliente", self.save_new_client)

    def save_new_client(self, data: Client | None = None, create=True):
        try:
            response = ClientManager.create_client(data)
            Messagebox.show_info(response.get_message(), "Exito")
            self.refresh_clients()
            for text, client in self.clients.items():
                if client.email == data.email:
                    self.cmb_client.set(text)
                    break
            return True
        except Exception as e:
            Messagebox.show_error(f"{e}", "Error")
            return False
