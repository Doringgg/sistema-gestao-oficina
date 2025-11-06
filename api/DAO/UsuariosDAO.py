from api.Model.usuarios import Usuario
from argon2 import PasswordHasher
import argon2

class UsuarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency

    def login(self, email: str, senha_plain_text: str) -> Usuario | None:
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
                cursor.execute(SQL, (email,))
                rows = cursor.fetchall()
        
        if len(rows) != 1:
            print("Usuário não encontrado")
            return None
        
        usuarioDB = rows[0]

        try:
            ph = PasswordHasher()
            ph.verify(usuarioDB["senha"], senha_plain_text)
            
            usuario = Usuario()
            usuario.id = usuarioDB["id"]
            usuario.email = usuarioDB["email"]
            
            print("✅ UsuarioDAO.login() -> sucesso")
            return usuario
            
        except argon2.exceptions.VerifyMismatchError:
            print("Senha Inválida")
            return None