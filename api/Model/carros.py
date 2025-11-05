import re
from api.Model.clientes import Cliente

class Carro:
    def __init__(self):

        self.__placa = None
        self.__montadora = None
        self.__modelo = None
        self.__cor = None
        self.__clientes_cpf = None

    @property
    def placa(self):
        return self.__placa
    
    @placa.setter
    def placa(self,value):
        value = value.upper().strip()
        value = re.sub(r'[-\s]', '', value)
        if len(value) != 7:
            raise ValueError("Placa Inválida")
        
        mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'
        antigo = r'^[A-Z]{3}[0-9]{4}$'

        if re.match(antigo, value):
            value = f"{value[:3]}-{value[3:]}"
            self.__placa = value
    
        elif re.match(mercosul, value):
            self.__placa = value
        
        else:
            raise ValueError("Placa Inválida")
    
    
    @property
    def montadora(self):
        return self.__montadora
    
    @montadora.setter
    def montadora(self,value):
        value = value.strip()
        pattern = r"^(?=.*[A-Za-zÀ-ÿ])[A-Za-zÀ-ÿ0-9\s\-&.,()]{2,50}$"
        if not re.match(pattern, value):
            raise ValueError("Montadora Inválida")
        
        if re.match(r'^([A-Za-z0-9])\1+$', value.replace(' ','')):
            raise ValueError("Montadora Inválida")
        
        self.__montadora = value


    @property
    def modelo(self):
        return self.__modelo
    
    @modelo.setter
    def modelo(self,value):
        value = value.strip()
        pattern = r"^[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9\s\-\.\+/\(\)]{0,49}$"
        if not re.match(pattern, value):
            raise ValueError("Modelo Inválido")
        invalid_patterns = [
        r"^[\.\-\s]+$",
        r"^\d+$",
        r"^([A-Za-z])\1+$",
        ]  
        for _, invalid_pattern in enumerate(invalid_patterns):
            if re.match(invalid_pattern, value):
                raise ValueError("Modelo Inválido")
        self.__modelo = value


    @property
    def cor(self):
        return self.__cor
    
    @cor.setter
    def cor(self,value):
        value = value.strip()
        invalid_patterns = [
        r"^\d+$",                           # Apenas números: "123"
        r"^[\s\-]+$",                       # Apenas espaços ou hífens: "   ", "---"
        r".*[!@#$%^&*()_+=<>?{}~`].*",     # Caracteres especiais proibidos
        r"^\d+\s*[A-Za-z]",                # Números no início: "123 Azul"
        r".*\d{4,}.*",                     # Mais de 3 números consecutivos
        r"^([A-Za-z])\1+$",                  # Letra repetida: "AAAA", "BBBB"
        ]
        if len(value) < 2 or len(value) > 30:
            raise ValueError("Cor Inválida")
        
        for _,invalid_pattern in enumerate(invalid_patterns):
            if re.match(invalid_pattern, value, re.IGNORECASE):
                raise ValueError("Cor Inválida")
            
        self.__cor = value

    
    @property
    def clientes_cpf(self):
        return self.__clientes_cpf
    
    @clientes_cpf.setter
    def clientes_cpf(self,value):
        if not isinstance(value,Cliente):
            raise ValueError("Cliente deve ser uma instância válida de Cliente")
        self.__clientes_cpf = value