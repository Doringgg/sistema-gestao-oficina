import re
from argon2 import PasswordHasher

class Usuario: 
    def __init__(self):
        self.__id = None
        self.__email = None
        self.__senha = None

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        try:
            parsed = int(value)
        except(ValueError, TypeError):
            raise ValueError("Id deve ser um número inteiro")
        
        if parsed <= 0:
            raise ValueError("Id deve ser um número maior que zero")
        
        self.__id = parsed
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Email nulo")
        value = value.strip()
        if len(value) < 5 or len(value) > 150:
            raise ValueError("Email Inválido")
        if not '@' in value:
            raise ValueError("Email Inválido")
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern,value):
            raise ValueError("Email Inválido")
        
        self.__email = value.lower()

    
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, value):
        if value is None:
            raise ValueError("Senha nula")
        value = value.strip()
        if len(value) < 6 or len(value) > 100:
            raise ValueError("Senha Inválida")
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+\[\]{}|;:,.<>?/])[A-Za-z\d!@#$%^&*()\-_=+\[\]{}|;:,.<>?/]{6,}$'
        if not re.match(pattern,value):
            raise ValueError("Senha Inválida")
        ph = PasswordHasher()
        self.__senha = ph.hash(value)
    
