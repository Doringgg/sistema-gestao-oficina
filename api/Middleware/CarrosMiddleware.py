from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class CarroMiddleware:
    def validate_create_body(self,f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            print("🔷 CarroMiddleware.validate_create_body()")
            body = request.get_json()

            if not body or 'carro' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'funcionario' é obrigatório!"})
            
            carro = body["carro"]

            campos_obrigatorios = ["placa","montadora","modelo","cor"]
            for campo in campos_obrigatorios:
                if campo not in carro:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})
                
            if 'cliente' not in carro or 'clientes_cpf' not in carro['cliente']:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'carro.cliente' é obrigatório!"})
                
            return f(*args,**kwargs)
        return decorated_function
        
    def validate_update_body(self,f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            print("🔷 CarroMiddleware.validate_update_body()")
            body = request.get_json()

            if not body or 'carro' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'funcionario' é obrigatório!"})
            
            carro = body["carro"]

            campos_obrigatorios = ["montadora","modelo","cor"]
            for campo in campos_obrigatorios:
                if campo not in carro:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})
                
            if 'cliente' not in carro or 'clientes_cpf' not in carro['cliente']:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'carro.cliente' é obrigatório!"})
                
            return f(*args,**kwargs)
        return decorated_function
    
    def validate_placa_param(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 CarroMiddleware.validate_update_body()")
            if 'placa' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'placa' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function
