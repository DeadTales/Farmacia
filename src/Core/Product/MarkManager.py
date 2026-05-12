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
    
    @staticmethod
    def get_one_mark(mark_id):
        try:
            data = MarkRepository.get_one(mark_id)

            if not data:
                return Response(data = None, message = "No coincide una marca con ese id", status = 400)
            
            return Response(data = data, message = "Hubo coincidencia", status = 200)
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
            raise APIError(e)
        except Exception as e:
            print(f"Errro desconocido: {e}")
            raise Exception("Error desconocido al crear")
        pass
    
    @staticmethod
    def update_mark(id_value, mark: Mark):
        if not id_value:
            raise ValueError("No hay una marca seleccionada")
        
        if not mark.name:
            raise ValueError("No hay nombre de marca")
        
        if not mark.vendor.get_vendor_id():
            raise ValueError("No hay un proveedor seleccionado")
        
        try:
            data = MarkRepository.update(id_value, mark.to_dict())

            return Response(data = data, message = "Actualizacion exitosa", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_mark(id_value):
        if not id_value:
            raise ValueError("No hay una marca seleccionada")
        
        try:
            data = MarkRepository.delete(id_value)

            return Response(data, message = "Eliminado exitosamente", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MarkManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al eliminar")
        pass