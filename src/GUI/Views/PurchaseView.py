import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tableview import Tableview
from postgrest.exceptions import APIError

from Core.Commons import validate_number
from Core.Product.ProductManager import ProductManager
from Core.PurchaseManager import PurchaseManager
from Core.VendorManager import VendorManager
from Models.Product.Product import Product
from Models.Transaction.TransactionDetail import TransactionDetail


class PurchaseView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.vendors = {}
        self.products = {}
        self.cart: list[TransactionDetail] = []

        tb.Label(self, text="Registro de Compra", font=("Helvetica", 20, "bold")).pack(pady=12)
        self.build_vendor_section()
        self.build_product_section()
        self.build_cart_section()
        self.refresh_vendors()
        self.refresh_products()
        self.refresh_cart()

    def build_vendor_section(self):
        frame = tb.Labelframe(self, text="Proveedor", padding=10)
        frame.pack(fill=X, padx=20, pady=8)

        tb.Label(frame, text="Proveedor:").pack(side=LEFT, padx=5)
        self.cmb_vendor = tb.Combobox(frame, values=[], state=READONLY, width=58)
        self.cmb_vendor.pack(side=LEFT, padx=5)

        self.var_order = tb.BooleanVar(value=True)
        self.var_send_email = tb.BooleanVar(value=False)
        tb.Checkbutton(frame, text="Generar orden PDF", variable=self.var_order, bootstyle="round-toggle").pack(side=LEFT, padx=8)
        tb.Checkbutton(frame, text="Enviar al proveedor", variable=self.var_send_email, bootstyle="round-toggle").pack(side=LEFT, padx=8)

    def build_product_section(self):
        frame = tb.Labelframe(self, text="Agregar producto", padding=10)
        frame.pack(fill=X, padx=20, pady=8)

        tb.Label(frame, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.cmb_product = tb.Combobox(frame, values=[], state=READONLY, width=52)
        self.cmb_product.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

        v_number = frame.register(validate_number)
        tb.Label(frame, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_amount = tb.Spinbox(frame, from_=1, to=9999, width=8, validate="key", validatecommand=(v_number, "%P"))
        self.ent_amount.grid(row=0, column=3, padx=5, pady=5)
        self.ent_amount.delete(0, END)
        self.ent_amount.insert(0, "1")

        tb.Label(frame, text="Precio compra:").grid(row=0, column=4, padx=5, pady=5)
        self.ent_price = tb.Entry(frame, width=12, validate="key", validatecommand=(v_number, "%P"))
        self.ent_price.grid(row=0, column=5, padx=5, pady=5)

        tb.Button(frame, text="Agregar", bootstyle="success", command=self.add_product).grid(row=0, column=6, padx=5, pady=5)
        frame.columnconfigure(1, weight=1)

    def build_cart_section(self):
        self.coldata = [
            {"text": "Codigo", "stretch": False},
            {"text": "Producto", "stretch": True},
            {"text": "Cantidad", "stretch": False},
            {"text": "Precio compra", "stretch": False},
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
        self.lbl_total = tb.Label(frame, text="Total: $ 0.00", font=("Helvetica", 12, "bold"))
        self.lbl_total.pack(side=RIGHT, padx=8)
        tb.Button(frame, text="Registrar compra", bootstyle="success", command=self.finish_purchase).pack(side=RIGHT, padx=5)

    def refresh_vendors(self):
        try:
            response = VendorManager.get_all_vendors()
            pairs = [(f"{item.vendor_id} - {item.name}", item) for item in response.get_data()]
            self.vendors = dict(pairs)
            self.cmb_vendor.configure(values=[text for text, value in pairs])
        except Exception as e:
            Messagebox.show_error(f"Error al cargar proveedores {e}", "Error")

    def refresh_products(self):
        try:
            response = ProductManager.get_all_products()
            pairs = [(f"{item.barcode} - {item.name} | Stock: {item.stock} | $ {float(item.price or 0):.2f}", item) for item in response.get_data()]
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
        subtotal = self.get_total()
        total = subtotal * 1.16
        self.lbl_total.configure(text=f"Total c/IVA: $ {total:.2f}")

    def add_product(self):
        product = self.products.get(self.cmb_product.get())
        if not product:
            Messagebox.show_warning("Selecciona un producto", "Advertencia")
            return
        amount = int(float(self.ent_amount.get() or 0))
        price = float(self.ent_price.get() or 0)
        if amount <= 0 or price <= 0:
            Messagebox.show_warning("Cantidad y precio deben ser mayores a cero", "Advertencia")
            return

        existing = next((item for item in self.cart if item.product.barcode == product.barcode), None)
        if existing:
            existing.amount += amount
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

    def finish_purchase(self):
        vendor = self.vendors.get(self.cmb_vendor.get())
        if not vendor:
            Messagebox.show_warning("Selecciona un proveedor", "Advertencia")
            return
        try:
            response = PurchaseManager.register_purchase(vendor, self.cart, self.var_order.get(), self.var_send_email.get())
            data = response.get_data()
            message = (
                f"{response.get_message()}\n"
                f"Subtotal: $ {data['subtotal']:.2f}\n"
                f"IVA: $ {data['iva']:.2f}\n"
                f"Total: $ {data['total']:.2f}"
            )
            if data.get("order_path"):
                message += f"\nOrden: {data['order_path']}"
            if self.var_send_email.get():
                message += f"\nCorreo enviado a: {vendor.email}"
            Messagebox.show_info(message, "Exito")
            self.clear_cart()
            self.refresh_products()
        except APIError as e:
            Messagebox.show_error(e.message, "Error")
        except Exception as e:
            Messagebox.show_error(f"{e}", "Error")
