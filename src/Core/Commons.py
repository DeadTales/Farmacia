import re

REX_DECIMAL = r"((?:\d+\.\d*)|(?:\.?\d+))"
REX_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validate_number(value: str) -> bool:
    if re.fullmatch(REX_DECIMAL, value):
        return True
    elif value == "":
        return True
    else:
        return False
    
def validate_email(value:str, widget) -> bool:    
    if value == "":
        widget.configure(bootstyle="default") # Color neutro si está vacío
    elif re.fullmatch(REX_EMAIL, value):
        widget.configure(bootstyle="success") # Color del tema para éxito
    else:
        widget.configure(bootstyle="danger")  # Color del tema para error
    
    return True