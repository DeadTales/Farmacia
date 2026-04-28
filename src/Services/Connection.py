import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DBManager:
        client: Client = None

        @classmethod
        def get_connection(cls) -> Client:
                
            if cls.client is None:
                    url = os.getenv("DB_URL")
                    key = os.getenv("DB_KEY")

                    if not url or not key:
                        raise ValueError("Faltan las credenciales de la base de datos")
                    
                    cls.client = create_client(url, key)

            return cls.client
        

db = DBManager.get_connection()

