#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para busca de caixas de radiador com compatibilidade
"""

from sistema_automotivo import SistemaAutomotivo

def testar_busca_radiador():
    """Testa a busca por caixas de radiador com informações de compatibilidade"""
    print("🔍 TESTANDO BUSCA POR CAIXAS DE RADIADOR COM COMPATIBILIDADE")
    print("=" * 70)
    
    sistema = SistemaAutomotivo()
    
    # Termos de busca para testar
    termos_teste = [
        "caixas de radiador",
        "caixa de radiador",
        "radiador"
    ]
    
    for termo in termos_teste:
        print(f"\n🔍 Buscando: '{termo}'")
        print("-" * 50)
        
        # Busca no banco local
        pecas_local = sistema.buscar_pecas(termo)
        
        if pecas_local:
            print(f"✅ Encontradas {len(pecas_local)} peças no banco local:")
            for i, peca in enumerate(pecas_local[:3], 1):  # Limita a 3 resultados
                nome, categoria, preco, fabricante, codigo, aplicacao, montadora, modelo, motor, anos = peca
                preco_str = f"R$ {preco:.2f}" if preco > 0 else "Sob consulta"
                
                print(f"  {i}. {nome} - {preco_str}")
                print(f"     Categoria: {categoria} | Fabricante: {fabricante}")
                
                if montadora and montadora != "Não especificado":
                    print(f"     🚗 Compatível: {montadora} {modelo} ({motor}) - Anos: {anos}")
                else:
                    print(f"     📋 Aplicação: {aplicacao}")
                print()
        else:
            print("❌ Nenhuma peça encontrada no banco local")
        
        # Busca na internet (base especializada)
        print(f"🌐 Buscando na base especializada...")
        pecas_internet = sistema.scraper.extrair_pecas_autopecas(termo, max_resultados=3)
        
        if pecas_internet:
            print(f"✅ Encontradas {len(pecas_internet)} peças especializadas:")
            for i, peca in enumerate(pecas_internet, 1):
                print(f"  {i}. {peca.nome}")
                print(f"     💰 Preço: R$ {peca.preco:.2f}")
                print(f"     🏭 Fabricante: {peca.fabricante}")
                print(f"     🚗 Aplicação: {peca.montadora} {peca.modelo_carro}")
                print(f"     � Motor: {peca.motor} | Anos: {peca.anos_compativel}")
                
                # Informações específicas de radiador
                if hasattr(peca, 'tipo_radiador') and peca.tipo_radiador != "Não especificado":
                    print(f"     📦 Tipo: {peca.tipo_radiador} | Dimensões: {peca.dimensoes}")
                    print(f"     🔩 Material: {peca.material} | Lado: {peca.lado_aplicacao}")
                    print(f"     📋 Código Original: {peca.codigo_original}")
                print()
        else:
            print("❌ Nenhuma peça encontrada na base especializada")
        
        print("=" * 70)

if __name__ == "__main__":
    testar_busca_radiador()
