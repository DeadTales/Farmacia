from postgrest import APIError

from Models.Product import *
from Core.Response import Response
from Services.Product import  *

class MedicineManager():
    @staticmethod
    def get_all_medicines():
        try:
            data = MedicineRepository.get_all()

            if not data:
                return Response(data = [], message = "No hay elementos", status = 204)
            
            list_medicines = []

            for medicine in data:
                list_medicines.append(Medicine.from_dict(medicine))
            
            return Response(data = list_medicines, message = "Consulta exitosa de medicinas", status = 204)
        
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MedicineManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def get_one_medicine(medicine_id):
        try:
            data = MedicineRepository.get_one(medicine_id)

            if not data:
                return Response(data = None, message = "No coincide una medicina con ese id", status = 400)
            
            return Response(data = Medicine.from_dict(data), message = "Hubo coincidencia", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MedicineManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def create_medicine(medicine: Medicine):
        if not medicine.name:
            raise ValueError("La medicina no tiene nombre")

        if not medicine.mark.get_mark_id():
            raise ValueError("No hay una marca seleccionada")

        if medicine.price is None or float(medicine.price) < 0:
            raise ValueError("No hay precio valido")
        
        try:
            product_payload = medicine.to_product_dict()
            product_payload["barcode"] = medicine.barcode 
            
            ProductRepository.create(product_payload)
            
            medicine_payload = medicine.to_medicine_dict()
            medicine_payload["barcode"] = medicine.barcode
            
            data = MedicineRepository.create(medicine_payload)
            
            return Response(data = data, message = "medicina creada exitosamente", status = 200)

        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"Errro desconocido: {e}")
            raise Exception("Error desconocido al crear")
    
    @staticmethod
    def update_medicine(value_id, medicine: Medicine):
        if not value_id:
            raise ValueError("No hay una medicina seleccionada")
        
        if not medicine.name:
            raise ValueError("No hay nombre de medicina")
        
        if not medicine.mark.get_mark_id():
            raise ValueError("No hay una marca seleccionada")

        if medicine.price is None or float(medicine.price) < 0:
            raise ValueError("No hay precio valido")
        
        try:

            ProductRepository.update(value_id, medicine.to_product_dict())
            data = MedicineRepository.update(value_id, medicine.to_medicine_dict())

            return Response(data = data, message = "Actualizacion exitosa", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MedicineManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_medicine(value_id):
        if not value_id:
            raise ValueError("No hay una medicina seleccionada")
        
        try:
            data = MedicineRepository.delete_logic(value_id)

            return Response(data, message = "Eliminado exitosamente", status = 200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"--MedicineManager-- Error desconocido: {e}")
            raise Exception("Error desconocido al eliminar")
    
