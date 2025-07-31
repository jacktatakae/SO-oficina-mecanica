#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUIA COMPLETO: Como Adicionar Novos Modelos de Carros
=====================================================

Para adicionar um novo modelo de carro ao sistema, siga estes 4 passos:

EXEMPLO: Vamos adicionar o FIAT MOBI
"""

# PASSO 1: Adicionar o modelo na lista de reconhecimento
# =====================================================
# Arquivo: sistema_automotivo.py
# Localização: Função extrair_pecas_autopecas(), linha ~505

"""
ANTES:
modelos_carros = ['gol', 'onix', 'ka', 'uno', 'civic', 'corolla', 'hb20', 'march', ...]

DEPOIS:
modelos_carros = ['gol', 'onix', 'ka', 'uno', 'mobi', 'civic', 'corolla', 'hb20', 'march', ...]
                                           ^^^^^^ 
                                        ADICIONE AQUI
"""

# PASSO 2: Adicionar as especificações técnicas do modelo
# =======================================================
# Arquivo: sistema_automotivo.py
# Localização: Função _gerar_compatibilidade_veiculo(), dentro de pecas_especificas

"""
ADICIONE no dicionário pecas_especificas:

# RADIADORES - FIAT MOBI
'radiador mobi': {
    'montadora': 'Fiat', 
    'modelo': 'Mobi Like/Way', 
    'motor': '1.0 8V Flex',
    'anos': '2016-2023', 
    'tipo_radiador': 'Magneti Marelli', 
    'dimensoes': '420x310x26mm',
    'material': 'Alumínio/Plástico', 
    'codigo_original': '51932077'
},
'caixa radiador mobi': {
    'montadora': 'Fiat', 
    'modelo': 'Mobi Like/Way', 
    'motor': '1.0 8V Flex',
    'anos': '2016-2023', 
    'tipo_radiador': 'Magneti Marelli', 
    'dimensoes': 'Superior 420mm',
    'material': 'Plástico ABS', 
    'codigo_original': '51932077A'
},
"""

# PASSO 3: Adicionar as peças específicas do modelo
# =================================================
# Arquivo: sistema_automotivo.py
# Localização: Função extrair_pecas_autopecas(), dentro de pecas_especializadas

"""
ADICIONE na lista pecas_especializadas:

# FIAT MOBI
{"nome": "Radiador Completo Fiat Mobi 1.0 8V Flex Magneti Marelli", "preco": 345.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
{"nome": "Caixa Superior Radiador Fiat Mobi Magneti 51932077A", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
{"nome": "Caixa Inferior Radiador Fiat Mobi Magneti 51932077B", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
{"nome": "Kit Caixas Radiador Fiat Mobi Original Magneti", "preco": 135.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
"""

# PASSO 4: Adicionar o match no sistema de busca
# ==============================================
# Arquivo: sistema_automotivo.py
# Localização: Função _gerar_compatibilidade_veiculo(), no final

"""
ADICIONE no bloco de matches por marca:

elif 'mobi' in nome_lower:
    return pecas_especificas['radiador mobi']
"""

# EXEMPLO COMPLETO DE IMPLEMENTAÇÃO:
# ==================================

def exemplo_adicionar_fiat_mobi():
    """
    Exemplo completo de como ficaria o código após adicionar o Fiat Mobi
    """
    
    # 1. Lista de modelos (linha ~505)
    modelos_carros = [
        'gol', 'onix', 'ka', 'uno', 'mobi',  # ← MOBI ADICIONADO
        'civic', 'corolla', 'hb20', 'march'
    ]
    
    # 2. Especificações técnicas (dentro de _gerar_compatibilidade_veiculo)
    pecas_especificas = {
        # ... outros modelos ...
        
        # FIAT MOBI - NOVO MODELO
        'radiador mobi': {
            'montadora': 'Fiat', 
            'modelo': 'Mobi Like/Way', 
            'motor': '1.0 8V Flex',
            'anos': '2016-2023', 
            'tipo_radiador': 'Magneti Marelli', 
            'dimensoes': '420x310x26mm',
            'material': 'Alumínio/Plástico', 
            'codigo_original': '51932077'
        },
        'caixa radiador mobi': {
            'montadora': 'Fiat', 
            'modelo': 'Mobi Like/Way', 
            'motor': '1.0 8V Flex',
            'anos': '2016-2023', 
            'tipo_radiador': 'Magneti Marelli', 
            'dimensoes': 'Superior 420mm',
            'material': 'Plástico ABS', 
            'codigo_original': '51932077A'
        }
    }
    
    # 3. Peças específicas (dentro de extrair_pecas_autopecas)
    pecas_especializadas = [
        # ... outras peças ...
        
        # FIAT MOBI - NOVAS PEÇAS
        {"nome": "Radiador Completo Fiat Mobi 1.0 8V Flex Magneti Marelli", "preco": 345.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
        {"nome": "Caixa Superior Radiador Fiat Mobi Magneti 51932077A", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
        {"nome": "Caixa Inferior Radiador Fiat Mobi Magneti 51932077B", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
        {"nome": "Kit Caixas Radiador Fiat Mobi Original Magneti", "preco": 135.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
    ]
    
    # 4. Match no sistema de busca (dentro de _gerar_compatibilidade_veiculo)
    if 'mobi' in nome_lower:
        return pecas_especificas['radiador mobi']

# INFORMAÇÕES TÉCNICAS NECESSÁRIAS:
# =================================

"""
Para adicionar um modelo novo, você precisa pesquisar:

1. MONTADORA: Fiat, Volkswagen, Chevrolet, etc.
2. MODELO COMPLETO: Mobi Like/Way, Gol G5/G6, etc.
3. MOTORES: 1.0 8V Flex, 1.6 16V, 1.5 Turbo, etc.
4. ANOS: 2016-2023, 2008-2016, etc.
5. FABRICANTE DO RADIADOR: Valeo, Behr, Denso, Magneti Marelli, etc.
6. DIMENSÕES: 420x310x26mm (Comprimento x Altura x Espessura)
7. MATERIAL: Alumínio/Plástico, PA66, ABS, etc.
8. CÓDIGO ORIGINAL: Código da montadora (ex: 51932077)
9. PREÇOS: Pesquisar preços de mercado atuais

FONTES DE INFORMAÇÃO:
- Catálogos de autopeças
- Sites de fabricantes (Valeo, Behr, Denso)
- Sistemas de consulta automotiva
- Concessionárias da marca
"""

print("📋 GUIA COMPLETO PARA ADICIONAR NOVOS MODELOS")
print("=" * 50)
print("✅ Siga os 4 passos acima")
print("✅ Pesquise as informações técnicas necessárias")
print("✅ Teste a busca após adicionar")
print("=" * 50)
