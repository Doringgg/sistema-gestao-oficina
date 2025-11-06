from flask import Blueprint, request
from functools import wraps
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.CarrosMiddleware import CarroMiddleware
from api.Control.CarrosControl import CarroControl

class CarroRouter:
    def __init__(self, jwt_middleware:JwtMiddleware, carro_middleware: CarroMiddleware, carro_control:CarroControl):
        print("⬆️  CarroRouter.__init__()")
        
        self.jwt_middleware = jwt_middleware
        self.carro_middleware = carro_middleware
        self.carro_control = carro_control

        self.blueprint = Blueprint('carro', __name__)

        
    def create_routes(self):
        @self.blueprint.route('/',methods=['POST'])
        @self.jwt_middleware.validate_token
        @self.carro_middleware.validate_create_body
        def store():
            return self.carro_control.store()
        
        
        @self.blueprint.route('/',methods=['GET'])
        @self.jwt_middleware.validate_token
        def showALL():
            return self.carro_control.showALL()
        

        @self.blueprint.route('/<string:placa>',methods=['GET'])
        @self.jwt_middleware.validate_token
        @self.carro_middleware.validate_placa_param
        def showOne(placa):
            return self.carro_control.showOne(placa)
        

        @self.blueprint.route('/<string:placa>',methods=['PUT'])
        @self.jwt_middleware.validate_token
        @self.carro_middleware.validate_placa_param
        @self.carro_middleware.validate_update_body
        def update(placa):
            return self.carro_control.update(placa)
        

        @self.blueprint.route('/<string:placa>',methods=['DELETE'])
        @self.jwt_middleware.validate_token
        @self.carro_middleware.validate_placa_param
        def delete(placa):
            return self.carro_control.destroy(placa)
        
        return self.blueprint