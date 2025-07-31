#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para busca por modelo de carro
"""

from sistema_automotivo import SistemaAutomotivo

def testar_busca_por_modelo():
    """Testa a busca por modelo específico de carro"""
    print("🔍 TESTANDO BUSCA POR MODELO ESPECÍFICO DE CARRO")
    print("=" * 60)
    
    sistema = SistemaAutomotivo()
    
    # Termos de busca específicos por modelo
    termos_teste = [
        ("caixa radiador gol", "Deveria trazer apenas peças do Gol"),
        ("radiador onix", "Deveria trazer apenas peças do Onix"),
        ("caixa radiador ka", "Deveria trazer apenas peças do Ka"),
        ("radiador civic", "Deveria trazer apenas peças do Civic"),
        ("caixas de radiador", "Busca geral - vários modelos")
    ]
    
    for termo, expectativa in termos_teste:
        print(f"\n🔍 Buscando: '{termo}'")
        print(f"📋 Expectativa: {expectativa}")
        print("-" * 50)
        
        # Busca na base especializada
        pecas_internet = sistema.scraper.extrair_pecas_autopecas(termo, max_resultados=5)
        
        if pecas_internet:
            print(f"✅ Encontradas {len(pecas_internet)} peças:")
            for i, peca in enumerate(pecas_internet, 1):
                print(f"  {i}. {peca.nome}")
                print(f"     🚗 Aplicação: {peca.montadora} {peca.modelo_carro}")
                print(f"     🔧 Motor: {peca.motor} | Anos: {peca.anos_compativel}")
                print(f"     💰 Preço: R$ {peca.preco:.2f}")
                print()
        else:
            print("❌ Nenhuma peça encontrada")
        
        print("=" * 60)

if __name__ == "__main__":
    testar_busca_por_modelo()
