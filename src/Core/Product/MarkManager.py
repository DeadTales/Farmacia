from postgrest import APIError

from Models.Product.Mark import Mark
from Core.Response import Response
from Services.Product.MarkRepository import MarkRepository

class MarkManager():
    @staticmethod
    def get_all_marks():
        try:
            data = MarkRepository.get_all()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_marks = []

            for mark in data:
                list_marks.append(Mark.from_dict(mark))
            
            return Response(data = list_marks, message = "Consulta exitosa de marcas", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")
    
    #TODO implement the method to complement the TODO of MarkRepository

    @staticmethod
    def get_one_mark(mark_id):
        try:
            data = MarkRepository.get_one(mark_id)

            if not data:
                return Response(data = None, message = "No coincide una marca con ese id", status = 400)
            
            return Response(data = Mark.from_dict(data), message = "Hubo coincidencia", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def create_mark(mark: Mark):
        if not mark.name:
            raise ValueError("La marca no tiene nombre")

        if not mark.vendor.get_vendor_id():
            raise ValueError("No hay un proveedor seleccionado")
        
        try:

            data = MarkRepository.create(mark.to_dict())

            return Response(data = data, message = "Marca creada exitosamente", status = 200)

        except APIError as e:
            print(f"API -Vendor-: {e}")
            raise APIError(e)
        except Exception as e:
            print(f"Error desconocido: {e}")
            raise Exception("Error desconocido al crear")
    
    @staticmethod
    def update_mark(value_id, mark: Mark):
        if not value_id:
            raise ValueError("No hay una marca seleccionada")
        
        if not mark.name:
            raise ValueError("No hay nombre de marca")
        
        if not mark.vendor.get_vendor_id():
            raise ValueError("No hay un proveedor seleccionado")
        
        try:
            data = MarkRepository.update(value_id, mark.to_dict())

            return Response(data = data, message = "Actualizacion exitosa", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_mark(value_id):
        if not value_id:
            raise ValueError("No hay una marca seleccionada")
        
        try:
            data = MarkRepository.delete(value_id)

            return Response(data, message = "Eliminado exitosamente", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al eliminar")