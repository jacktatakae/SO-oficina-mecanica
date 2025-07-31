import pandas as pd
import sqlite3
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class ImportadorDados:
    def __init__(self, db_name="automotivas.db"):
        self.db_name = db_name
    
    def importar_pecas_csv(self, arquivo_csv):
        """Importa peças de um arquivo CSV
        
        Formato esperado do CSV:
        nome,categoria,preco,fabricante,codigo_peca,aplicacao,descricao
        """
        try:
            df = pd.read_csv(arquivo_csv)
            
            # Validar colunas obrigatórias
            colunas_necessarias = ['nome', 'categoria', 'preco', 'fabricante', 'codigo_peca']
            for coluna in colunas_necessarias:
                if coluna not in df.columns:
                    raise ValueError(f"Coluna '{coluna}' não encontrada no CSV")
            
            conn = sqlite3.connect(self.db_name)
            
            # Buscar IDs das categorias
            categorias_map = {}
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome FROM categorias')
            for cat_id, cat_nome in cursor.fetchall():
                categorias_map[cat_nome] = cat_id
            
            # Inserir peças
            pecas_inseridas = 0
            for _, row in df.iterrows():
                categoria_id = categorias_map.get(row['categoria'])
                
                cursor.execute('''
                    INSERT INTO pecas (nome, categoria_id, preco, fabricante, codigo_peca, 
                                     aplicacao, descricao, url_fonte)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['nome'],
                    categoria_id,
                    float(row['preco']) if pd.notna(row['preco']) else 0,
                    row['fabricante'],
                    row['codigo_peca'],
                    row.get('aplicacao', ''),
                    row.get('descricao', ''),
                    row.get('url_fonte', '')
                ))
                pecas_inseridas += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Importadas {pecas_inseridas} peças do arquivo {arquivo_csv}")
            return pecas_inseridas
            
        except Exception as e:
            logger.error(f"Erro ao importar peças do CSV: {e}")
            return 0
    
    def importar_clientes_csv(self, arquivo_csv):
        """Importa clientes de um arquivo CSV
        
        Formato esperado do CSV:
        nome,endereco,telefone,email,marca_carro,modelo_carro,ano_carro
        """
        try:
            df = pd.read_csv(arquivo_csv)
            
            # Validar colunas obrigatórias
            colunas_necessarias = ['nome', 'endereco', 'telefone', 'email', 'marca_carro', 'modelo_carro', 'ano_carro']
            for coluna in colunas_necessarias:
                if coluna not in df.columns:
                    raise ValueError(f"Coluna '{coluna}' não encontrada no CSV")
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Inserir clientes
            clientes_inseridos = 0
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO clientes (nome, endereco, telefone, email, marca_carro, 
                                        modelo_carro, ano_carro)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['nome'],
                    row['endereco'],
                    row['telefone'],
                    row['email'],
                    row['marca_carro'],
                    row['modelo_carro'],
                    int(row['ano_carro']) if pd.notna(row['ano_carro']) else 2020
                ))
                clientes_inseridos += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Importados {clientes_inseridos} clientes do arquivo {arquivo_csv}")
            return clientes_inseridos
            
        except Exception as e:
            logger.error(f"Erro ao importar clientes do CSV: {e}")
            return 0
    
    def exportar_pecas_csv(self, arquivo_saida="pecas_export.csv", categoria=None):
        """Exporta peças para um arquivo CSV"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT 
                p.nome,
                c.nome as categoria,
                p.preco,
                p.fabricante,
                p.codigo_peca,
                p.aplicacao,
                p.descricao,
                p.url_fonte,
                p.data_atualizacao
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        '''
        
        params = []
        if categoria:
            query += ' WHERE c.nome = ?'
            params.append(categoria)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        df.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        logger.info(f"Peças exportadas para {arquivo_saida}")
        return len(df)
    
    def exportar_clientes_csv(self, arquivo_saida="clientes_export.csv"):
        """Exporta clientes para um arquivo CSV"""
        conn = sqlite3.connect(self.db_name)
        
        df = pd.read_sql_query('SELECT * FROM clientes', conn)
        conn.close()
        
        df.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        logger.info(f"Clientes exportados para {arquivo_saida}")
        return len(df)
    
    def criar_templates_csv(self):
        """Cria templates CSV de exemplo"""
        
        # Template de peças
        pecas_template = pd.DataFrame({
            'nome': ['Vela de Ignição NGK', 'Amortecedor Dianteiro', 'Radiador Completo'],
            'categoria': ['Motor', 'Suspensão', 'Arrefecimento'],
            'preco': [25.90, 180.00, 320.50],
            'fabricante': ['NGK', 'Monroe', 'Valeo'],
            'codigo_peca': ['NGK001', 'MON456', 'VAL789'],
            'aplicacao': ['Universal', 'Gol/Palio', 'Civic 2006-2012'],
            'descricao': ['Vela padrão resistiva', 'Amortecedor original', 'Radiador com garantia']
        })
        
        pecas_template.to_csv('template_pecas.csv', index=False, encoding='utf-8-sig')
        
        # Template de clientes
        clientes_template = pd.DataFrame({
            'nome': ['João Silva', 'Maria Santos', 'Pedro Costa'],
            'endereco': ['Rua A, 123', 'Av. B, 456', 'Rua C, 789'],
            'telefone': ['11999999999', '11888888888', '11777777777'],
            'email': ['joao@email.com', 'maria@email.com', 'pedro@email.com'],
            'marca_carro': ['Volkswagen', 'Fiat', 'Honda'],
            'modelo_carro': ['Gol', 'Palio', 'Civic'],
            'ano_carro': [2018, 2015, 2020]
        })
        
        clientes_template.to_csv('template_clientes.csv', index=False, encoding='utf-8-sig')
        
        print("✅ Templates criados:")
        print("  - template_pecas.csv")
        print("  - template_clientes.csv")

def exemplo_importacao():
    """Exemplo de como usar o importador"""
    importador = ImportadorDados()
    
    print("📥 SISTEMA DE IMPORTAÇÃO/EXPORTAÇÃO")
    print("="*40)
    
    # Criar templates
    print("\n1. Criando templates CSV...")
    importador.criar_templates_csv()
    
    # Verificar se existem templates para importar
    if os.path.exists('template_pecas.csv'):
        print("\n2. Importando peças do template...")
        pecas_importadas = importador.importar_pecas_csv('template_pecas.csv')
        print(f"   ✅ {pecas_importadas} peças importadas")
    
    if os.path.exists('template_clientes.csv'):
        print("\n3. Importando clientes do template...")
        clientes_importados = importador.importar_clientes_csv('template_clientes.csv')
        print(f"   ✅ {clientes_importados} clientes importados")
    
    # Exportar dados
    print("\n4. Exportando dados...")
    pecas_exportadas = importador.exportar_pecas_csv("backup_pecas.csv")
    clientes_exportados = importador.exportar_clientes_csv("backup_clientes.csv")
    
    print(f"   ✅ {pecas_exportadas} peças exportadas para backup_pecas.csv")
    print(f"   ✅ {clientes_exportados} clientes exportados para backup_clientes.csv")

if __name__ == "__main__":
    exemplo_importacao()
