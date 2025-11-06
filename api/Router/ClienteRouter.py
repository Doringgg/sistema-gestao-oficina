from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.ClientesMiddleware import ClienteMiddleware
from api.Control.ClientesControl import ClientesControl

class ClienteRouter:
    def __init__(self, jwt_middleware: JwtMiddleware, cliente_middleware: ClienteMiddleware, cliente_control: ClientesControl):
        print("⬆️  ClienteRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__cliente_middleware = cliente_middleware
        self.__cliente_control = cliente_control

        self.__blueprint = Blueprint('cliente', __name__)


    def create_routes(self):

        @self.__blueprint.route('/',methods=['POST'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_create_body
        def store():
            return self.__cliente_control.store()
        
        
        @self.__blueprint.route('/',methods=['GET'])
        @self.__jwt_middleware.validate_token
        def showALL():
            return self.__cliente_control.showALL()
        

        @self.__blueprint.route('/<string:cpf>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_cpf_param
        def showOne(cpf):
            return self.__cliente_control.showOne(cpf)
        

        @self.__blueprint.route('/<string:cpf>',methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_cpf_param
        @self.__cliente_middleware.validate_update_body
        def update(cpf):
            return self.__cliente_control.update(cpf)
        

        @self.__blueprint.route('/<string:cpf>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_cpf_param
        def destroy(cpf):
            return self.__cliente_control.destroy(cpf)  
        return self.__blueprint