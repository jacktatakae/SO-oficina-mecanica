#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para busca de caixas de radiador
"""

from sistema_automotivo import SistemaAutomotivo

def testar_busca_radiador():
    """Testa a busca por caixas de radiador"""
    print("🔍 TESTANDO BUSCA POR CAIXAS DE RADIADOR")
    print("=" * 50)
    
    sistema = SistemaAutomotivo()
    
    # Termos de busca para testar
    termos_teste = [
        "caixas de radiador",
        "caixa de radiador",
        "caixa radiador",
        "caixas radiador",
        "radiador"
    ]
    
    for termo in termos_teste:
        print(f"\n🔍 Buscando: '{termo}'")
        print("-" * 40)
        
        # Busca no banco local
        pecas_local = sistema.buscar_pecas(termo)
        
        if pecas_local:
            print(f"✅ Encontradas {len(pecas_local)} peças no banco local:")
            for i, peca in enumerate(pecas_local[:5], 1):  # Limita a 5 resultados
                print(f"  {i}. {peca[1]} - R$ {peca[2]:.2f} ({peca[3]})")
        else:
            print("❌ Nenhuma peça encontrada no banco local")
        
        # Busca na internet (base especializada)
        print(f"\n🌐 Buscando na base especializada...")
        pecas_internet = sistema.scraper.extrair_pecas_autopecas(termo, max_resultados=5)
        
        if pecas_internet:
            print(f"✅ Encontradas {len(pecas_internet)} peças especializadas:")
            for i, peca in enumerate(pecas_internet, 1):
                print(f"  {i}. {peca.nome} - R$ {peca.preco:.2f} ({peca.categoria})")
                if hasattr(peca, 'montadora') and peca.montadora != "Não especificado":
                    print(f"      🚗 Compatível: {peca.montadora} {peca.modelo_carro} ({peca.motor}) - {peca.anos_compativel}")
        else:
            print("❌ Nenhuma peça encontrada na base especializada")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    testar_busca_radiador()
