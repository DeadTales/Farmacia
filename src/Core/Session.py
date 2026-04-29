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


    