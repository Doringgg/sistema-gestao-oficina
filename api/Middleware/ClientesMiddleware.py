from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class ClienteMiddleware:
    def validate_create_body(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_body_create()")
            body = request.get_json()

            if not body or 'cliente' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'cliente' é obrigatório!"}
                )
            
            cliente = body[cliente]
            if 'nome' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nome' é obrigatório!"}
                )
            
            if 'telefone' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'telefone' é obrigatório!"}
                )
            
            if 'cpf' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'cpf' é obrigatório!"}
                )
            
            return f(*args,**kwargs)
        return decorated_function
    
    def validate_update_body(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_body_update()")
            body = request.get_json()

            if not body or 'cliente' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'cliente' é obrigatório!"}
                )
            
            cliente = body[cliente]
            if 'nome' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nome' é obrigatório!"}
                )
            
            if 'telefone' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'telefone' é obrigatório!"}
                )
            
            return f(*args,**kwargs)
        return decorated_function
    
    def validate_cpf_param(self, f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            print("🔷 ClienteMiddleware.validate_cpf_param()")
            if 'cpf' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'cpf' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function