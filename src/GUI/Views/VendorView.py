import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

from GUI.Form.VendorForm import VendorFormModal
from Models.Vendor import Vendor
from Core.VendorManager import VendorManager

class PieceView(tb.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.current_folio = ""
        
        #Título
        lbl = tb.Label(self, text="Gestión de Proveedores", font=("Helvetica", 20, "bold"))
        lbl.pack(pady=20)

        #Definición de Columnas
        self.coldata = [
            {"text": "ID Proveedor", "stretch": False},
            {"text": "Nombre", "stretch": True},
            {"text": "Telefono de serie", "stretch": True},
            {"text": "Correo electronico ", "stretch": True}
        ]

       
        try:
            
            response = VendorManager.get_all_vendors()
            rowdata = []

            for item in response['data']:
                rowdata.append((
                        item.vendor_id,
                        item.name,
                        item.phone,
                        item.email
                    )
                )

        except Exception as e:
            Messagebox.show_error(f"Error al cargar los datos {e}", "Error")

        #Tableview
        self.dt = Tableview(
            master=self,
            coldata=self.coldata,
            rowdata=rowdata,
            paginated=True,   
            searchable=True,    
            bootstyle="info",
            pagesize=10,       
            stripecolor=(None, "#f2f2f2"), # Efecto cebra 
        )
        
        self.dt.align_column_center()
        self.dt.pack(fill=BOTH, expand=True, padx=20, pady=10)

        frame_actions = tb.Frame(self)

        frame_actions.pack(fill= X, padx=20, pady=10)

        btn_new = tb.Button(
            frame_actions, 
            text="Crear nuevo proveedor",
            bootstyle="outline-success",
            command=self.create_vendor
        )
        btn_new.pack(side=LEFT, padx=5)

        btn_edit = tb.Button(
            frame_actions, 
            text="Editar pproveedor",
            bootstyle="outline-primary",
            command=self.edit_vendor
        )
        btn_edit.pack(side=LEFT, padx=5)

        btn_delete = tb.Button(
            frame_actions,
            text="Eliminar proveedor",
            bootstyle="outline-danger",
            command=self.delete_vendor
        )
        btn_delete.pack(side=RIGHT, pady=5)


    def refresh_table(self):

        try:
            response = VendorManager.get_all_vendors()

            rowdata = []

            for item in response['data']:
                rowdata.append((
                        item.vendor_id,
                        item.name,
                        item.phone,
                        item.email
                    )
                )
            
            self.dt.build_table_data(self.coldata, rowdata)
        except Exception as e:
            Messagebox.show_error(f"Error al recargar los datos {e}", "Error")
        

    def save_info(self, data:Vendor | None = None, create = True):
        if create:
            respone = VendorManager.create_vendor(data)
        else:
            respone = VendorManager.update_vendor(data, self.current_folio)
        
        if isinstance(respone, dict):
            Messagebox.show_info(respone["message"], "Exito")
            self.refresh_table()
            return True
        else:
            Messagebox.show_error(respone["message"], "Error")
            return False

    def create_vendor(self):
        VendorFormModal(self, "Crear Proveedor", self.save_info)

    def edit_vendor(self):
        selection = self.dt.view.selection()
        if not selection:
            Messagebox.show_warning("Ningun proveedor seleccionado", "Advertencia")
            return
        
        item_id = selection[0]
        values = self.dt.view.item(item_id, 'values')
        self.current_folio = values[0]

        # Reconstruimos el objeto con lo que ya hay en la tabla
        vendor = Vendor(
            vendor_id=values[0],
            name=values[1],
            phone=values[2],
            email= values[3],
        )

        VendorFormModal(
            self,
            "Editar proveedor",
            self.save_info,
            vendor
    )



    def delete_vendor(self):
        selection = self.dt.view.selection()

        if not selection:
            Messagebox.show_warning(f"Ningun proveedor seleccionado", "Advertencia")
            return

        item_id =  selection[0]

        values = self.dt.view.item(item_id, 'values')

        answer = Messagebox.yesno(
            message=f"Desea eliminar el proveedor: {values[0]}",
            title="Eliminar proveedor",
            alert=True
        )

        if answer == "Sí":
            response = VendorManager.delete_vendor(values[0])
            Messagebox.show_info(response["message"], "Exito")
            self.refresh_table()


