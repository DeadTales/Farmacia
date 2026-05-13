from Models.User import User

class Session:
    _instance_ = None
    _user_data_: User | None = None


    def __new__(cls):
        if cls._instance_ is None:
            cls._instance_ = super(Session, cls).__new__(cls)
        
        return cls._instance_
    
    def start_session(self, user: User):
        self._user_data_ = user

    @staticmethod
    def get_session():
        return Session() if Session._instance_ is None else Session._instance_
    
    @staticmethod
    def log_out():
        Session._instance_ = None

    @property
    def is_logged(self) -> bool:
        return self._user_data_ is not None
    
    @property
    def user(self)-> User | None:
        return self._user_data_

    @property
    def role_name(self) -> str:
        if not self._user_data_ or not self._user_data_.user_type:
            return ""
        user_type = self._user_data_.user_type
        if hasattr(user_type, "get_type_name"):
            return (user_type.get_type_name() or "").strip().lower()
        if isinstance(user_type, dict):
            return (user_type.get("name") or "").strip().lower()
        return str(user_type).strip().lower()

    def has_role(self, *roles: str) -> bool:
        role_aliases = {
            "administrador": "admin",
            "administrator": "admin",
        }
        current_role = role_aliases.get(self.role_name, self.role_name)
        return current_role in [role_aliases.get(role.strip().lower(), role.strip().lower()) for role in roles]

    def has_permission(self, option: str) -> bool:
        role_aliases = {
            "administrador": "admin",
            "administrator": "admin",
        }
        role = role_aliases.get(self.role_name, self.role_name)
        permissions = {
            "admin": {"Usuarios", "Clientes", "Productos", "Ventas", "Proveedores", "Compras", "Reportes"},
            "encargado": {"Clientes", "Productos", "Ventas"},
            "gerente": {"Usuarios", "Clientes", "Productos", "Ventas", "Compras", "Reportes"},
        }
        return option in permissions.get(role, set())


    
