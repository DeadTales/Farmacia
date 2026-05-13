from postgrest import APIError

from Models.Product import *
from Core.Response import Response
from Services.Product.ProductRepository import ProductRepository

class ProductManager():
    @staticmethod
    def get_all_products():
        try:
            data = ProductRepository.get_all()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_products = []

            for product in data:
                list_products.append(Product.from_dict(product))
            
            return Response(data = list_products, message = "Consulta exitosa de productos", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--ProductManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")
    
    @staticmethod
    def get_generic_product():
        try:
            data = ProductRepository.get_generic()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_products = []

            for product in data:
                list_products.append(Product.from_dict(product))
            
            return Response(data = list_products, message = "Consulta exitosa de productos", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--ProductManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def get_one_product(product_id):
        try:
            data = ProductRepository.get_one(product_id)

            if not data:
                return Response(data = None, message = "No coincide un producto con ese id", status = 400)
            
            return Response(data = Product.from_dict(data), message = "Hubo coincidencia", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--ProductManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def create_product(product: Product):
        if not product.name:
            raise ValueError("El producto no tiene nombre")

        if not product.mark.get_mark_id():
            raise ValueError("No hay una marca seleccionada")
        
        if not product.category.get_category_id():
            raise ValueError("No hay una categoria seleccionada")

        if product.price is None or float(product.price) < 0:
            raise ValueError("No hay precio valido")
        
        try:

            data = ProductRepository.create(product.to_dict())

            return Response(data = data, message = "producto creada exitosamente", status = 200)

        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"Errro desconocido: {e}")
            raise Exception("Error desconocido al crear")
        pass
    
    @staticmethod
    def update_product(value_id, product: Product):
        if not value_id:
            raise ValueError("No hay un producto seleccionada")
        
        if not product.name:
            raise ValueError("No hay nombre de producto")
        
        if not product.mark.get_mark_id():
            raise ValueError("No hay una marca seleccionada")

        if not product.category.get_category_id():
            raise ValueError("No hay una categoria seleccionada")

        if product.price is None or float(product.price) < 0:
            raise ValueError("No hay precio valido")
        
        try:
            data = ProductRepository.update(value_id, product.to_dict())

            return Response(data = data, message = "Actualizacion exitosa", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--ProductManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_product(value_id):
        if not value_id:
            raise ValueError("No hay un producto seleccionada")
        
        try:
            data = ProductRepository.delete_logic(value_id)

            return Response(data, message = "Eliminado exitosamente", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--ProductManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al eliminar")
    
