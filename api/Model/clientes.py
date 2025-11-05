from utils import cpfVerify
import re

class Cliente:
    def __init__(self):
        self.__cpf = None
        self.__nome = None
        self.__telefone = None
    
    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self,value):
        value = ''.join(filter(str.isdigit, str(value)))

        if len(value) !=11:
            raise ValueError("CPF inválido")
        soma = sum(int(value[i]) * (10 - i) for i in range(9))
        dig1 = 0 if (soma % 11) < 2 else 11 - (soma % 11)
    
        if dig1 != int(value[9]):
            raise ValueError("CPF inválido")

        soma = sum(int(value[i]) * (11 - i) for i in range(10))
        dig2 = 0 if (soma % 11) < 2 else 11 - (soma % 11)
    
        if dig2 == int(value[10]):
            self.__cpf = value
        else:
            raise ValueError("CPF inválido")
    
    
    @property
    def nome(self):
        return self.__nome 
    
    @nome.setter
    def nome(self,value):
        value = value.strip()
        pattern = r"^[A-Za-zÀ-ÿ]{2,}(?:['-][A-Za-zÀ-ÿ]{2,})*(?:\s+[A-Za-zÀ-ÿ]{2,}(?:['-][A-Za-zÀ-ÿ]{2,})*)+$"

        if bool(re.match(pattern,value)) == False:
            raise ValueError("Nome Inválido")
        self.__nome = value.title()
    
    
    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self,value):
        value = ''.join(filter(str.isdigit, str(value)))

        if len(value) != 11:
            raise ValueError("Telefone inválido")
    
        if not (11 <= int(value[:2]) <= 99):
            raise ValueError("Telefone Inválido")
    
    # Verifica se começa com 9 (celular)
        if value[2] != '9':
            raise ValueError("Telefone Inválido")
    
    # Verifica segundo dígito (não pode ser 0 ou 1)
        if value[3] in ['0', '1']:
            raise ValueError("Telefone Inválido")
        
        self.__telefone = value
        

