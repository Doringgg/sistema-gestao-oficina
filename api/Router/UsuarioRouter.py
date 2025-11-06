from flask import Blueprint, request
from functools import wraps
from api.Middleware.UsuariosMiddleware import UsuarioMiddleware
from api.Control.UsuariosControl import UsuariosControl

class UsuarioRouter:
    def __init__(self, usuario_middleware:UsuarioMiddleware, usuario_control:UsuariosControl):

        print("⬆️  UsuarioRouter.__init__()")
        self.usuario_middleware = usuario_middleware
        self.usuario_control = usuario_control

        self.blueprint = Blueprint('usuario',__name__)

    def create_routes(self):
        @self.blueprint.route('/login', methods=['POST'])
        @self.usuario_middleware.validate_login_body
        def login():
            print("usuarioRouter.login()")
            return self.usuario_control.login()
        return self.blueprint