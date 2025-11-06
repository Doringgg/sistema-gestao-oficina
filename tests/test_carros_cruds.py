#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar todos os CRUDs da entidade Carro
"""

import sys
import os

# Adiciona o caminho raiz do projeto ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.Database.database import Database
from api.DAO.ClientesDAO import ClienteDAO
from api.DAO.CarrosDAO import CarroDAO
from api.Model.clientes import Cliente
from api.Model.carros import Carro

def test_carro_crud():
    """Testa todas as operações CRUD da entidade Carro"""
    print("🚗 INICIANDO TESTES CRUD - CARRO")
    print("=" * 50)
    
    try:
        # 1. CONEXÃO COM BANCO
        print("1. 📡 Conectando ao banco de dados...")
        db = Database()
        cliente_dao = ClienteDAO(db)
        carro_dao = CarroDAO(db)
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # 2. CREATE CLIENTE - Criar cliente primeiro
        print("2. 👤 CRIANDO CLIENTE para associar ao carro...")
        cliente = Cliente()
        cliente.cpf = "52998224725"  # CPF válido
        cliente.nome = "João Dono do Carro"
        cliente.telefone = "11999999999"
        
        cliente_dao.create(cliente)
        print("✅ Cliente criado com sucesso!")
        print(f"   CPF: {cliente.cpf}")
        print(f"   Nome: {cliente.nome}")
        print()
        
        # 3. CREATE CARRO - Criar carro associado ao cliente
        print("3. 🚗 TESTE CREATE - Criando carro...")
        carro = Carro()
        carro.placa = "ABC1D23"  # Padrão Mercosul
        carro.montadora = "Volkswagen"
        carro.modelo = "Golf GTI"
        carro.cor = "Vermelho"
        carro.cliente = cliente  # ✅ Associa o cliente
        
        carro_dao.create(carro)
        print("✅ Carro criado com sucesso!")
        print(f"   Placa: {carro.placa}")
        print(f"   Montadora: {carro.montadora}")
        print(f"   Modelo: {carro.modelo}")
        print(f"   Cor: {carro.cor}")
        print(f"   Dono: {carro.cliente.nome}")
        print()
        
        # 4. READ BY PLACA - Buscar carro específico
        print("4. 🔍 TESTE READ BY PLACA - Buscando carro...")
        carro_encontrado = carro_dao.readByPlaca("ABC1D23")
        
        if carro_encontrado:
            print("✅ Carro encontrado!")
            print(f"   Dados: {carro_encontrado}")
        else:
            print("❌ Carro não encontrado!")
            return False
        print()
        
        # 5. READ ALL - Listar todos carros
        print("5. 📋 TESTE READ ALL - Listando todos carros...")
        todos_carros = carro_dao.readALL()
        
        print(f"✅ Total de carros no banco: {len(todos_carros)}")
        for i, car in enumerate(todos_carros, 1):
            print(f"   {i}. {car['montadora']} {car['modelo']} - {car['placa']}")
        print()
        
        # 6. UPDATE - Atualizar carro
        print("6. ✏️  TESTE UPDATE - Atualizando carro...")
        carro.montadora = "VW"
        carro.modelo = "Golf GTI 2.0"
        carro.cor = "Azul"
        
        sucesso_update = carro_dao.update(carro)
        if sucesso_update:
            print("✅ Carro atualizado com sucesso!")
            
            # Verificar se realmente atualizou
            carro_atualizado = carro_dao.readByPlaca("ABC1D23")
            print(f"   Nova montadora: {carro_atualizado['montadora']}")
            print(f"   Novo modelo: {carro_atualizado['modelo']}")
            print(f"   Nova cor: {carro_atualizado['cor']}")
        else:
            print("❌ Falha ao atualizar carro!")
            return False
        print()
        
        # 7. DELETE - Remover carro
        print("7. 🗑️  TESTE DELETE - Removendo carro...")
        sucesso_delete = carro_dao.delete(carro)
        
        if sucesso_delete:
            print("✅ Carro removido com sucesso!")
            
            # Verificar se realmente foi removido
            carro_verificacao = carro_dao.readByPlaca("ABC1D23")
            if not carro_verificacao:
                print("✅ Confirmação: Carro não existe mais no banco")
            else:
                print("❌ ERRO: Carro ainda existe no banco!")
                return False
        else:
            print("❌ Falha ao remover carro!")
            return False
        print()
        
        # 8. DELETE CLIENTE (limpeza)
        print("8. 🧹 Limpando cliente de teste...")
        cliente_dao.delete(cliente)
        print("✅ Cliente removido!")
        print()
        
        # 9. TESTE DE CARRO INEXISTENTE
        print("9. 🔎 TESTE CARRO INEXISTENTE...")
        carro_inexistente = carro_dao.readByPlaca("ZZZ9999")
        
        if not carro_inexistente:
            print("✅ Correto: Carro inexistente retorna None")
        else:
            print("❌ ERRO: Carro inexistente deveria retornar None")
            return False
        print()
        
        print("🎉🎉🎉 TODOS OS TESTES DE CARRO PASSARAM COM SUCESSO! 🎉🎉🎉")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌❌❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return False

def test_validacoes_carro():
    """Testa as validações da classe Carro"""
    print("\n🧪 TESTANDO VALIDAÇÕES DA CLASSE CARRO")
    print("=" * 50)
    
    try:
        # Teste placa inválida
        print("1. Testando placa inválida...")
        carro = Carro()
        try:
            carro.placa = "ABC123"  # Placa muito curta
            print("❌ ERRO: Placa inválida deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Placa inválida lança exceção -> {e}")
        
        # Teste montadora inválida
        print("2. Testando montadora inválida...")
        try:
            carro.montadora = "V@W"  # Caractere especial não permitido
            print("❌ ERRO: Montadora inválida deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Montadora inválida lança exceção -> {e}")
        
        # Teste modelo inválido
        print("3. Testando modelo inválido...")
        try:
            carro.modelo = "A@B"  # Caractere especial não permitido
            print("❌ ERRO: Modelo inválido deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Modelo inválido lança exceção -> {e}")
        
        # Teste cor inválida
        print("4. Testando cor inválida...")
        try:
            carro.cor = "V@rmelho"  # Caractere especial não permitido
            print("❌ ERRO: Cor inválida deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Cor inválida lança exceção -> {e}")
        
        # Teste cliente inválido
        print("5. Testando cliente inválido...")
        try:
            carro.cliente = "Não é um cliente"  # String em vez de objeto Cliente
            print("❌ ERRO: Cliente inválido deveria lançar exceção!")
            return False
        except ValueError as e:
            print(f"✅ Correto: Cliente inválido lança exceção -> {e}")
        
        print("🎉 TODAS AS VALIDAÇÕES DE CARRO FUNCIONANDO CORRETAMENTE!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ ERRO NAS VALIDAÇÕES: {e}")
        return False

def test_placas_validas():
    """Testa diferentes formatos de placas válidas"""
    print("\n🚘 TESTANDO FORMATOS DE PLACAS VÁLIDAS")
    print("=" * 50)
    
    carro = Carro()
    placas_validas = [
        "ABC1D23",      # ✅ Mercosul
        "ABC1234",      # ✅ Antigo
        "abc1d23",      # ✅ Mercosul minúsculo (deve converter)
        "abc-1234",     # ✅ Antigo com hífen
        "ABC 1D23",     # ✅ Mercosul com espaço
    ]
    
    for placa in placas_validas:
        try:
            carro.placa = placa
            print(f"✅ '{placa}' -> '{carro.placa}' (válida)")
        except ValueError as e:
            print(f"❌ '{placa}' -> {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    print("🧪 TESTADOR DE CRUDS - SISTEMA OFICINA (CARROS)")
    print("=" * 60)
    
    # Executar testes
    sucesso_crud = test_carro_crud()
    sucesso_validacoes = test_validacoes_carro()
    test_placas_validas()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES - CARRO:")
    print(f"   CRUDs: {'✅ PASSOU' if sucesso_crud else '❌ FALHOU'}")
    print(f"   Validações: {'✅ PASSOU' if sucesso_validacoes else '❌ FALHOU'}")
    
    if sucesso_crud and sucesso_validacoes:
        print("\n🎉🎉🎉 TODOS OS TESTES DE CARRO FORAM BEM-SUCEDIDOS! 🎉🎉🎉")
        print("Sistema de carros pronto para uso! 🚗💨")
    else:
        print("\n💥 ALGUNS TESTES FALHARAM! Verifique o código.")
    
    print("=" * 60)