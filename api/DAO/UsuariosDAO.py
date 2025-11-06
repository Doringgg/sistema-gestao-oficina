from api.Model.usuarios import Usuario
import bcrypt


class UsuarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency

    def login(self, objUsuario) -> Usuario | None:
        print("🟢 UsuarioDAO.login()")
        SQL = """
            SELECT
                id,
                email,
                senha
            FROM usuarios
            WHERE email = %s;
            """
        
        with self.__database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, (objUsuario.email,))
                rows = cursor.fetchall()
        
        if len(rows) != 1:
            print("Usuário não encontrado")
            return None
        
        usuarioDB = rows[0]

        if not bcrypt.checkpw(
            objUsuario.senha.encode("utf-8"),
            usuarioDB["senha"].encode("utf-8")
        ):
            print("Senha Inválida")
            return None
            
        usuario = Usuario()
        usuario.id = usuarioDB["id"]
        usuario.email = usuarioDB["email"]
            
        print("✅ UsuarioDAO.login() -> sucesso")
        return usuario
            