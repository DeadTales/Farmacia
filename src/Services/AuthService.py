from postgrest.exceptions import APIError
from Services.Connection import db
from Models.User import User
from Models.UserType import UserType


def verify_credentials(nickname, pswd):
    try:
        response = db.table("profile").select("nickname, first_name, last_name, user_type: user_type(*)") \
                .eq("nickname", nickname).eq("pswd", pswd).single().execute()
        
        return User.from_dict(response.data)

    except APIError as e:
        if e.code == "PGRST116": # Código específico de "No rows found"
            raise ValueError("Credenciales incorrectas.")
        raise Exception(f"Error de base de datos: {e.message}")

    