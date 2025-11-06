from flask import request, jsonify
from api.Service.UsuariosService import UsuarioService

class FuncionarioControl:
    def __init__(self, usuario_service: UsuarioService):
        print("⬆️  FuncionarioControl.constructor()")
        self.__usuario_service = usuario_service

    def login(self):
        print ("🔵 UsuariosControl.login()")

        json_usuario = request.json.get("usuario")
        resultado = self.__usuario_service.login(json_usuario)
        return jsonify({
            "success": True,
            "message": "Login efetuado com sucesso!",
            "data": resultado
        }), 201