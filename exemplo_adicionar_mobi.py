#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO PRÁTICO: Adicionando Fiat Mobi ao Sistema
=================================================
"""

# Vou demonstrar adicionando o Fiat Mobi como exemplo

# PASSO 1: Adicionar 'mobi' na lista de modelos reconhecidos
print("🔧 PASSO 1: Adicionando na lista de modelos...")

# Na linha ~505 do sistema_automotivo.py, mude de:
# modelos_carros = ['gol', 'onix', 'ka', 'uno', 'civic', ...]
# Para:
# modelos_carros = ['gol', 'onix', 'ka', 'uno', 'mobi', 'civic', ...]

print("✅ Adicione 'mobi' na lista modelos_carros")

# PASSO 2: Adicionar especificações técnicas
print("\n🔧 PASSO 2: Adicionando especificações técnicas...")

especificacoes_mobi = {
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
    }
}

print("✅ Adicione essas especificações no dicionário pecas_especificas")

# PASSO 3: Adicionar peças do modelo
print("\n🔧 PASSO 3: Adicionando peças específicas...")

pecas_mobi = [
    # FIAT MOBI
    {"nome": "Radiador Completo Fiat Mobi 1.0 8V Flex Magneti Marelli", "preco": 345.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
    {"nome": "Caixa Superior Radiador Fiat Mobi Magneti 51932077A", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
    {"nome": "Caixa Inferior Radiador Fiat Mobi Magneti 51932077B", "preco": 72.50, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
    {"nome": "Kit Caixas Radiador Fiat Mobi Original Magneti", "preco": 135.90, "categoria": "Arrefecimento", "fabricante": "Magneti Marelli"},
]

print("✅ Adicione essas peças na lista pecas_especializadas")

# PASSO 4: Adicionar match de busca
print("\n🔧 PASSO 4: Adicionando match de busca...")

print("✅ Adicione esta linha no bloco de matches:")
print("elif 'mobi' in nome_lower:")
print("    return pecas_especificas['radiador mobi']")

# RESULTADO ESPERADO
print("\n🎯 RESULTADO ESPERADO:")
print("Após essas mudanças, quando buscar 'caixa radiador mobi':")
print("- Sistema vai reconhecer 'mobi' como modelo específico")
print("- Vai trazer apenas peças do Fiat Mobi")
print("- Com todas as especificações técnicas corretas")

# LOCALIZAÇÕES EXATAS NO CÓDIGO
print("\n📍 LOCALIZAÇÕES EXATAS NO ARQUIVO sistema_automotivo.py:")
print("1. Lista modelos_carros: ~linha 505")
print("2. Dicionário pecas_especificas: ~linha 265-330")
print("3. Lista pecas_especializadas: ~linha 420-480") 
print("4. Bloco de matches: ~linha 325-340")

print("\n🔍 TESTE:")
print("Execute: py teste_busca_modelo.py")
print("Busque: 'caixa radiador mobi'")
print("Deve trazer apenas peças do Fiat Mobi!")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("📋 RESUMO DOS 4 PASSOS:")
    print("1. ✅ Adicionar 'mobi' na lista modelos_carros")
    print("2. ✅ Adicionar especificações no pecas_especificas") 
    print("3. ✅ Adicionar peças na lista pecas_especializadas")
    print("4. ✅ Adicionar match 'elif mobi in nome_lower'")
    print("="*50)
