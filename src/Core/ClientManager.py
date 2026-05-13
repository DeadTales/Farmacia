from postgrest.exceptions import APIError

from Core.Response import Response
from Core.Address.AddressManager import AddressManager
from Models.Client import Client
from Services.ClientRepository import ClientRepository


class ClientManager:
    @staticmethod
    def get_all_clients():
        try:
            data = ClientRepository.get_all()
            if not data:
                return Response(data=[], message="No hay clientes", status=204)
            return Response(data=[Client.from_dict(item) for item in data], message="Consulta exitosa de clientes", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"ClientManager Error --- {e}")
            raise Exception("Error desconocido al consultar")
    def create_client(client: Client):
        ClientManager._validate_client(client)
        try:
            data = ClientRepository.create(ClientManager._to_db_dict(client))
            AddressManager.save_for_client(client.email, client.get_address())
            return Response(data=data, message="Cliente creado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"ClientManager Error --- {e}")
            raise Exception("Error desconocido al crear")

    @staticmethod
    def update_client(email: str, client: Client):
        if not email:
            raise ValueError("No hay un cliente seleccionado")
        ClientManager._validate_client(client)
        try:
            data = ClientRepository.update(email, ClientManager._to_db_dict(client))
            AddressManager.save_for_client(email, client.get_address())
            return Response(data=data, message="Cliente actualizado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"ClientManager Error --- {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_client(email: str):
        if not email:
            raise ValueError("No hay un cliente seleccionado")
        try:
            AddressManager.delete_by_client(email)
            return Response(data=ClientRepository.delete(email), message="Cliente eliminado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"ClientManager Error --- {e}")
            raise Exception("Error desconocido al eliminar")

    @staticmethod
    def _validate_client(client: Client):
        if not client.email:
            raise ValueError("No hay correo del cliente")
        if not client.first_name:
            raise ValueError("No hay nombre del cliente")
        if not client.last_name:
            raise ValueError("No hay apellidos del cliente")
        if not client.phone:
            raise ValueError("No hay telefono del cliente")

    @staticmethod
    def _to_db_dict(client: Client):
        return {
            "email": client.email,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "rfc": client.rfc,
            "phone": client.phone,
            "points": client.points or 0,
        }
