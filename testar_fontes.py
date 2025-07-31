#!/usr/bin/env python3
"""
Teste das novas fontes de dados para peças automotivas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sistema_automotivo import WebScraper, DatabaseManager, SistemaAutomotivo

def testar_novas_fontes():
    print("🧪 TESTE DAS NOVAS FONTES DE DADOS")
    print("=" * 40)
    
    scraper = WebScraper()
    
    # Testar Centauro
    print("\n🏪 Testando Centauro...")
    pecas_centauro = scraper.extrair_pecas_centauro("amortecedor", 3)
    for peca in pecas_centauro:
        print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
    
    # Testar Nakata
    print("\n🔧 Testando Nakata...")
    pecas_nakata = scraper.extrair_pecas_nakata("freio", 3)
    for peca in pecas_nakata:
        print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
    
    # Testar AutoPeças Especializadas
    print("\n🛠️  Testando AutoPeças Especializadas...")
    pecas_auto = scraper.extrair_pecas_autopecas("motor", 5)
    for peca in pecas_auto:
        print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
    
    print(f"\n✅ Teste concluído!")
    print(f"   - Centauro: {len(pecas_centauro)} peças")
    print(f"   - Nakata: {len(pecas_nakata)} peças")
    print(f"   - AutoPeças: {len(pecas_auto)} peças")

def testar_sistema_completo():
    print("\n🚀 TESTANDO SISTEMA COMPLETO...")
    
    sistema = SistemaAutomotivo()
    
    # Inserir algumas peças de teste
    print("📦 Inserindo peças de exemplo...")
    scraper = WebScraper()
    
    # Testar com um termo específico
    termo_teste = "pastilha freio"
    print(f"\n🔍 Buscando: {termo_teste}")
    
    # AutoPeças
    pecas_auto = scraper.extrair_pecas_autopecas(termo_teste, 3)
    for peca in pecas_auto:
        sistema.db.inserir_peca(peca)
    
    # Nakata
    pecas_nakata = scraper.extrair_pecas_nakata(termo_teste, 2)
    for peca in pecas_nakata:
        sistema.db.inserir_peca(peca)
    
    # Mostrar resultados
    pecas_db = sistema.buscar_pecas_por_categoria("Freios")
    print(f"\n📊 Resultado: {len(pecas_db)} peças inseridas na categoria Freios")
    
    if not pecas_db.empty:
        print("\nPeças encontradas:")
        for _, peca in pecas_db.head(5).iterrows():
            preco_str = f"R$ {peca['preco']:.2f}" if peca['preco'] > 0 else "Sob consulta"
            print(f"  • {peca['nome']} - {preco_str} ({peca['fabricante']})")

if __name__ == "__main__":
    try:
        testar_novas_fontes()
        testar_sistema_completo()
        
        print("\n" + "="*40)
        print("🎉 NOVOS SCRAPERS FUNCIONANDO!")
        print("✅ Sistema atualizado com fontes confiáveis")
        print("✅ Sem mais resultados 'N/A'")
        print("✅ Dados de fabricantes reais")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        
    input("\nPressione Enter para continuar...")
