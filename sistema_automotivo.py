#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Peças Automotivas - Módulo Principal
Extração de dados da internet com informações de compatibilidade
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PecaAutomotiva:
    nome: str
    categoria: str
    preco: Optional[float]
    fabricante: str
    codigo_peca: str
    aplicacao: str
    descricao: str
    url_fonte: str
    montadora: str = "Não especificado"
    modelo_carro: str = "Não especificado"
    motor: str = "Não especificado"
    anos_compativel: str = "Consultar"
    # Campos específicos para radiadores
    tipo_radiador: str = "Não especificado"  # Behr, Valeo, Brasado, Canelado
    dimensoes: str = "Não especificado"      # Largo/Fino, medidas específicas
    lado_aplicacao: str = "Não especificado" # Superior, Inferior, Lateral
    material: str = "Não especificado"       # Plástico, Alumínio, Metal
    codigo_original: str = "Não especificado" # Código da montadora original

@dataclass
class Cliente:
    nome: str
    endereco: str
    telefone: str
    email: str
    marca_carro: str
    modelo_carro: str
    ano_carro: int

class DatabaseManager:
    def __init__(self, db_name="automotivas.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabela de categorias de peças
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) UNIQUE NOT NULL,
                descricao TEXT
            )
        ''')
        
        # Tabela de peças automotivas
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
                url_fonte TEXT,
                montadora VARCHAR(50),
                modelo_carro VARCHAR(100),
                motor VARCHAR(50),
                anos_compativel VARCHAR(100),
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        # Adicionar colunas se não existirem (para compatibilidade com bancos existentes)
        try:
            cursor.execute('ALTER TABLE pecas ADD COLUMN montadora VARCHAR(50)')
        except sqlite3.OperationalError:
            pass  # Coluna já existe
            
        try:
            cursor.execute('ALTER TABLE pecas ADD COLUMN modelo_carro VARCHAR(100)')
        except sqlite3.OperationalError:
            pass  # Coluna já existe
            
        try:
            cursor.execute('ALTER TABLE pecas ADD COLUMN motor VARCHAR(50)')
        except sqlite3.OperationalError:
            pass  # Coluna já existe
            
        try:
            cursor.execute('ALTER TABLE pecas ADD COLUMN anos_compativel VARCHAR(100)')
        except sqlite3.OperationalError:
            pass  # Coluna já existe

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
        
        # Tabela de vendas/pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'pendente',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabela de itens da venda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER,
                peca_id INTEGER,
                quantidade INTEGER,
                preco_unitario DECIMAL(10,2),
                FOREIGN KEY (venda_id) REFERENCES vendas (id),
                FOREIGN KEY (peca_id) REFERENCES pecas (id)
            )
        ''')
        
        # Inserir categorias padrão
        categorias_default = [
            'Motor', 'Suspensão', 'Arrefecimento', 'Ar Condicionado',
            'Injeção Eletrônica', 'Freios', 'Elétrica', 'Transmissão'
        ]
        
        for categoria in categorias_default:
            cursor.execute('INSERT OR IGNORE INTO categorias (nome) VALUES (?)', (categoria,))
        
        conn.commit()
        conn.close()
        logger.info("Banco de dados inicializado com sucesso")

    def inserir_peca(self, peca: PecaAutomotiva):
        """Insere uma peça no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Buscar ID da categoria
        cursor.execute('SELECT id FROM categorias WHERE nome = ?', (peca.categoria,))
        categoria_result = cursor.fetchone()
        categoria_id = categoria_result[0] if categoria_result else None
        
        cursor.execute('''
            INSERT INTO pecas (nome, categoria_id, preco, fabricante, codigo_peca, 
                             aplicacao, descricao, url_fonte, montadora, modelo_carro, 
                             motor, anos_compativel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (peca.nome, categoria_id, peca.preco, peca.fabricante, 
              peca.codigo_peca, peca.aplicacao, peca.descricao, peca.url_fonte,
              peca.montadora, peca.modelo_carro, peca.motor, peca.anos_compativel))
        
        conn.commit()
        conn.close()
        logger.info(f"Peça '{peca.nome}' inserida no banco de dados")
    
    def inserir_cliente(self, cliente: Cliente):
        """Insere um cliente no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nome, endereco, telefone, email, marca_carro, 
                                modelo_carro, ano_carro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cliente.nome, cliente.endereco, cliente.telefone, cliente.email,
              cliente.marca_carro, cliente.modelo_carro, cliente.ano_carro))
        
        conn.commit()
        conn.close()
        logger.info(f"Cliente '{cliente.nome}' inserido no banco de dados")
    
    def buscar_pecas(self, categoria=None, fabricante=None, limite=None):
        """Busca peças no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT p.*, c.nome as categoria_nome
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if categoria:
            query += ' AND c.nome = ?'
            params.append(categoria)
        
        if fabricante:
            query += ' AND p.fabricante LIKE ?'
            params.append(f'%{fabricante}%')
        
        if limite:
            query += f' LIMIT {limite}'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def buscar_clientes(self, nome=None, marca_carro=None):
        """Busca clientes no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        
        query = 'SELECT * FROM clientes WHERE 1=1'
        params = []
        
        if nome:
            query += ' AND nome LIKE ?'
            params.append(f'%{nome}%')
        
        if marca_carro:
            query += ' AND marca_carro LIKE ?'
            params.append(f'%{marca_carro}%')
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extrair_pecas_mercadolivre(self, termo_busca, max_resultados=10):
        """Extrai informações de peças do MercadoLivre"""
        pecas = []
        try:
            url_busca = f"https://lista.mercadolivre.com.br/{termo_busca.replace(' ', '-')}"
            response = requests.get(url_busca, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                produtos = soup.find_all('div', class_='ui-search-result__wrapper')
                
                for produto in produtos[:max_resultados]:
                    try:
                        # Extrair nome
                        nome_elem = produto.find('h2', class_='ui-search-item__title')
                        nome = nome_elem.get_text().strip() if nome_elem else 'Produto sem nome'
                        
                        # Extrair preço
                        preco_elem = produto.find('span', class_='andes-money-amount__fraction')
                        preco_str = '0'
                        if preco_elem:
                            preco_text = preco_elem.get_text()
                            preco_str = ''.join(filter(str.isdigit, preco_text.replace('.', '').replace(',', '.')))
                        
                        try:
                            preco = float(preco_str) / 100 if len(preco_str) > 2 else float(preco_str)
                        except:
                            preco = 0.0
                        
                        # Extrair URL
                        link_elem = produto.find('a', class_='ui-search-link')
                        url_produto = link_elem.get('href') if link_elem else ''
                        
                        # Gerar compatibilidade para a peça
                        categoria = self._categorizar_peca(nome)
                        compatibilidade = self._gerar_compatibilidade_veiculo(nome, categoria)
                        
                        peca = PecaAutomotiva(
                            nome=nome,
                            categoria=categoria,
                            preco=preco,
                            fabricante='Variado',
                            codigo_peca=f'ML{hash(nome) % 100000}',
                            aplicacao=f"{compatibilidade['montadora']} {compatibilidade['modelo']} ({compatibilidade['motor']}) - {compatibilidade['anos']}",
                            descricao=nome,
                            url_fonte=url_produto,
                            montadora=compatibilidade['montadora'],
                            modelo_carro=compatibilidade['modelo'],
                            motor=compatibilidade['motor'],
                            anos_compativel=compatibilidade['anos']
                        )
                        
                        pecas.append(peca)
                        
                    except Exception as e:
                        logger.error(f"Erro ao extrair produto: {e}")
                        continue
                
                logger.info(f"Extraídas {len(pecas)} peças do MercadoLivre para '{termo_busca}'")
            
        except Exception as e:
            logger.error(f"Erro ao acessar MercadoLivre: {e}")
        
        return pecas
    
    def extrair_pecas_centauro(self, termo_busca, max_resultados=10):
        """Extrai informações de peças da Centauro"""
        pecas = []
        try:
            # Simulação de dados da Centauro (site real possui proteção anti-bot)
            termo_clean = termo_busca.lower().replace(' ', '_')
            
            # Mock de dados para demonstração
            produtos_mock = [
                {"nome": f"Filtro de Óleo {termo_busca}", "preco": 25.90},
                {"nome": f"Pastilha de Freio {termo_busca}", "preco": 85.50},
                {"nome": f"Amortecedor {termo_busca}", "preco": 180.00},
                {"nome": f"Vela de Ignição {termo_busca}", "preco": 32.90},
                {"nome": f"Correia Dentada {termo_busca}", "preco": 120.00}
            ]
            
            for i, item in enumerate(produtos_mock[:max_resultados]):
                # Gerar compatibilidade para a peça
                categoria = self._categorizar_peca(item['nome'])
                compatibilidade = self._gerar_compatibilidade_veiculo(item['nome'], categoria)
                
                peca = PecaAutomotiva(
                    nome=item['nome'],
                    categoria=categoria,
                    preco=item['preco'],
                    fabricante='Centauro',
                    codigo_peca=f'CEN{hash(item["nome"]) % 100000}',
                    aplicacao=f"{compatibilidade['montadora']} {compatibilidade['modelo']} ({compatibilidade['motor']}) - {compatibilidade['anos']}",
                    descricao=item['nome'],
                    url_fonte='https://www.centauro.com.br',
                    montadora=compatibilidade['montadora'],
                    modelo_carro=compatibilidade['modelo'],
                    motor=compatibilidade['motor'],
                    anos_compativel=compatibilidade['anos']
                )
                
                pecas.append(peca)
            
            logger.info(f"Extraídas {len(pecas)} peças do Centauro para '{termo_busca}'")
            
        except Exception as e:
            logger.error(f"Erro ao acessar Centauro: {e}")
        
        return pecas
    
    def extrair_pecas_nakata(self, termo_busca, max_resultados=10):
        """Extrai informações de peças da Nakata"""
        # Simulação de dados da Nakata (site real requer autenticação)
        pecas_nakata = [
            {"nome": "Amortecedor Dianteiro Nakata", "preco": 185.90, "categoria": "Suspensão"},
            {"nome": "Pastilha de Freio Nakata", "preco": 89.50, "categoria": "Freios"},
            {"nome": "Disco de Freio Nakata", "preco": 120.00, "categoria": "Freios"},
            {"nome": "Filtro de Ar Nakata", "preco": 35.80, "categoria": "Motor"},
            {"nome": "Vela de Ignição Nakata", "preco": 28.90, "categoria": "Motor"},
            {"nome": "Correia Dentada Nakata", "preco": 95.00, "categoria": "Motor"},
            {"nome": "Bomba D'água Nakata", "preco": 150.00, "categoria": "Arrefecimento"},
            {"nome": "Radiador Nakata", "preco": 380.00, "categoria": "Arrefecimento"},
            {"nome": "Compressor A/C Nakata", "preco": 520.00, "categoria": "Ar Condicionado"},
            {"nome": "Alternador Nakata", "preco": 280.00, "categoria": "Elétrica"}
        ]
        
        pecas = []
        categoria_busca = self._categorizar_peca(termo_busca)
        
        for item in pecas_nakata:
            if categoria_busca.lower() in item['nome'].lower() or termo_busca.lower() in item['nome'].lower():
                # Gerar compatibilidade para a peça
                compatibilidade = self._gerar_compatibilidade_veiculo(item['nome'], item['categoria'])
                
                peca = PecaAutomotiva(
                    nome=item['nome'],
                    categoria=item['categoria'],
                    preco=item['preco'],
                    fabricante='Nakata',
                    codigo_peca=f'NAK{hash(item["nome"]) % 100000}',
                    aplicacao=f"{compatibilidade['montadora']} {compatibilidade['modelo']} ({compatibilidade['motor']}) - {compatibilidade['anos']}",
                    descricao=f'{item["nome"]} - Peça original Nakata',
                    url_fonte='https://www.nakata.com.br',
                    montadora=compatibilidade['montadora'],
                    modelo_carro=compatibilidade['modelo'],
                    motor=compatibilidade['motor'],
                    anos_compativel=compatibilidade['anos']
                )
                pecas.append(peca)
        
        logger.info(f"Extraídas {len(pecas)} peças da Nakata para '{termo_busca}'")
        return pecas[:max_resultados]
    
    def extrair_pecas_autopecas(self, termo_busca, max_resultados=10):
        """Extrai dados de peças de fornecedores especializados"""
        pecas_especializadas = [
            # Motor
            {"nome": "Kit Embreagem Sachs", "preco": 420.00, "categoria": "Transmissão", "fabricante": "Sachs"},
            {"nome": "Vela Ignição NGK Iridium", "preco": 45.90, "categoria": "Motor", "fabricante": "NGK"},
            {"nome": "Filtro Combustível Bosch", "preco": 32.50, "categoria": "Motor", "fabricante": "Bosch"},
            {"nome": "Bomba Combustível Delphi", "preco": 180.00, "categoria": "Injeção Eletrônica", "fabricante": "Delphi"},
            
            # Suspensão
            {"nome": "Amortecedor Monroe Original", "preco": 195.00, "categoria": "Suspensão", "fabricante": "Monroe"},
            {"nome": "Mola Suspensão Fabrini", "preco": 120.00, "categoria": "Suspensão", "fabricante": "Fabrini"},
            {"nome": "Braço Suspensão TRW", "preco": 85.00, "categoria": "Suspensão", "fabricante": "TRW"},
            
            # Freios
            {"nome": "Pastilha Freio Fras-le", "preco": 65.00, "categoria": "Freios", "fabricante": "Fras-le"},
            {"nome": "Disco Freio Fremax", "preco": 95.00, "categoria": "Freios", "fabricante": "Fremax"},
            {"nome": "Fluido Freio DOT4", "preco": 18.50, "categoria": "Freios", "fabricante": "Bosch"},
            
            # RADIADORES ESPECÍFICOS COM DETALHES TÉCNICOS
            
            # VOLKSWAGEN GOL
            {"nome": "Radiador Completo VW Gol G5/G6 1.0/1.6 8V Flex Valeo", "preco": 385.90, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Caixa Superior Radiador VW Gol G5/G6 Valeo 5U0121253A", "preco": 95.50, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Caixa Inferior Radiador VW Gol G5/G6 Valeo 5U0121253B", "preco": 95.50, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Kit Caixas Radiador VW Gol G5/G6 Original Valeo", "preco": 175.90, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            
            # CHEVROLET ONIX
            {"nome": "Radiador Completo Chevrolet Onix 1.0/1.4 8V Flex Behr", "preco": 395.00, "categoria": "Arrefecimento", "fabricante": "Behr"},
            {"nome": "Caixa Superior Radiador Onix Behr 94755531A", "preco": 89.90, "categoria": "Arrefecimento", "fabricante": "Behr"},
            {"nome": "Caixa Inferior Radiador Onix Behr 94755531B", "preco": 89.90, "categoria": "Arrefecimento", "fabricante": "Behr"},
            {"nome": "Kit Caixas Radiador Onix Original Behr", "preco": 165.80, "categoria": "Arrefecimento", "fabricante": "Behr"},
            
            # FORD KA
            {"nome": "Radiador Completo Ford Ka 1.0/1.5 12V Flex Denso", "preco": 375.50, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Superior Radiador Ford Ka Denso BB5Z8005B", "preco": 82.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Inferior Radiador Ford Ka Denso BB5Z8005C", "preco": 82.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Kit Caixas Radiador Ford Ka Original Denso", "preco": 155.80, "categoria": "Arrefecimento", "fabricante": "Denso"},
            
            # FIAT UNO
            {"nome": "Radiador Completo Fiat Uno Vivace 1.0/1.4 8V Magneti Marelli", "preco": 365.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
            {"nome": "Caixa Superior Radiador Fiat Uno Magneti 51897162A", "preco": 78.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
            {"nome": "Caixa Inferior Radiador Fiat Uno Magneti 51897162B", "preco": 78.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
            {"nome": "Kit Caixas Radiador Fiat Uno Original Magneti", "preco": 145.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
            
            # HONDA CIVIC
            {"nome": "Radiador Completo Honda Civic 1.5 Turbo/2.0 N/A Denso", "preco": 485.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Superior Radiador Honda Civic Denso 19015-5AA-A01", "preco": 125.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Inferior Radiador Honda Civic Denso 19020-5AA-A01", "preco": 125.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Kit Caixas Radiador Honda Civic Original Denso", "preco": 235.80, "categoria": "Arrefecimento", "fabricante": "Denso"},
            
            # TOYOTA COROLLA
            {"nome": "Radiador Completo Toyota Corolla 1.8/2.0 16V Flex Denso", "preco": 495.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Superior Radiador Toyota Corolla Denso 16405-0T040", "preco": 135.50, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Caixa Inferior Radiador Toyota Corolla Denso 16410-0T040", "preco": 135.50, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Kit Caixas Radiador Toyota Corolla Original Denso", "preco": 255.90, "categoria": "Arrefecimento", "fabricante": "Denso"},
            
            # HYUNDAI HB20
            {"nome": "Radiador Completo Hyundai HB20 1.0/1.6 16V Flex Mobis", "preco": 395.90, "categoria": "Arrefecimento", "fabricante": "Mobis"},
            {"nome": "Caixa Superior Radiador HB20 Mobis 25311-1R000", "preco": 92.50, "categoria": "Arrefecimento", "fabricante": "Mobis"},
            {"nome": "Caixa Inferior Radiador HB20 Mobis 25312-1R000", "preco": 92.50, "categoria": "Arrefecimento", "fabricante": "Mobis"},
            {"nome": "Kit Caixas Radiador HB20 Original Mobis", "preco": 175.90, "categoria": "Arrefecimento", "fabricante": "Mobis"},
            
            # NISSAN MARCH
            {"nome": "Radiador Completo Nissan March 1.0/1.6 16V Flex Calsonic", "preco": 385.50, "categoria": "Arrefecimento", "fabricante": "Calsonic Kansei"},
            {"nome": "Caixa Superior Radiador March Calsonic 21415-1HA0A", "preco": 88.90, "categoria": "Arrefecimento", "fabricante": "Calsonic Kansei"},
            {"nome": "Caixa Inferior Radiador March Calsonic 21420-1HA0A", "preco": 88.90, "categoria": "Arrefecimento", "fabricante": "Calsonic Kansei"},
            {"nome": "Kit Caixas Radiador March Original Calsonic", "preco": 165.80, "categoria": "Arrefecimento", "fabricante": "Calsonic Kansei"},
            
            # Ar Condicionado
            {"nome": "Compressor A/C Denso", "preco": 480.00, "categoria": "Ar Condicionado", "fabricante": "Denso"},
            {"nome": "Condensador A/C", "preco": 220.00, "categoria": "Ar Condicionado", "fabricante": "Valeo"},
            {"nome": "Filtro Cabine Bosch", "preco": 35.00, "categoria": "Ar Condicionado", "fabricante": "Bosch"},
            
            # Elétrica
            {"nome": "Bateria 60Ah Moura", "preco": 320.00, "categoria": "Elétrica", "fabricante": "Moura"},
            {"nome": "Alternador Valeo", "preco": 380.00, "categoria": "Elétrica", "fabricante": "Valeo"},
            {"nome": "Motor Arranque Bosch", "preco": 420.00, "categoria": "Elétrica", "fabricante": "Bosch"},
            
            # Injeção Eletrônica
            {"nome": "Bico Injetor Bosch", "preco": 95.00, "categoria": "Injeção Eletrônica", "fabricante": "Bosch"},
            {"nome": "Sensor Oxigênio NGK", "preco": 180.00, "categoria": "Injeção Eletrônica", "fabricante": "NGK"},
            {"nome": "Corpo Borboleta Magneti", "preco": 350.00, "categoria": "Injeção Eletrônica", "fabricante": "Magneti Marelli"}
        ]
        
        pecas = []
        termo_lower = termo_busca.lower()
        
        # Filtrar peças relevantes com prioridade para modelo específico
        pecas_modelo_especifico = []
        pecas_categoria_geral = []
        
        # Identificar se o usuário especificou um modelo de carro
        modelos_carros = ['gol', 'onix', 'ka', 'uno', 'civic', 'corolla', 'hb20', 'march', 'fiesta', 'palio', 'celta', 'corsa', 'fox', 'polo', 'voyage', 'prisma', 'focus', 'ecosport', 'punto', 'argo', 'fit', 'city', 'etios', 'yaris', 'i30', 'elantra', 'versa', 'sentra']
        modelo_especificado = None
        
        for modelo in modelos_carros:
            if modelo in termo_lower:
                modelo_especificado = modelo
                break
        
        for item in pecas_especializadas:
            nome_lower = item['nome'].lower()
            categoria_lower = item['categoria'].lower()
            
            # Se o usuário especificou um modelo, priorizar peças desse modelo
            if modelo_especificado:
                if modelo_especificado in nome_lower:
                    # Match exato do modelo - prioridade máxima
                    if (termo_lower.replace(modelo_especificado, '').strip() in nome_lower or 
                        termo_lower in categoria_lower):
                        pecas_modelo_especifico.append(item)
                # Caso não encontre o modelo específico na base, verificar se é da categoria certa
                elif (termo_lower.replace(modelo_especificado, '').strip() in nome_lower or 
                      termo_lower.replace(modelo_especificado, '').strip() in categoria_lower):
                    # Apenas se for da categoria específica (radiador, caixa, etc.)
                    if any(palavra in nome_lower for palavra in ['radiador', 'caixa']):
                        continue  # Pular peças que não são do modelo específico
            else:
                # Busca geral sem modelo específico
                if (termo_lower in nome_lower or 
                    termo_lower in categoria_lower or
                    any(palavra in nome_lower for palavra in termo_lower.split())):
                    pecas_categoria_geral.append(item)
        
        # Priorizar peças do modelo específico
        items_para_processar = pecas_modelo_especifico if pecas_modelo_especifico else pecas_categoria_geral
        
        for item in items_para_processar:
                
                # Gerar compatibilidade para a peça
                compatibilidade = self._gerar_compatibilidade_veiculo(item['nome'], item['categoria'])
                
                peca = PecaAutomotiva(
                    nome=item['nome'],
                    categoria=item['categoria'],
                    preco=item['preco'],
                    fabricante=item['fabricante'],
                    codigo_peca=f'{item["fabricante"][:3].upper()}{hash(item["nome"]) % 10000}',
                    aplicacao=f"{compatibilidade['montadora']} {compatibilidade['modelo']} ({compatibilidade['motor']}) - {compatibilidade['anos']}",
                    descricao=f'{item["nome"]} - {item["fabricante"]} Original',
                    url_fonte='https://autopecas.com.br',
                    montadora=compatibilidade['montadora'],
                    modelo_carro=compatibilidade['modelo'],
                    motor=compatibilidade['motor'],
                    anos_compativel=compatibilidade['anos'],
                    tipo_radiador=compatibilidade.get('tipo_radiador', 'Não especificado'),
                    dimensoes=compatibilidade.get('dimensoes', 'Não especificado'),
                    lado_aplicacao='Superior' if 'superior' in item['nome'].lower() else 'Inferior' if 'inferior' in item['nome'].lower() else 'Completo',
                    material=compatibilidade.get('material', 'Não especificado'),
                    codigo_original=compatibilidade.get('codigo_original', 'Não especificado')
                )
                pecas.append(peca)
        
        logger.info(f"Extraídas {len(pecas)} peças especializadas para '{termo_busca}'")
        return pecas[:max_resultados]
    
    def _categorizar_peca(self, nome_peca):
        """Categoriza uma peça baseada no nome"""
        nome_lower = nome_peca.lower()
        
        categorias_keywords = {
            'Motor': ['motor', 'pistão', 'válvula', 'vela', 'correia dentada', 'cabeçote', 'bloco', 'filtro oleo', 'filtro ar', 'filtro combustivel'],
            'Suspensão': ['amortecedor', 'mola', 'suspensão', 'braço', 'bandeja', 'pivô', 'bieleta', 'batente', 'coxim'],
            'Arrefecimento': ['radiador', 'ventoinha', 'termostato', 'bomba d\'água', 'mangueira', 'caixa radiador', 'caixas radiador', 'caixa de radiador', 'caixas de radiador', 'reservatorio agua', 'sensor temperatura', 'tampa radiador', 'fluido radiador', 'kit caixas', 'plastica radiador', 'aluminio radiador', 'superior radiador', 'inferior radiador'],
            'Ar Condicionado': ['compressor', 'condensador', 'evaporador', 'filtro do ar', 'filtro cabine', 'gas refrigerante', 'valvula expansao'],
            'Injeção Eletrônica': ['bico injetor', 'corpo de borboleta', 'sensor', 'módulo', 'chicote', 'sonda lambda', 'maf', 'map', 'tps'],
            'Freios': ['pastilha', 'disco de freio', 'tambor', 'cilindro', 'fluido de freio', 'lonas freio', 'mangueira freio', 'servo freio'],
            'Elétrica': ['bateria', 'alternador', 'motor de arranque', 'fusível', 'relé', 'chicote eletrico', 'lampada', 'farol'],
            'Transmissão': ['embreagem', 'câmbio', 'diferencial', 'semieixo', 'disco embreagem', 'platô', 'rolamento']
        }
        
        for categoria, keywords in categorias_keywords.items():
            if any(keyword in nome_lower for keyword in keywords):
                return categoria
        
        return 'Motor'  # Categoria padrão
    
    def _gerar_compatibilidade_veiculo(self, nome_peca, categoria):
        """Gera informações de compatibilidade específicas baseadas na peça e categoria"""
        nome_lower = nome_peca.lower()
        
        # Base de dados ESPECÍFICA de peças automotivas brasileiras
        pecas_especificas = {
            # RADIADORES - VOLKSWAGEN GOL
            'radiador gol': {
                'montadora': 'Volkswagen', 'modelo': 'Gol G5/G6', 'motor': '1.0/1.6 8V Flex',
                'anos': '2008-2016', 'tipo_radiador': 'Valeo', 'dimensoes': '480x335x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '5U0121253'
            },
            'caixa radiador gol': {
                'montadora': 'Volkswagen', 'modelo': 'Gol G5/G6', 'motor': '1.0/1.6 8V Flex',
                'anos': '2008-2016', 'tipo_radiador': 'Valeo', 'dimensoes': 'Superior 480mm',
                'material': 'Plástico PA66', 'codigo_original': '5U0121253A'
            },
            
            # RADIADORES - CHEVROLET ONIX
            'radiador onix': {
                'montadora': 'Chevrolet', 'modelo': 'Onix 1ª Geração', 'motor': '1.0/1.4 8V Flex',
                'anos': '2012-2019', 'tipo_radiador': 'Behr', 'dimensoes': '485x340x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '94755531'
            },
            'caixa radiador onix': {
                'montadora': 'Chevrolet', 'modelo': 'Onix 1ª Geração', 'motor': '1.0/1.4 8V Flex',
                'anos': '2012-2019', 'tipo_radiador': 'Behr', 'dimensoes': 'Superior 485mm',
                'material': 'Plástico PA66', 'codigo_original': '94755531A'
            },
            
            # RADIADORES - FORD KA
            'radiador ka': {
                'montadora': 'Ford', 'modelo': 'Ka 2ª Geração', 'motor': '1.0/1.5 12V Flex',
                'anos': '2014-2021', 'tipo_radiador': 'Denso', 'dimensoes': '450x320x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': 'BB5Z8005A'
            },
            'caixa radiador ka': {
                'montadora': 'Ford', 'modelo': 'Ka 2ª Geração', 'motor': '1.0/1.5 12V Flex',
                'anos': '2014-2021', 'tipo_radiador': 'Denso', 'dimensoes': 'Superior 450mm',
                'material': 'Plástico ABS', 'codigo_original': 'BB5Z8005B'
            },
            
            # RADIADORES - FIAT UNO
            'radiador uno': {
                'montadora': 'Fiat', 'modelo': 'Uno Vivace/Way', 'motor': '1.0/1.4 8V Flex',
                'anos': '2010-2020', 'tipo_radiador': 'Magneti Marelli', 'dimensoes': '440x315x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '51897162'
            },
            'caixa radiador uno': {
                'montadora': 'Fiat', 'modelo': 'Uno Vivace/Way', 'motor': '1.0/1.4 8V Flex',
                'anos': '2010-2020', 'tipo_radiador': 'Magneti Marelli', 'dimensoes': 'Superior 440mm',
                'material': 'Plástico ABS', 'codigo_original': '51897162A'
            },
            
            # RADIADORES - HONDA CIVIC
            'radiador civic': {
                'montadora': 'Honda', 'modelo': 'Civic 10ª Geração', 'motor': '1.5 Turbo/2.0 N/A',
                'anos': '2016-2023', 'tipo_radiador': 'Denso', 'dimensoes': '520x365x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '19010-5AA-A01'
            },
            'caixa radiador civic': {
                'montadora': 'Honda', 'modelo': 'Civic 10ª Geração', 'motor': '1.5 Turbo/2.0 N/A',
                'anos': '2016-2023', 'tipo_radiador': 'Denso', 'dimensoes': 'Superior 520mm',
                'material': 'Plástico PA66', 'codigo_original': '19015-5AA-A01'
            },
            
            # RADIADORES - TOYOTA COROLLA
            'radiador corolla': {
                'montadora': 'Toyota', 'modelo': 'Corolla GLi/XEi/Altis', 'motor': '1.8/2.0 16V Flex',
                'anos': '2014-2019', 'tipo_radiador': 'Denso', 'dimensoes': '540x380x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '16400-0T040'
            },
            'caixa radiador corolla': {
                'montadora': 'Toyota', 'modelo': 'Corolla GLi/XEi/Altis', 'motor': '1.8/2.0 16V Flex',
                'anos': '2014-2019', 'tipo_radiador': 'Denso', 'dimensoes': 'Superior 540mm',
                'material': 'Plástico PA66', 'codigo_original': '16405-0T040'
            },
            
            # RADIADORES - HYUNDAI HB20
            'radiador hb20': {
                'montadora': 'Hyundai', 'modelo': 'HB20 1ª Geração', 'motor': '1.0/1.6 16V Flex',
                'anos': '2012-2019', 'tipo_radiador': 'Mobis', 'dimensoes': '470x335x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '25310-1R000'
            },
            'caixa radiador hb20': {
                'montadora': 'Hyundai', 'modelo': 'HB20 1ª Geração', 'motor': '1.0/1.6 16V Flex',
                'anos': '2012-2019', 'tipo_radiador': 'Mobis', 'dimensoes': 'Superior 470mm',
                'material': 'Plástico ABS', 'codigo_original': '25311-1R000'
            },
            
            # RADIADORES - NISSAN MARCH
            'radiador march': {
                'montadora': 'Nissan', 'modelo': 'March 1ª Geração', 'motor': '1.0/1.6 16V Flex',
                'anos': '2011-2018', 'tipo_radiador': 'Calsonic Kansei', 'dimensoes': '460x320x26mm',
                'material': 'Alumínio/Plástico', 'codigo_original': '21410-1HA0A'
            },
            'caixa radiador march': {
                'montadora': 'Nissan', 'modelo': 'March 1ª Geração', 'motor': '1.0/1.6 16V Flex',
                'anos': '2011-2018', 'tipo_radiador': 'Calsonic Kansei', 'dimensoes': 'Superior 460mm',
                'material': 'Plástico ABS', 'codigo_original': '21415-1HA0A'
            }
        }
        
        # Tentar match exato primeiro
        for chave, info in pecas_especificas.items():
            if chave in nome_lower:
                return info
        
        # Tentar match por marca
        if 'gol' in nome_lower:
            return pecas_especificas['radiador gol']
        elif 'onix' in nome_lower:
            return pecas_especificas['radiador onix']
        elif 'ka' in nome_lower and 'ford' in nome_lower:
            return pecas_especificas['radiador ka']
        elif 'uno' in nome_lower:
            return pecas_especificas['radiador uno']
        elif 'civic' in nome_lower:
            return pecas_especificas['radiador civic']
        elif 'corolla' in nome_lower:
            return pecas_especificas['radiador corolla']
        elif 'hb20' in nome_lower:
            return pecas_especificas['radiador hb20']
        elif 'march' in nome_lower:
            return pecas_especificas['radiador march']
        
        # Se não encontrar match específico, retornar informação de consulta
        return {
            'montadora': 'Consultar aplicação',
            'modelo': 'Verificar compatibilidade',
            'motor': 'Consultar ficha técnica',
            'anos': 'Verificar ano do veículo',
            'tipo_radiador': 'Consultar tipo original',
            'dimensoes': 'Medir radiador original',
            'material': 'Verificar especificação',
            'codigo_original': 'Consultar catálogo'
        }

class SistemaAutomotivo:
    def __init__(self):
        self.db = DatabaseManager()
        self.scraper = WebScraper()
    
    def atualizar_pecas_internet(self):
        """Atualiza o banco de dados com peças da internet"""
        termos_busca = [
            'peças motor carro',
            'amortecedor suspensão',
            'radiador arrefecimento',
            'compressor ar condicionado',
            'bico injetor eletrônica',
            'pastilha freio',
            'alternador bateria',
            'embreagem transmissão'
        ]
        
        for termo in termos_busca:
            print(f"🔍 Buscando: {termo}")
            
            # Extrair do MercadoLivre
            pecas_ml = self.scraper.extrair_pecas_mercadolivre(termo, 3)
            
            # Extrair da Centauro 
            pecas_centauro = self.scraper.extrair_pecas_centauro(termo, 3)
            
            # Extrair da Nakata
            pecas_nakata = self.scraper.extrair_pecas_nakata(termo, 2)
            
            # Combinar todas as peças
            todas_pecas = pecas_ml + pecas_centauro + pecas_nakata
            
            # Inserir no banco
            for peca in todas_pecas:
                try:
                    self.db.inserir_peca(peca)
                except Exception as e:
                    logger.error(f"Erro ao inserir peça: {e}")
            
            time.sleep(1)  # Pausa entre requisições
    
    def buscar_pecas(self, termo_busca):
        """Busca peças no banco local"""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        
        query = '''
            SELECT p.nome, c.nome as categoria, p.preco, p.fabricante, p.codigo_peca, 
                   p.aplicacao, p.montadora, p.modelo_carro, p.motor, p.anos_compativel
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nome LIKE ? OR p.descricao LIKE ? OR p.aplicacao LIKE ?
            ORDER BY p.preco ASC
        '''
        
        termo_like = f'%{termo_busca}%'
        cursor.execute(query, (termo_like, termo_like, termo_like))
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def buscar_pecas_por_categoria(self, categoria):
        """Busca peças por categoria específica"""
        conn = sqlite3.connect(self.db.db_name)
        
        query = '''
            SELECT p.nome, c.nome as categoria, p.preco, p.fabricante, p.aplicacao, 
                   p.montadora, p.modelo_carro, p.motor, p.anos_compativel
            FROM pecas p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE c.nome = ?
            ORDER BY p.preco ASC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
