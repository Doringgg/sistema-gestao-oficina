from flask import Flask, jsonify, request
from flask_cors import CORS

from werkzeug.exceptions import HTTPException, NotFound

from api.Database.database import Database
from api.utils.error_response import ErrorResponse
from api.utils.logger import Logger

from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.ClientesMiddleware import ClienteMiddleware
from api.Middleware.CarrosMiddleware import CarroMiddleware
from api.Middleware.UsuariosMiddleware import UsuarioMiddleware

from api.Control.ClientesControl import ClientesControl
from api.Control.CarrosControl import CarroControl
from api.Control.UsuariosControl import UsuariosControl

from api.Service.ClientesService import ClienteService
from api.Service.CarrosService import CarroService
from api.Service.UsuariosService import UsuarioService

from api.DAO.ClientesDAO import ClienteDAO
from api.DAO.CarrosDAO import CarroDAO
from api.DAO.UsuariosDAO import UsuarioDAO

from api.Router.ClienteRouter import ClienteRouter
from api.Router.CarroRouter import CarroRouter
from api.Router.UsuarioRouter import UsuarioRouter

import traceback

class Server:

    def __init__(self, porta: int = 80):

        self.__porta = porta

        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        CORS(self.__app, resources={r"/*": {"origins": "*"}})

        self.__jwt_middleware = JwtMiddleware()
        self.__cliente_middleware = ClienteMiddleware()
        self.__carro_middleware = CarroMiddleware()
        self.__usuario_middleware = UsuarioMiddleware()

        self.__cliente_dao = None
        self.__cliente_service = None
        self.__cliente_control = None

        self.__carro_dao = None
        self.__carro_service = None
        self.__carro_control = None

        self.__usuario_dao = None
        self.__usuario_service = None
        self.__usuario_control = None

        self.__db_connection = None

    def init(self):

        self.__before_routing()

        self.__db_connection = Database(
            pool_name="pool_oficina",
            pool_size= 10,
            host="127.0.0.1",
            user="root",
            password="",
            database="oficina",
            port=3306
        )
        self.__db_connection.connect()

        self.__setup_cliente()
        self.__setup_carro()
        self.__setup_usuario()
        self.__error_middleware()

    def __setup_cliente(self):

        print("⬆️  Setup Cliente")

        self.__cliente_dao = ClienteDAO(self.__db_connection)

        self.__cliente_service = ClienteService(self.__cliente_dao)
        
        self.__cliente_control = ClientesControl(self.__cliente_service)

        cliente_router = ClienteRouter(
            self.__jwt_middleware,
            self.__cliente_middleware,
            self.__cliente_control
        )

        self.__app.register_blueprint(cliente_router.create_routes(), url_prefix="/api/v1/clientes")

    def __setup_carro(self):

        print("⬆️  Setup Carro")

        self.__carro_dao = CarroDAO(self.__db_connection)

        if self.__cliente_dao is None:
            self.__cliente_dao = ClienteDAO(self.__db_connection)

        self.__carro_service = CarroService(self.__carro_dao, self.__cliente_dao)

        self.__carro_control = CarroControl(self.__carro_service)

        carro_router = CarroRouter(
            self.__jwt_middleware,
            self.__carro_middleware,
            self.__carro_control
        )
        
        self.__app.register_blueprint(carro_router.create_routes(), url_prefix="/api/v1/carros")

    def __setup_usuario(self):
        print("⬆️  Setup Usuario")

        self.__usuario_dao = UsuarioDAO(self.__db_connection)

        self.__usuario_service = UsuarioService(self.__usuario_dao)

        self.__usuario_control = UsuariosControl(self.__usuario_service)

        usuario_router = UsuarioRouter(
            self.__usuario_middleware,
            self.__usuario_control
        )

        self.__app.register_blueprint(usuario_router.create_routes(), url_prefix="/api/v1/usuarios")

        print("📋 Rotas registradas:")
        for rule in self.__app.url_map.iter_rules():
            print(f"  {rule.methods} {rule}")

    def __before_routing(self):

        @self.__app.before_request
        def log_separator():
            print("-" * 70)

    def __error_middleware(self):

        @self.__app.errorhandler(Exception)
        def handle_error(error):

            if isinstance(error, NotFound):
                return error, 404
            
            if isinstance(error, ErrorResponse):
                print("🟡 Server.error_middleware()")
                # Extrai stack trace como string
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

                Logger.log_error(error)  # Loga a exceção real

                resposta = {
                    "success": False,
                    "error": {
                        "message": str(error),
                        "code": getattr(error, "code", None),
                        "details": getattr(error, "error", None)
                    },
                    "data": {
                        "message": "Erro tratado pela aplicação",
                        "stack": stack_str
                    }
                }
                return jsonify(resposta), error.httpCode

            # 🔹 Outros erros internos (não tratados)
            stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print("🟡 Server.error_middleware()")
            resposta = {
                "success": False,
                "error": {
                    "message": str(error),
                    "code": getattr(error, "code", None)
                },
                "data": {
                    "message": "Ocorreu um erro interno no servidor",
                    "stack": stack_str
                }
            }

            Logger.log_error(error)  # Loga a exceção real
            return jsonify(resposta), 500

    def run(self):
        """Inicia o servidor Flask na porta configurada"""
        print(f"🚀 Servidor rodando em: http://127.0.0.1:{self.__porta}/Login.html")
        # ⚠️ debug=False é necessário para que o errorhandler global capture exceções
        self.__app.run(port=self.__porta, debug=False)

        

