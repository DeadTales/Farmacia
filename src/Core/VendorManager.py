from postgrest.exceptions import APIError

from Core.Response import Response
from Services.VendorRepositoy import VendorRepositoy
from Models.Vendor import Vendor

class VendorManager: 

    @staticmethod
    def get_all_vendors():
        try:
            data = VendorRepositoy.get_all()

            if not data:
                return Response(data=[], message= "No hay patrocinadores", status=204)
            
            list_vendors = []

            for item in data:
                list_vendors.append(Vendor.from_dict(item))
            
            return Response(data=list_vendors, message="Consulta exitosa de patrocinadores", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"VendorManager Error --- {e}") 
            raise Exception("Error desconocido a consultar")
        
    @staticmethod
    def get_one_vendor(id_value: str):
        try:
            data = VendorRepositoy.get_one(id_value)

            if not data:
                return Response(data=None, message="No coincide un proveedor con ese id", status=400)
            
            return Response(data= Vendor.from_dict(data), message="Hubo coincidencia", status=200)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"VendorManager Error --- {e}") 
            raise Exception("Error desconocido al consultar")


    @staticmethod
    def create_vendor(vendor: Vendor):
        if not vendor.vendor_id:
            raise ValueError("No hay id del proveedor")
            
        if not vendor.name:
            raise ValueError("No hay nombre de proveedor")
        
        if not vendor.phone:
            raise ValueError("No hay telefono de proveedor")
        
        if not vendor.email:
            raise ValueError("No hay correo")

        try:
            data = VendorRepositoy.create(vendor.to_dict())

            return Response(data=data, message="Creado exitosamente", status=200)

        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"VendorManager --- Error {e}")
            raise Exception("Error desconocido al crear")

    @staticmethod
    def update_vendor(id_value: str, vendor: Vendor):
        
        if not id_value:
            raise ValueError("No hay un proveedor seleccinado")
        
        if not vendor.vendor_id:
            raise ValueError("No hay id del proveedor")
        
        if not vendor.name:
            raise ValueError("No hay nombre de proveedor")
        
        if not vendor.phone:
            raise ValueError("No hay telefono de proveedor")
        
        if not vendor.email:
            raise ValueError("No hay correo")
             
        try:   
            data = VendorRepositoy.update(id_value, vendor.to_dict())

            return Response(data=data, message="Actualizacion exitosa", status=200)

        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"VendorManager --- Error {e}")
            raise Exception("Error desconocido al actualizar")



    @staticmethod
    def delete_vendor(id_value: str):
        if not id_value:
            raise ValueError("No hay un proveedor seleccionado")

        try:
            
            data = VendorRepositoy.delete(id_value)

            return Response(data=data, message="Eliminado exitosamente", status=200)

        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"VendorManager --- Error {e}")
            raise Exception("Error desconocido al eliminar")


