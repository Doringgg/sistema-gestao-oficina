from api.http.meu_token_jwt import MeuTokenJWT
from api.utils.error_response import ErrorResponse
from api.Model.usuarios import Usuario
from api.DAO.UsuariosDAO import UsuarioDAO

class UsuarioService:
    def __init__(self, usuario_dao_dependency: UsuarioDAO):
        print("⬆️  UsuarioService.__init__()")
        self.__usuarioDAO = usuario_dao_dependency

    def login(self, jsonUsuario: dict) -> dict:
        print("🟣 UsuarioService.login()")
        print(jsonUsuario)

        objUsuario = Usuario()
        objUsuario.email = jsonUsuario["email"]
        senha_plain_text = jsonUsuario["senha"]

        encontrado = self.__usuarioDAO.login(objUsuario.email, senha_plain_text)

        if not encontrado:
            raise ErrorResponse(
                401,
                "Usuário ou senha inválidos",
                {"message": "Não foi possível realizar autenticação"}
            )
        
        jwt = MeuTokenJWT()
        user = {
            "usuario": {
                "email": encontrado.email,
                "id": encontrado.id
            }
        }
        return {"user": user, "token": jwt.gerarToken(user["usuario"])}