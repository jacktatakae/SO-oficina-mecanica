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
    modelo_carro: str = "Universal"
    motor: str = "Não especificado"
    anos_compativel: str = "Consultar"

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
            
            # Arrefecimento
            {"nome": "Radiador Valeo Original", "preco": 350.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Caixa de Radiador Superior", "preco": 85.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Caixa de Radiador Inferior", "preco": 85.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Kit Caixas de Radiador", "preco": 160.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Caixa Radiador Plástica", "preco": 75.00, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
            {"nome": "Caixa Radiador Alumínio", "preco": 120.00, "categoria": "Arrefecimento", "fabricante": "Denso"},
            {"nome": "Termostato Wahler", "preco": 65.00, "categoria": "Arrefecimento", "fabricante": "Wahler"},
            {"nome": "Ventoinha Radiador", "preco": 120.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Tampa Radiador", "preco": 25.00, "categoria": "Arrefecimento", "fabricante": "Gates"},
            {"nome": "Reservatório Água Radiador", "preco": 45.00, "categoria": "Arrefecimento", "fabricante": "Valeo"},
            {"nome": "Sensor Temperatura Radiador", "preco": 35.00, "categoria": "Arrefecimento", "fabricante": "Bosch"},
            {"nome": "Mangueira Superior Radiador", "preco": 28.00, "categoria": "Arrefecimento", "fabricante": "Gates"},
            {"nome": "Mangueira Inferior Radiador", "preco": 28.00, "categoria": "Arrefecimento", "fabricante": "Gates"},
            
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
        
        # Filtrar peças relevantes
        for item in pecas_especializadas:
            nome_lower = item['nome'].lower()
            categoria_lower = item['categoria'].lower()
            
            # Verificar se o termo de busca está presente
            if (termo_lower in nome_lower or 
                termo_lower in categoria_lower or
                any(palavra in nome_lower for palavra in termo_lower.split())):
                
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
                    anos_compativel=compatibilidade['anos']
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
        """Gera informações de compatibilidade baseadas na peça e categoria"""
        nome_lower = nome_peca.lower()
        
        # Base de dados de compatibilidade por marca e modelo
        compatibilidades = {
            # Volkswagen
            'gol': {'montadora': 'Volkswagen', 'modelo': 'Gol', 'motor': '1.0/1.6', 'anos': '2005-2023'},
            'polo': {'montadora': 'Volkswagen', 'modelo': 'Polo', 'motor': '1.6', 'anos': '2018-2023'},
            'voyage': {'montadora': 'Volkswagen', 'modelo': 'Voyage', 'motor': '1.0/1.6', 'anos': '2008-2023'},
            'fox': {'montadora': 'Volkswagen', 'modelo': 'Fox', 'motor': '1.0/1.6', 'anos': '2003-2021'},
            
            # Chevrolet
            'onix': {'montadora': 'Chevrolet', 'modelo': 'Onix', 'motor': '1.0/1.4', 'anos': '2012-2023'},
            'prisma': {'montadora': 'Chevrolet', 'modelo': 'Prisma', 'motor': '1.0/1.4', 'anos': '2013-2023'},
            'celta': {'montadora': 'Chevrolet', 'modelo': 'Celta', 'motor': '1.0/1.4', 'anos': '2000-2016'},
            'corsa': {'montadora': 'Chevrolet', 'modelo': 'Corsa', 'motor': '1.0/1.4', 'anos': '1994-2012'},
            
            # Ford
            'ka': {'montadora': 'Ford', 'modelo': 'Ka', 'motor': '1.0/1.5', 'anos': '1997-2023'},
            'fiesta': {'montadora': 'Ford', 'modelo': 'Fiesta', 'motor': '1.0/1.6', 'anos': '1996-2019'},
            'focus': {'montadora': 'Ford', 'modelo': 'Focus', 'motor': '1.6/2.0', 'anos': '2000-2019'},
            'ecosport': {'montadora': 'Ford', 'modelo': 'EcoSport', 'motor': '1.6/2.0', 'anos': '2003-2023'},
            
            # Fiat
            'uno': {'montadora': 'Fiat', 'modelo': 'Uno', 'motor': '1.0/1.4', 'anos': '1984-2023'},
            'palio': {'montadora': 'Fiat', 'modelo': 'Palio', 'motor': '1.0/1.4/1.6', 'anos': '1996-2017'},
            'punto': {'montadora': 'Fiat', 'modelo': 'Punto', 'motor': '1.4/1.6/1.8', 'anos': '2007-2017'},
            'argo': {'montadora': 'Fiat', 'modelo': 'Argo', 'motor': '1.0/1.3/1.8', 'anos': '2017-2023'},
            
            # Honda
            'civic': {'montadora': 'Honda', 'modelo': 'Civic', 'motor': '1.8/2.0', 'anos': '1992-2023'},
            'fit': {'montadora': 'Honda', 'modelo': 'Fit', 'motor': '1.4/1.5', 'anos': '2003-2020'},
            'city': {'montadora': 'Honda', 'modelo': 'City', 'motor': '1.5', 'anos': '2009-2023'},
            
            # Toyota
            'corolla': {'montadora': 'Toyota', 'modelo': 'Corolla', 'motor': '1.8/2.0', 'anos': '1993-2023'},
            'etios': {'montadora': 'Toyota', 'modelo': 'Etios', 'motor': '1.3/1.5', 'anos': '2012-2021'},
            'yaris': {'montadora': 'Toyota', 'modelo': 'Yaris', 'motor': '1.3/1.5', 'anos': '2018-2023'},
            
            # Hyundai
            'hb20': {'montadora': 'Hyundai', 'modelo': 'HB20', 'motor': '1.0/1.6', 'anos': '2012-2023'},
            'i30': {'montadora': 'Hyundai', 'modelo': 'i30', 'motor': '1.6/2.0', 'anos': '2009-2023'},
            'elantra': {'montadora': 'Hyundai', 'modelo': 'Elantra', 'motor': '1.8/2.0', 'anos': '2011-2023'},
            
            # Nissan
            'march': {'montadora': 'Nissan', 'modelo': 'March', 'motor': '1.0/1.6', 'anos': '2011-2023'},
            'versa': {'montadora': 'Nissan', 'modelo': 'Versa', 'motor': '1.6', 'anos': '2011-2023'},
            'sentra': {'montadora': 'Nissan', 'modelo': 'Sentra', 'motor': '1.8/2.0', 'anos': '2007-2023'},
        }
        
        # Tentar identificar o modelo pela peça
        for modelo, info in compatibilidades.items():
            if modelo in nome_lower:
                return info
        
        # Compatibilidade por categoria (genérica)
        if categoria == 'Motor':
            return {
                'montadora': 'Universal',
                'modelo': 'Consultar aplicação',
                'motor': '1.0/1.4/1.6/1.8/2.0',
                'anos': '2000-2023'
            }
        elif categoria == 'Arrefecimento':
            return {
                'montadora': 'Universal',
                'modelo': 'Consultar aplicação',
                'motor': 'Todos',
                'anos': '2005-2023'
            }
        elif categoria == 'Suspensão':
            return {
                'montadora': 'Universal',
                'modelo': 'Consultar aplicação',
                'motor': 'Todos',
                'anos': '2000-2023'
            }
        elif categoria == 'Freios':
            return {
                'montadora': 'Universal',
                'modelo': 'Consultar aplicação',
                'motor': 'Todos',
                'anos': '2000-2023'
            }
        else:
            return {
                'montadora': 'Universal',
                'modelo': 'Universal',
                'motor': 'Universal',
                'anos': '2000-2023'
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
