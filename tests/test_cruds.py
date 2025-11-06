#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar todos os CRUDs da aplicação
"""

import sys
import os

# Adiciona o caminho raiz do projeto ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.Database.database import Database
from api.DAO.ClientesDAO import ClienteDAO
from api.Model.clientes import Cliente

def test_cliente_crud():
    """Testa todas as operações CRUD da entidade Cliente"""
    print("🚀 INICIANDO TESTES CRUD - CLIENTE")
    print("=" * 50)
    
    try:
        # 1. CONEXÃO COM BANCO
        print("1. 📡 Conectando ao banco de dados...")
        db = Database()
        cliente_dao = ClienteDAO(db)
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # 2. CREATE - Criar cliente
        print("2. 📝 TESTE CREATE - Criando cliente...")
        cliente = Cliente()
        cliente.cpf = "47958841884"  # CPF válido
        cliente.nome = "João Silva Teste"
        cliente.telefone = "11999999999"
        
        cliente_dao.create(cliente)
        print("✅ Cliente criado com sucesso!")
        print(f"   CPF: {cliente.cpf}")
        print(f"   Nome: {cliente.nome}")
        print(f"   Telefone: {cliente.telefone}")
        print()
        
        # 3. READ BY CPF - Buscar cliente específico
        print("3. 🔍 TESTE READ BY CPF - Buscando cliente...")
        cliente_encontrado = cliente_dao.readByCPF("47958841884")
        
        if cliente_encontrado:
            print("✅ Cliente encontrado!")
            print(f"   Dados: {cliente_encontrado}")
        else:
            print("❌ Cliente não encontrado!")
            return False
        print()
        
        # 4. READ ALL - Listar todos clientes
        print("4. 📋 TESTE READ ALL - Listando todos clientes...")
        todos_clientes = cliente_dao.readALL()
        
        print(f"✅ Total de clientes no banco: {len(todos_clientes)}")
        for i, cli in enumerate(todos_clientes, 1):
            print(f"   {i}. {cli['nome']} - {cli['cpf']}")
        print()
        
        # 5. UPDATE - Atualizar cliente
        print("5. ✏️  TESTE UPDATE - Atualizando cliente...")
        cliente.nome = "João Silva ATUALIZADO"
        cliente.telefone = "12996474222"
        
        sucesso_update = cliente_dao.update(cliente)
        if sucesso_update:
            print("✅ Cliente atualizado com sucesso!")
            
            # Verificar se realmente atualizou
            cliente_atualizado = cliente_dao.readByCPF("47958841884")
            print(f"   Novo nome: {cliente_atualizado['nome']}")
            print(f"   Novo telefone: {cliente_atualizado['telefone']}")
        else:
            print("❌ Falha ao atualizar cliente!")
            return False
        print()
        
        # 6. DELETE - Remover cliente
        print("6. 🗑️  TESTE DELETE - Removendo cliente...")
        sucesso_delete = cliente_dao.delete(cliente)
        
        if sucesso_delete:
            print("✅ Cliente removido com sucesso!")
            
            # Verificar se realmente foi removido
            cliente_verificacao = cliente_dao.readByCPF("47958841884")
            if not cliente_verificacao:
                print("✅ Confirmação: Cliente não existe mais no banco")
            else:
                print("❌ ERRO: Cliente ainda existe no banco!")
                return False
        else:
            print("❌ Falha ao remover cliente!")
            return False
        print()
        
        # 7. TESTE DE CLIENTE INEXISTENTE
        print("7. 🔎 TESTE CLIENTE INEXISTENTE...")
        cliente_inexistente = cliente_dao.readByCPF("99999999999")
        
        if not cliente_inexistente:
            print("✅ Correto: Cliente inexistente retorna None")
        else:
            print("❌ ERRO: Cliente inexistente deveria retornar None")
            return False
        print()
        
        print("🎉🎉🎉 TODOS OS TESTES PASSARAM COM SUCESSO! 🎉🎉🎉")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌❌❌ ERRO DURANTE OS TESTES: {e}")
        print("=" * 50)
        return False

def test_validacoes_cliente():
    """Testa as validações da classe Cliente"""
    print("\n🧪 TESTANDO VALIDAÇÕES DA CLASSE CLIENTE")
    print("=" * 50)
    
    try:
        # Teste CPF inválido
        print("1. Testando CPF inválido...")
        cliente = Cliente()
        try:
            cliente.cpf = "123"  # CPF muito curto
            print("❌ ERRO: CPF inválido deveria lançar exceção!")
            return False
        except ValueError:
            print("✅ Correto: CPF inválido lança exceção")
        
        # Teste nome inválido
        print("2. Testando nome inválido...")
        try:
            cliente.nome = "J"  # Nome muito curto
            print("❌ ERRO: Nome inválido deveria lançar exceção!")
            return False
        except ValueError:
            print("✅ Correto: Nome inválido lança exceção")
        
        # Teste telefone inválido
        print("3. Testando telefone inválido...")
        try:
            cliente.telefone = "119"  # Telefone muito curto
            print("❌ ERRO: Telefone inválido deveria lançar exceção!")
            return False
        except ValueError:
            print("✅ Correto: Telefone inválido lança exceção")
        
        print("🎉 TODAS AS VALIDAÇÕES FUNCIONANDO CORRETAMENTE!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NAS VALIDAÇÕES: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTADOR DE CRUDS - SISTEMA OFICINA")
    print("=" * 60)
    
    # Executar testes
    sucesso_crud = test_cliente_crud()
    sucesso_validacoes = test_validacoes_cliente()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print(f"   CRUDs: {'✅ PASSOU' if sucesso_crud else '❌ FALHOU'}")
    print(f"   Validações: {'✅ PASSOU' if sucesso_validacoes else '❌ FALHOU'}")
    
    if sucesso_crud and sucesso_validacoes:
        print("\n🎉🎉🎉 TODOS OS TESTES FORAM BEM-SUCEDIDOS! 🎉🎉🎉")
        print("Sistema pronto para uso! 🚀")
    else:
        print("\n💥 ALGUNS TESTES FALHARAM! Verifique o código.")
    
    print("=" * 60)