from Services.Connection import db
from Models.User import User
from Models.UserType import UserType

def verify_credentials(nickname, pswd):

    response = db.table("profile").select("nickname, first_name, last_name, type_id") \
            .eq("nickname", nickname).eq("pswd", pswd).single().execute()

    if not response.data:
        raise ValueError("Credenciales incorrectas. Por favor, verifica tu usuario y contraseña.")
    
    user_data = response.data

    type_response = db.table("user_type").select("*").eq("type_id", user_data.get("type_id"), ).single().execute()

    if type_response.data:
        user_type = UserType.from_dict(type_response.data)
        user_data["user_type"] = user_type
    
    return User.from_dict(user_data)

    