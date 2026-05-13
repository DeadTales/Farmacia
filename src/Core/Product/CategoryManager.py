from postgrest import APIError

from Models.Product.Category import Category 
from Core.Response import Response
from Services.Product.CategoryRepository import CategoryRepository


class CategoryManager:
    @staticmethod
    def get_all_categories():
        try:
            data = CategoryRepository.get_all()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_categories = []

            for category in data:
                list_categories.append(Category.from_dict(category))
            
            return Response(data = list_categories, message = "Consulta exitosa de categorias", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--CategoryManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")
    @staticmethod
    def get_generic_categories():
        try:
            data = CategoryRepository.get_generic()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_categories = []

            for category in data:
                list_categories.append(Category.from_dict(category))
            
            return Response(data = list_categories, message = "Consulta exitosa de categorias", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--CategoryManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    
    @staticmethod
    def get_one_category(category_id):
        try:
            data = CategoryRepository.get_one(category_id)

            if not data:
                return Response(data = None, message = "No coincide una categoria con ese id", status = 400)
            
            return Response(data = Category.from_dict(data), message = "Hubo coincidencia", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--CategoryManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def create_category(category: Category):
        if not category.name:
            raise ValueError("La categoria no tiene nombre")
        
        try:

            data = CategoryRepository.create(category.to_dict())

            return Response(data = data, message = "Categoria creada exitosamente", status = 200)

        except APIError as e:
            print(f"API -Vendor-: {e}")
            raise APIError(e)
        except Exception as e:
            print(f"Error desconocido: {e}")
            raise Exception("Error desconocido al crear")
    
    @staticmethod
    def update_category(value_id, category: Category):
        if not value_id:
            raise ValueError("No hay una categoria seleccionada")
        
        if not category.name:
            raise ValueError("No hay nombre de categoria")
        
        try:
            data = CategoryRepository.update(value_id, category.to_dict())

            return Response(data = data, message = "Actualizacion exitosa", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--CategoryManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_category(value_id):
        if not value_id:
            raise ValueError("No hay una categoria seleccionada")
        
        try:
            data = CategoryRepository.delete(value_id)

            return Response(data, message = "Eliminado exitosamente", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--CategoryManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al eliminar")