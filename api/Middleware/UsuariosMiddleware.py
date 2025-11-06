from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class UsuarioMiddleware:

    def validate_login_body(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UsuarioMiddleware.validate_login_body()")
            body = request.get_json()

            if not body or 'usuario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'usuario' é obrigatório!"})
            
            usuario = body['usuario']

            campos_obrigatorios = ["email","senha"]
            for campo in campos_obrigatorios:
                if campo not in usuario:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo {campo} é obrigatório!"})
                
            return f(*args, **kwargs)
        return decorated_function