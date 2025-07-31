#!/usr/bin/env python3
"""
DEMONSTRAÇÃO SIMPLES - Sistema de Peças Automotivas
Versão sem dependências externas - apenas SQLite nativo
"""

import sqlite3
import json
from datetime import datetime
import os

class SistemaAutomotivoSimples:
    def __init__(self, db_name="automotivas_demo.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabela de categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) UNIQUE NOT NULL,
                descricao TEXT
            )
        ''')
        
        # Tabela de peças
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pecas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(200) NOT NULL,
                categoria_id INTEGER,
                preco DECIMAL(10,2),
                fabricante VARCHAR(100),
                codigo_peca VARCHAR(50),
                aplicacao TEXT,
                descricao TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(200) NOT NULL,
                endereco TEXT,
                telefone VARCHAR(20),
                email VARCHAR(100),
                marca_carro VARCHAR(50),
                modelo_carro VARCHAR(100),
                ano_carro INTEGER,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inserir categorias padrão
        categorias = [
            ('Motor', 'Peças relacionadas ao motor'),
            ('Suspensão', 'Sistema de suspensão'),
            ('Arrefecimento', 'Sistema de arrefecimento'),
            ('Ar Condicionado', 'Sistema de ar condicionado'),
            ('Injeção Eletrônica', 'Sistema de injeção eletrônica'),
            ('Freios', 'Sistema de freios'),
            ('Elétrica', 'Peças elétricas'),
            ('Transmissão', 'Peças da transmissão')
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO categorias (nome, descricao) VALUES (?, ?)',
            categorias
        )
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado!")
    
    def cadastrar_peca(self, nome, categoria, preco, fabricante, codigo, aplicacao="", descricao=""):
        """Cadastra uma nova peça"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Buscar ID da categoria
        cursor.execute('SELECT id FROM categorias WHERE nome = ?', (categoria,))
        resultado = cursor.fetchone()
        categoria_id = resultado[0] if resultado else None
        
        cursor.execute('''
            INSERT INTO pecas (nome, categoria_id, preco, fabricante, codigo_peca, aplicacao, descricao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, categoria_id, preco, fabricante, codigo, aplicacao, descricao))
        
        conn.commit()
        conn.close()
        print(f"✅ Peça '{nome}' cadastrada!")
    
    def cadastrar_cliente(self, nome, endereco, telefone, email, marca_carro, modelo_carro, ano_carro):
        """Cadastra um novo cliente"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nome, endereco, telefone, email, marca_carro, modelo_carro, ano_carro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, endereco, telefone, email, marca_carro, modelo_carro, ano_carro))
        
        conn.commit()
        conn.close()
        print(f"✅ Cliente '{nome}' cadastrado!")
    
    def listar_pecas(self, categoria=None, limite=None):
        """Lista peças cadastradas"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = '''
            SELECT p.nome, c.nome as categoria, p.preco, p.fabricante, p.codigo_peca, p.aplicacao
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        '''
        
        params = []
        if categoria:
            query += ' WHERE c.nome = ?'
            params.append(categoria)
        
        if limite:
            query += f' LIMIT {limite}'
        
        cursor.execute(query, params)
        pecas = cursor.fetchall()
        conn.close()
        
        return pecas
    
    def listar_clientes(self):
        """Lista clientes cadastrados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()
        conn.close()
        
        return clientes
    
    def estatisticas(self):
        """Mostra estatísticas do sistema"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Total de peças
        cursor.execute('SELECT COUNT(*) FROM pecas')
        total_pecas = cursor.fetchone()[0]
        
        # Total de clientes
        cursor.execute('SELECT COUNT(*) FROM clientes')
        total_clientes = cursor.fetchone()[0]
        
        # Preço médio
        cursor.execute('SELECT AVG(preco) FROM pecas WHERE preco > 0')
        preco_medio = cursor.fetchone()[0] or 0
        
        # Categoria com mais peças
        cursor.execute('''
            SELECT c.nome, COUNT(p.id) as total
            FROM categorias c
            LEFT JOIN pecas p ON c.id = p.categoria_id
            GROUP BY c.id, c.nome
            ORDER BY total DESC
            LIMIT 1
        ''')
        categoria_top = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_pecas': total_pecas,
            'total_clientes': total_clientes, 
            'preco_medio': round(preco_medio, 2),
            'categoria_top': categoria_top
        }
    
    def popular_dados_exemplo(self):
        """Popula o banco com dados de exemplo"""
        print("📊 Inserindo dados de exemplo...")
        
        # Peças de exemplo
        pecas_exemplo = [
            ("Vela de Ignição NGK", "Motor", 25.90, "NGK", "NGK001", "Universal", "Vela resistiva padrão"),
            ("Amortecedor Dianteiro", "Suspensão", 180.00, "Monroe", "MON456", "Gol/Palio", "Amortecedor original"),
            ("Radiador Completo", "Arrefecimento", 320.50, "Valeo", "VAL789", "Civic 2006-2012", "Radiador com garantia"),
            ("Compressor A/C", "Ar Condicionado", 450.00, "Denso", "DEN123", "Universal", "Compressor remanufaturado"),
            ("Bico Injetor", "Injeção Eletrônica", 85.00, "Bosch", "BSH999", "Flex", "Bico injetor multiponto"),
            ("Pastilha de Freio", "Freios", 45.00, "Frasle", "FRA555", "Dianteira", "Pastilha cerâmica"),
            ("Bateria 60Ah", "Elétrica", 280.00, "Moura", "MOU777", "Universal", "Bateria selada"),
            ("Kit Embreagem", "Transmissão", 380.00, "Sachs", "SAC888", "1.0/1.4", "Kit completo com disco e platô")
        ]
        
        for peca in pecas_exemplo:
            self.cadastrar_peca(*peca)
        
        # Clientes de exemplo
        clientes_exemplo = [
            ("João Silva", "Rua das Flores, 123", "11999999999", "joao@email.com", "Volkswagen", "Gol", 2018),
            ("Maria Santos", "Av. Paulista, 456", "11888888888", "maria@email.com", "Fiat", "Palio", 2015),
            ("Pedro Costa", "Rua da Paz, 789", "11777777777", "pedro@email.com", "Honda", "Civic", 2020),
            ("Ana Oliveira", "Av. Brasil, 321", "11666666666", "ana@email.com", "Chevrolet", "Onix", 2019),
            ("Carlos Souza", "Rua do Sol, 654", "11555555555", "carlos@email.com", "Toyota", "Corolla", 2021)
        ]
        
        for cliente in clientes_exemplo:
            self.cadastrar_cliente(*cliente)
        
        print("✅ Dados de exemplo inseridos!")

def menu_principal():
    """Menu principal do sistema"""
    sistema = SistemaAutomotivoSimples()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           🚗 SISTEMA DE PEÇAS AUTOMOTIVAS 🔧                ║
║                    VERSÃO DEMONSTRAÇÃO                       ║
║                  (Apenas SQLite nativo)                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n📋 MENU PRINCIPAL")
        print("="*30)
        print("1. 📊 Popular dados de exemplo")
        print("2. 🔧 Cadastrar peça")
        print("3. 👤 Cadastrar cliente")
        print("4. 📦 Listar peças")
        print("5. 👥 Listar clientes")
        print("6. 📈 Ver estatísticas")
        print("7. 🔍 Buscar peças por categoria")
        print("0. 🚪 Sair")
        
        opcao = input("\n➤ Escolha uma opção: ").strip()
        
        if opcao == '1':
            sistema.popular_dados_exemplo()
        
        elif opcao == '2':
            print("\n➕ CADASTRAR NOVA PEÇA")
            print("-" * 25)
            nome = input("Nome da peça: ").strip()
            
            print("\nCategorias disponíveis:")
            print("Motor, Suspensão, Arrefecimento, Ar Condicionado")
            print("Injeção Eletrônica, Freios, Elétrica, Transmissão")
            categoria = input("Categoria: ").strip()
            
            try:
                preco = float(input("Preço (R$): ").strip())
            except ValueError:
                preco = 0.0
            
            fabricante = input("Fabricante: ").strip()
            codigo = input("Código da peça: ").strip()
            aplicacao = input("Aplicação (opcional): ").strip()
            descricao = input("Descrição (opcional): ").strip()
            
            if nome and categoria and fabricante:
                sistema.cadastrar_peca(nome, categoria, preco, fabricante, codigo, aplicacao, descricao)
            else:
                print("❌ Nome, categoria e fabricante são obrigatórios!")
        
        elif opcao == '3':
            print("\n➕ CADASTRAR NOVO CLIENTE")
            print("-" * 25)
            nome = input("Nome completo: ").strip()
            endereco = input("Endereço: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            marca = input("Marca do carro: ").strip()
            modelo = input("Modelo do carro: ").strip()
            
            try:
                ano = int(input("Ano do carro: ").strip())
            except ValueError:
                ano = 2020
            
            if nome and endereco and telefone:
                sistema.cadastrar_cliente(nome, endereco, telefone, email, marca, modelo, ano)
            else:
                print("❌ Nome, endereço e telefone são obrigatórios!")
        
        elif opcao == '4':
            print("\n📦 LISTA DE PEÇAS")
            print("=" * 50)
            pecas = sistema.listar_pecas()
            
            if pecas:
                for peca in pecas:
                    nome, categoria, preco, fabricante, codigo, aplicacao = peca
                    preco_str = f"R$ {preco:.2f}" if preco > 0 else "Sob consulta"
                    print(f"• {nome}")
                    print(f"  Categoria: {categoria} | Preço: {preco_str}")
                    print(f"  Fabricante: {fabricante} | Código: {codigo}")
                    if aplicacao:
                        print(f"  Aplicação: {aplicacao}")
                    print()
            else:
                print("Nenhuma peça cadastrada.")
        
        elif opcao == '5':
            print("\n👥 LISTA DE CLIENTES") 
            print("=" * 50)
            clientes = sistema.listar_clientes()
            
            if clientes:
                for cliente in clientes:
                    _, nome, endereco, telefone, email, marca, modelo, ano, data = cliente
                    print(f"• {nome}")
                    print(f"  Telefone: {telefone} | Email: {email}")
                    print(f"  Carro: {marca} {modelo} ({ano})")
                    print(f"  Endereço: {endereco}")
                    print()
            else:
                print("Nenhum cliente cadastrado.")
        
        elif opcao == '6':
            print("\n📈 ESTATÍSTICAS DO SISTEMA")
            print("=" * 30)
            stats = sistema.estatisticas()
            
            print(f"🔧 Total de peças: {stats['total_pecas']}")
            print(f"👥 Total de clientes: {stats['total_clientes']}")
            print(f"💰 Preço médio das peças: R$ {stats['preco_medio']}")
            
            if stats['categoria_top']:
                categoria, total = stats['categoria_top']
                print(f"📦 Categoria com mais peças: {categoria} ({total} peças)")
        
        elif opcao == '7':
            print("\nCategorias disponíveis:")
            print("Motor, Suspensão, Arrefecimento, Ar Condicionado")
            print("Injeção Eletrônica, Freios, Elétrica, Transmissão")
            
            categoria = input("\nDigite a categoria: ").strip()
            
            if categoria:
                print(f"\n📦 PEÇAS DA CATEGORIA '{categoria.upper()}'")
                print("=" * 50)
                pecas = sistema.listar_pecas(categoria=categoria)
                
                if pecas:
                    for peca in pecas:
                        nome, cat, preco, fabricante, codigo, aplicacao = peca
                        preco_str = f"R$ {preco:.2f}" if preco > 0 else "Sob consulta"
                        print(f"• {nome} - {preco_str}")
                        print(f"  Fabricante: {fabricante} | Código: {codigo}")
                        if aplicacao:
                            print(f"  Aplicação: {aplicacao}")
                        print()
                else:
                    print(f"Nenhuma peça encontrada na categoria '{categoria}'")
        
        elif opcao == '0':
            print("\n👋 Obrigado por usar o Sistema de Peças Automotivas!")
            break
        
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema finalizado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
