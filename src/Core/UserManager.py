from postgrest.exceptions import APIError

from Core.Response import Response
from Models.User import User
from Models.UserType import UserType
from Services.UserRepository import UserRepository


class UserManager:
    @staticmethod
    def get_all_users():
        try:
            data = UserRepository.get_all()
            if not data:
                return Response(data=[], message="No hay usuarios", status=204)
            return Response(data=[User.from_dict(item) for item in data], message="Consulta exitosa de usuarios", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"UserManager Error --- {e}")
            raise Exception("Error desconocido al consultar")

    @staticmethod
    def get_user_types():
        try:
            data = UserRepository.get_user_types()
            if not data:
                return Response(data=[], message="No hay tipos de usuario", status=204)
            return Response(data=[UserType.from_dict(item) for item in data], message="Consulta exitosa de tipos de usuario", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"UserManager Error --- {e}")
            raise Exception("Error desconocido al consultar tipos de usuario")

    @staticmethod
    def create_user(user: User):
        UserManager._validate_user(user, creating=True)
        try:
            return Response(data=UserRepository.create(UserManager._to_db_dict(user, include_password=True)), message="Usuario creado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"UserManager Error --- {e}")
            raise Exception("Error desconocido al crear")

    @staticmethod
    def update_user(nickname: str, user: User):
        if not nickname:
            raise ValueError("No hay un usuario seleccionado")
        UserManager._validate_user(user, creating=False)
        try:
            data = UserManager._to_db_dict(user, include_password=bool(user.pswd))
            return Response(data=UserRepository.update(nickname, data), message="Usuario actualizado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"UserManager Error --- {e}")
            raise Exception("Error desconocido al actualizar")

    @staticmethod
    def delete_user(nickname: str):
        if not nickname:
            raise ValueError("No hay un usuario seleccionado")
        try:
            return Response(data=UserRepository.delete(nickname), message="Usuario eliminado exitosamente", status=200)
        except APIError as e:
            raise APIError(e)
        except Exception as e:
            print(f"UserManager Error --- {e}")
            raise Exception("Error desconocido al eliminar")

    @staticmethod
    def _validate_user(user: User, creating: bool):
        if not user.nickname:
            raise ValueError("No hay nombre de usuario")
        if not user.first_name:
            raise ValueError("No hay nombre")
        if not user.last_name:
            raise ValueError("No hay apellidos")
        if creating and not user.pswd:
            raise ValueError("No hay contrasena")
        if not user.user_type or not user.user_type.get_type_id():
            raise ValueError("No hay tipo de usuario seleccionado")

    @staticmethod
    def _to_db_dict(user: User, include_password: bool):
        data = {
            "nickname": user.nickname,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "type_id": user.user_type.get_type_id(),
        }
        if include_password:
            data["pswd"] = user.pswd
        return data
