#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE COMPLETO - MODEL USUARIO + DAO USUARIO + SERVICE USUARIO
Testa a integração completa das 3 camadas
"""

import sys
import os
import bcrypt

# Adiciona o caminho raiz do projeto ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.Database.database import Database
from api.DAO.UsuariosDAO import UsuarioDAO
from api.Model.usuarios import Usuario
from api.Service.UsuariosService import UsuarioService
from api.utils.error_response import ErrorResponse

def criar_usuario_teste():
    """Cria um usuário de teste no banco para os testes"""
    print("👤 CRIANDO USUÁRIO DE TESTE NO BANCO")
    print("=" * 50)
    
    try:
        db = Database()
        
        # SQL para criar usuário de teste com senha bcrypt
        SQL_INSERT = """
            INSERT INTO usuarios (email, senha) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE senha = VALUES(senha)
        """
        
        # Senha "Senha@123" em bcrypt
        senha_hash = bcrypt.hashpw("Senha@123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        with db.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL_INSERT, ("teste@oficina.com", senha_hash))
                connection.commit()
        
        print("✅ Usuário de teste criado/atualizado:")
        print(f"   Email: teste@oficina.com")
        print(f"   Senha: Senha@123")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário de teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_usuario():
    """Testa a camada Model - Validações do objeto Usuario"""
    print("\n🧪 TESTANDO CAMADA MODEL (Usuario)")
    print("=" * 50)
    
    try:
        # Teste 1: Criação básica do objeto
        print("1. 🔧 Teste de criação do objeto Usuario...")
        usuario = Usuario()
        print("✅ Objeto Usuario criado com sucesso")
        
        # Teste 2: Setters válidos
        print("2. ✅ Teste de setters válidos...")
        usuario.id = 1
        usuario.email = "usuario.valido@email.com"
        usuario.senha = "Senha@123"
        
        print(f"   ID: {usuario.id}")
        print(f"   Email: {usuario.email}")
        print(f"   Senha: {usuario.senha}")
        print("✅ Setters válidos funcionando")
        
        # Teste 3: Validações de ID
        print("3. 🆔 Teste de validações de ID...")
        try:
            usuario.id = -1
            print("❌ ERRO: ID negativo deveria ser rejeitado")
            return False
        except ValueError as e:
            print(f"✅ ID negativo rejeitado: {e}")
        
        try:
            usuario.id = "abc"
            print("❌ ERRO: ID não numérico deveria ser rejeitado")
            return False
        except ValueError as e:
            print(f"✅ ID não numérico rejeitado: {e}")
        
        # Teste 4: Validações de Email
        print("4. 📧 Teste de validações de Email...")
        emails_invalidos = [
            "emailinvalido",
            "a@b",
            "teste@",
            "@dominio.com",
            "a" * 151 + "@email.com"
        ]
        
        for email_invalido in emails_invalidos:
            try:
                usuario.email = email_invalido
                print(f"❌ ERRO: Email inválido aceito: {email_invalido}")
                return False
            except ValueError:
                print(f"✅ Email inválido rejeitado: {email_invalido[:20]}...")
        
        # Teste 5: Validações de Senha
        print("5. 🔒 Teste de validações de Senha...")
        senhas_invalidas = [
            "abc",           # Muito curta
            "senhasemmaiuscula123@",  # Sem maiúscula
            "SENHASEMminuscula123@",  # Sem minúscula
            "SenhaSemNumero@",        # Sem número
            "Senha123456"             # Sem caractere especial
        ]
        
        for senha_invalida in senhas_invalidas:
            try:
                usuario.senha = senha_invalida
                print(f"❌ ERRO: Senha inválida aceita: {senha_invalida}")
                return False
            except ValueError:
                print(f"✅ Senha inválida rejeitada: {senha_invalida[:15]}...")
        
        print("🎉 TODOS OS TESTES DO MODEL PASSARAM!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NOS TESTES DO MODEL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dao_usuario():
    """Testa a camada DAO - Interação com o banco de dados"""
    print("\n🗄️ TESTANDO CAMADA DAO (UsuarioDAO)")
    print("=" * 50)
    
    try:
        db = Database()
        usuario_dao = UsuarioDAO(db)
        
        # Teste 1: Login com credenciais corretas
        print("1. ✅ Teste de login com credenciais corretas...")
        usuario_login = Usuario()
        usuario_login.email = "teste@oficina.com"
        usuario_login.senha = "Senha@123"  # Senha em texto puro
        
        usuario_encontrado = usuario_dao.login(usuario_login)
        
        if usuario_encontrado:
            print("✅ Login bem-sucedido!")
            print(f"   ID retornado: {usuario_encontrado.id}")
            print(f"   Email retornado: {usuario_encontrado.email}")
            print(f"   Tipo do objeto: {type(usuario_encontrado)}")
        else:
            print("❌ ERRO: Login com credenciais corretas falhou")
            return False
        
        # Teste 2: Login com senha incorreta
        print("2. ❌ Teste de login com senha incorreta...")
        usuario_login.senha = "SenhaErrada123"
        usuario_encontrado = usuario_dao.login(usuario_login)
        
        if not usuario_encontrado:
            print("✅ Login com senha errada rejeitado corretamente")
        else:
            print("❌ ERRO: Login com senha errada deveria falhar")
            return False
        
        # Teste 3: Login com email inexistente
        print("3. 🔍 Teste de login com email inexistente...")
        usuario_login.email = "naoexiste@email.com"
        usuario_login.senha = "QualquerSenha123"
        usuario_encontrado = usuario_dao.login(usuario_login)
        
        if not usuario_encontrado:
            print("✅ Email inexistente rejeitado corretamente")
        else:
            print("❌ ERRO: Email inexistente deveria falhar")
            return False
        
        print("🎉 TODOS OS TESTES DO DAO PASSARAM!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NOS TESTES DO DAO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_service_usuario():
    """Testa a camada Service - Lógica de negócio e geração de token"""
    print("\n⚡ TESTANDO CAMADA SERVICE (UsuarioService)")
    print("=" * 50)
    
    try:
        db = Database()
        usuario_dao = UsuarioDAO(db)
        usuario_service = UsuarioService(usuario_dao)
        
        # Teste 1: Login bem-sucedido via Service
        print("1. ✅ Teste de login bem-sucedido via Service...")
        dados_login = {
            "email": "teste@oficina.com",
            "senha": "Senha@123"
        }
        
        resultado = usuario_service.login(dados_login)
        
        # Verifica estrutura do retorno
        if "user" in resultado and "token" in resultado:
            print("✅ Estrutura de retorno correta")
            print(f"   Email no user: {resultado['user']['usuario']['email']}")
            print(f"   ID no user: {resultado['user']['usuario']['id']}")
            print(f"   Token JWT gerado: {resultado['token'][:50]}...")
            
            # Verifica se o token é válido
            from api.http.meu_token_jwt import MeuTokenJWT
            jwt_validator = MeuTokenJWT()
            if jwt_validator.validarToken(resultado["token"]):
                print("✅ Token JWT válido")
            else:
                print("❌ ERRO: Token JWT inválido")
                return False
        else:
            print("❌ ERRO: Estrutura de retorno incorreta")
            return False
        
        # Teste 2: Login com credenciais inválidas via Service
        print("2. ❌ Teste de login inválido via Service...")
        dados_login_invalido = {
            "email": "teste@oficina.com",
            "senha": "SenhaErrada123"
        }
        
        try:
            resultado = usuario_service.login(dados_login_invalido)
            print("❌ ERRO: Login inválido deveria lançar exceção")
            return False
        except ErrorResponse as e:
            print(f"✅ Login inválido lançou ErrorResponse corretamente")
            print(f"   Status code: {e.status_code}")
            print(f"   Mensagem: {e.message}")
        
        # Teste 3: Login com email inexistente via Service
        print("3. 🔍 Teste de login com email inexistente via Service...")
        dados_login_inexistente = {
            "email": "naoexiste@email.com",
            "senha": "QualquerSenha123"
        }
        
        try:
            resultado = usuario_service.login(dados_login_inexistente)
            print("❌ ERRO: Email inexistente deveria lançar exceção")
            return False
        except ErrorResponse as e:
            print(f"✅ Email inexistente lançou ErrorResponse corretamente")
            print(f"   Status code: {e.status_code}")
        
        print("🎉 TODOS OS TESTES DO SERVICE PASSARAM!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NOS TESTES DO SERVICE: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fluxo_completo():
    """Testa o fluxo completo: JSON → Service → DAO → Model → Token"""
    print("\n🔄 TESTANDO FLUXO COMPLETO DA APLICAÇÃO")
    print("=" * 50)
    
    try:
        # Configuração das dependências
        db = Database()
        usuario_dao = UsuarioDAO(db)
        usuario_service = UsuarioService(usuario_dao)
        
        # Dados de entrada (simulando requisição HTTP)
        dados_requisicao = {
            "email": "teste@oficina.com",
            "senha": "Senha@123"
        }
        
        print("📥 Dados de entrada (JSON):")
        print(f"   Email: {dados_requisicao['email']}")
        print(f"   Senha: {dados_requisicao['senha'][:3]}...")
        print()
        
        # Executa o fluxo completo
        print("🔄 Executando fluxo completo...")
        resultado = usuario_service.login(dados_requisicao)
        print()
        
        # Verifica o resultado
        print("📤 Resultado final:")
        print(f"   ✅ Usuário autenticado: {resultado['user']['usuario']['email']}")
        print(f"   ✅ Token JWT gerado: {len(resultado['token'])} caracteres")
        print(f"   ✅ Estrutura completa: {list(resultado.keys())}")
        
        # Valida o token JWT
        from api.http.meu_token_jwt import MeuTokenJWT
        jwt_validator = MeuTokenJWT()
        if jwt_validator.validarToken(resultado["token"]):
            print("   ✅ Token JWT é válido e pode ser verificado")
            payload = jwt_validator.payload
            print(f"   ✅ Payload do token: email={payload.get('email')}, id={payload.get('id')}")
        else:
            print("   ❌ ERRO: Token JWT inválido")
            return False
        
        print("🎉 FLUXO COMPLETO FUNCIONANDO PERFEITAMENTE!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NO FLUXO COMPLETO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 TESTADOR COMPLETO - MODEL + DAO + SERVICE")
    print("=" * 60)
    print("Este teste verifica a integração de todas as camadas:")
    print("  📧 Model (Validações) → 🗄️ DAO (Banco) → ⚡ Service (Negócio)")
    print("=" * 60)
    
    # Executar todos os testes em sequência
    sucesso_setup = criar_usuario_teste()
    sucesso_model = test_model_usuario()
    sucesso_dao = test_dao_usuario()
    sucesso_service = test_service_usuario()
    sucesso_fluxo = test_fluxo_completo()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL DOS TESTES:")
    print(f"   🔧 Setup do banco: {'✅ PASSOU' if sucesso_setup else '❌ FALHOU'}")
    print(f"   📧 Model Usuario: {'✅ PASSOU' if sucesso_model else '❌ FALHOU'}")
    print(f"   🗄️ DAO Usuario: {'✅ PASSOU' if sucesso_dao else '❌ FALHOU'}")
    print(f"   ⚡ Service Usuario: {'✅ PASSOU' if sucesso_service else '❌ FALHOU'}")
    print(f"   🔄 Fluxo Completo: {'✅ PASSOU' if sucesso_fluxo else '❌ FALHOU'}")
    
    todos_passaram = all([sucesso_setup, sucesso_model, sucesso_dao, sucesso_service, sucesso_fluxo])
    
    if todos_passaram:
        print("\n🎉🎉🎉 PARABÉNS! TODAS AS CAMADAS ESTÃO INTEGRADAS! 🎉🎉🎉")
        print("\n📋 FLUXO CONFIRMADO:")
        print("   1. ✅ Model valida dados do usuário")
        print("   2. ✅ DAO consulta banco e verifica senha com bcrypt")
        print("   3. ✅ Service orquestra processo e gera token JWT")
        print("   4. ✅ Token JWT é válido e contém claims corretos")
    else:
        print("\n💥 ALGUNS TESTES FALHARAM! Verifique as camadas com problema.")
    
    print("=" * 60)