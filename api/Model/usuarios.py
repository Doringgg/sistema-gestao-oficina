import re

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
        if not isinstance(value, str):
            raise ValueError("senha deve ser uma string.")

        senha_trimmed = value.strip()

        if senha_trimmed == "":
            raise ValueError("senha não pode ser vazia.")

        if len(senha_trimmed) < 6:
            raise ValueError("senha deve ter pelo menos 6 caracteres.")

        if not any(c.isupper() for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos uma letra maiúscula.")

        if not any(c.isdigit() for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos um número.")

        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos um caractere especial.")
        
        self.__senha = senha_trimmed