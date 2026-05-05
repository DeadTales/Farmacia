

class Response:
    status_codes = {
        200: "Consulta exitosa",
        204: "Exitoso, sin contenido",
        400: "Solicitud erronea",
        403: "Se requiere autorizacion",
        404: "No se encontro el contenido",
        500: "Error interno del servidor"
    }
    
    def __init__(self, data: list = None, message: str = None, status: int = None):
        self.data = data
        self.message = message
        self.status = status

    def set_data(self, data: list):
        self.data = data
    
    def set_message(self, message: str):
        self.message = message

    def set_status(self, status: int):
        self.status = status

    def get_data(self):
        return self.data
    
    def get_message(self):
        return self.message

    def get_status(self):
        return self.status
    
    @property
    def status_message(self) -> str:
        if self.status in self.status_codes:
            return self.status_codes[self.status]
        
        return "Estado desconocido"