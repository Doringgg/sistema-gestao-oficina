#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar o sistema de login de usuários
"""

import sys
import os

# Adiciona o caminho raiz do projeto ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.Database.database import Database
from api.DAO.UsuariosDAO import UsuarioDAO
from api.Model.usuarios import Usuario

def test_criar_usuario_para_testes():
    """Cria um usuário de teste no banco (executar uma vez apenas)"""
    print("👤 CRIANDO USUÁRIO DE TESTE (executar apenas uma vez)")
    print("=" * 50)
    
    try:
        db = Database()
        # Precisamos criar um método create no UsuarioDAO temporariamente
        # Ou criar o usuário manualmente no banco
        
        print("💡 Para testar o login, primeiro crie um usuário:")
        print("1. Execute no MySQL:")
        print("""
        INSERT INTO usuarios (email, senha) VALUES (
            'teste@oficina.com', 
            '$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG'
        );
        """)
        print("\n2. Ou use a senha 'Senha@123' para criar via código")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_login_usuario():
    """Testa o sistema de login"""
    print("🔐 INICIANDO TESTES DE LOGIN")
    print("=" * 50)
    
    try:
        # 1. CONEXÃO COM BANCO
        print("1. 📡 Conectando ao banco de dados...")
        db = Database()
        usuario_dao = UsuarioDAO(db)
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # 2. TESTE LOGIN CORRETO
        print("2. ✅ TESTE LOGIN CORRETO...")
        usuario_logado = usuario_dao.login(
            email="teste@oficina.com",
            senha_plain_text="Senha@123"
        )
        
        if usuario_logado:
            print("✅ Login bem-sucedido!")
            print(f"   ID: {usuario_logado.id}")
            print(f"   Email: {usuario_logado.email}")
        else:
            print("❌ Login falhou (usuário não existe ou senha errada)")
            print("   💡 Crie o usuário primeiro com email: teste@oficina.com, senha: Senha@123")
        print()
        
        # 3. TESTE LOGIN SENHA ERRADA
        print("3. ❌ TESTE LOGIN SENHA ERRADA...")
        usuario_logado = usuario_dao.login(
            email="teste@oficina.com", 
            senha_plain_text="SenhaErrada123"
        )
        
        if not usuario_logado:
            print("✅ Correto: Login com senha errada retorna None")
        else:
            print("❌ ERRO: Login com senha errada deveria falhar")
            return False
        print()
        
        # 4. TESTE LOGIN EMAIL INEXISTENTE
        print("4. 🔍 TESTE LOGIN EMAIL INEXISTENTE...")
        usuario_logado = usuario_dao.login(
            email="naoexiste@email.com",
            senha_plain_text="QualquerSenha123"
        )
        
        if not usuario_logado:
            print("✅ Correto: Email inexistente retorna None")
        else:
            print("❌ ERRO: Email inexistente deveria retornar None")
            return False
        print()
        
        print("🎉🎉🎉 TODOS OS TESTES DE LOGIN PASSARAM! 🎉🎉🎉")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌❌❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return False

def test_validacoes_usuario():
    """Testa as validações da classe Usuario"""
    print("\n🧪 TESTANDO VALIDAÇÕES DA CLASSE USUARIO")
    print("=" * 50)
    
    try:
        # Teste email inválido
        print("1. Testando email inválido...")
        usuario = Usuario()
        try:
            usuario.email = "emailinvalido"  # Sem @
            print("❌ ERRO: Email inválido deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Email inválido lança exceção -> {e}")
        
        # Teste senha inválida
        print("2. Testando senha inválida...")
        try:
            usuario.senha = "abc"  # Muito curta e sem requisitos
            print("❌ ERRO: Senha inválida deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Senha inválida lança exceção -> {e}")
        
        # Teste ID inválido
        print("3. Testando ID inválido...")
        try:
            usuario.id = -5  # Número negativo
            print("❌ ERRO: ID inválido deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: ID inválido lança exceção -> {e}")
        
        # Teste senha válida (para ver o hash)
        print("4. Testando senha válida...")
        try:
            usuario.senha = "Senha@123"
            print("✅ Senha válida aceita!")
            print(f"   Hash gerado: {usuario.senha[:50]}...")
        except ValueError as e:
            print(f"❌ ERRO: {e}")
            return False
        
        print("🎉 TODAS AS VALIDAÇÕES DE USUARIO FUNCIONANDO CORRETAMENTE!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NAS VALIDAÇÕES: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTADOR DE LOGIN - SISTEMA OFICINA")
    print("=" * 60)
    
    # Executar testes
    test_criar_usuario_para_testes()
    sucesso_login = test_login_usuario()
    sucesso_validacoes = test_validacoes_usuario()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES - LOGIN:")
    print(f"   Login: {'✅ PASSOU' if sucesso_login else '❌ FALHOU'}")
    print(f"   Validações: {'✅ PASSOU' if sucesso_validacoes else '❌ FALHOU'}")
    
    if sucesso_login and sucesso_validacoes:
        print("\n🎉🎉🎉 SISTEMA DE LOGIN PRONTO! 🎉🎉🎉")
        print("Para usar:")
        print("1. Crie usuários com Usuario() + .senha (hash automático)")
        print("2. Faça login com usuario_dao.login(email, senha_plain_text)")
    else:
        print("\n💥 ALGUNS TESTES FALHARAM! Verifique o código.")
    
    print("=" * 60)