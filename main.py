#!/usr/bin/env python3
"""
Sistema Completo de Gestão de Peças Automotivas
Desenvolvido para extrair informações da internet e gerenciar clientes
"""

import os
import sys
import sqlite3
import shutil
from sistema_automotivo import SistemaAutomotivo
from relatorios import RelatoriosAvancados
from importador import ImportadorDados

class MenuPrincipal:
    def __init__(self):
        self.sistema = SistemaAutomotivo()
        self.relatorios = RelatoriosAvancados()
        self.importador = ImportadorDados()
    
    def mostrar_banner(self):
        """Mostra o banner do sistema"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║           🚗 SISTEMA DE PEÇAS AUTOMOTIVAS 🔧                ║
║                                                              ║
║  Sistema completo para gestão de peças e clientes           ║
║  Com extração automática de dados da internet               ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            self.mostrar_banner()
            print("\n📋 MENU PRINCIPAL")
            print("="*30)
            print("1.  🌐 Extrair peças da internet")
            print("2.  👤 Gerenciar clientes")
            print("3.  🔍 Consultar peças")
            print("4.  📊 Relatórios e análises")
            print("5.  📥 Importar/Exportar dados")
            print("6.  ⚙️  Configurações")
            print("0.  🚪 Sair")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.menu_extracao()
            elif opcao == '2':
                self.menu_clientes()
            elif opcao == '3':
                self.menu_consultas()
            elif opcao == '4':
                self.menu_relatorios()
            elif opcao == '5':
                self.menu_importacao()
            elif opcao == '6':
                self.menu_configuracoes()
            elif opcao == '0':
                print("\n👋 Obrigado por usar o Sistema de Peças Automotivas!")
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def menu_extracao(self):
        """Menu para extração de dados da internet"""
        while True:
            print("\n🌐 EXTRAÇÃO DE DADOS DA INTERNET")
            print("="*35)
            print("1. Atualizar todas as categorias")
            print("2. Extrair peças específicas")
            print("3. Ver última atualização")
            print("0. Voltar ao menu principal")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                print("\n🔄 Iniciando extração completa...")
                print("⚠️  Este processo pode demorar alguns minutos...")
                confirmacao = input("Deseja continuar? (s/n): ").lower()
                
                if confirmacao == 's':
                    try:
                        self.sistema.atualizar_pecas_internet()
                        print("✅ Extração concluída com sucesso!")
                    except Exception as e:
                        print(f"❌ Erro durante a extração: {e}")
                
                input("\nPressione Enter para continuar...")
            
            elif opcao == '2':
                termo = input("Digite o termo de busca (ex: 'vela ignição'): ").strip()
                if termo:
                    print(f"\n🔍 Buscando por: {termo}")
                    try:
                        # Buscar usando as novas fontes
                        pecas_encontradas = []
                        
                        # Buscar no banco de dados local primeiro
                        todas_pecas = self.sistema.db.buscar_pecas()
                        if not todas_pecas.empty:
                            pecas_filtradas = todas_pecas[
                                todas_pecas['nome'].str.contains(termo, case=False, na=False) |
                                todas_pecas['descricao'].str.contains(termo, case=False, na=False)
                            ]
                            
                            if not pecas_filtradas.empty:
                                print(f"\n� Encontradas {len(pecas_filtradas)} peças no banco local:")
                                for _, peca in pecas_filtradas.head(5).iterrows():
                                    preco_str = f"R$ {peca['preco']:.2f}" if peca['preco'] > 0 else "Sob consulta"
                                    print(f"  • {peca['nome']} - {preco_str} ({peca['fabricante']})")
                            else:
                                print("❌ Nenhuma peça encontrada no banco local")
                        
                        # Buscar online se necessário
                        buscar_online = input("\nDeseja buscar online também? (s/n): ").lower()
                        if buscar_online == 's':
                            print("🌐 Buscando online...")
                            
                            # Usar as novas fontes
                            pecas_auto = self.sistema.scraper.extrair_pecas_autopecas(termo, 3)
                            pecas_nakata = self.sistema.scraper.extrair_pecas_nakata(termo, 2)
                            
                            total_online = len(pecas_auto) + len(pecas_nakata)
                            if total_online > 0:
                                print(f"\n🎯 Encontradas {total_online} peças online:")
                                
                                for peca in pecas_auto:
                                    print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
                                
                                for peca in pecas_nakata:
                                    print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
                            else:
                                print("❌ Nenhuma peça encontrada online")
                        
                    except Exception as e:
                        print(f"❌ Erro na busca: {e}")
                
                input("\nPressione Enter para continuar...")
            
            elif opcao == '3':
                # Mostrar estatísticas da última atualização
                stats = self.relatorios.estatisticas_gerais()
                print(f"\n📊 Total de peças no banco: {stats.get('total_pecas', 0)}")
                print(f"📊 Categorias ativas: {stats.get('categorias_ativas', 0)}")
                
                input("\nPressione Enter para continuar...")
            
            elif opcao == '0':
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def menu_clientes(self):
        """Menu para gerenciamento de clientes"""
        while True:
            print("\n👤 GERENCIAMENTO DE CLIENTES")
            print("="*30)
            print("1. Cadastrar novo cliente")
            print("2. Buscar cliente")
            print("3. Listar todos os clientes")
            print("4. Clientes por marca de carro")
            print("0. Voltar ao menu principal")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.cadastrar_cliente()
            elif opcao == '2':
                self.buscar_cliente()
            elif opcao == '3':
                self.listar_clientes()
            elif opcao == '4':
                self.clientes_por_marca()
            elif opcao == '0':
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        print("\n➕ CADASTRAR NOVO CLIENTE")
        print("-" * 25)
        
        try:
            nome = input("Nome completo: ").strip()
            endereco = input("Endereço: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            marca = input("Marca do carro: ").strip()
            modelo = input("Modelo do carro: ").strip()
            ano = int(input("Ano do carro: ").strip())
            
            if nome and endereco and telefone:
                resultado = self.sistema.cadastrar_cliente(
                    nome, endereco, telefone, email, marca, modelo, ano
                )
                print(f"\n✅ {resultado}")
            else:
                print("❌ Nome, endereço e telefone são obrigatórios!")
                
        except ValueError:
            print("❌ Ano deve ser um número!")
        except Exception as e:
            print(f"❌ Erro ao cadastrar cliente: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def buscar_cliente(self):
        """Busca cliente por nome"""
        nome = input("\n🔍 Digite o nome do cliente: ").strip()
        
        if nome:
            clientes = self.sistema.db.buscar_clientes(nome=nome)
            
            if not clientes.empty:
                print(f"\n👥 Clientes encontrados:")
                print("-" * 50)
                for _, cliente in clientes.iterrows():
                    print(f"Nome: {cliente['nome']}")
                    print(f"Telefone: {cliente['telefone']}")
                    print(f"Carro: {cliente['marca_carro']} {cliente['modelo_carro']} ({cliente['ano_carro']})")
                    print("-" * 50)
            else:
                print("❌ Nenhum cliente encontrado!")
        
        input("\nPressione Enter para continuar...")
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        clientes = self.sistema.db.buscar_clientes()
        
        if not clientes.empty:
            print(f"\n👥 TODOS OS CLIENTES ({len(clientes)} registros)")
            print("=" * 60)
            
            for _, cliente in clientes.iterrows():
                print(f"• {cliente['nome']} - {cliente['telefone']}")
                print(f"  {cliente['marca_carro']} {cliente['modelo_carro']} ({cliente['ano_carro']})")
                print()
        else:
            print("❌ Nenhum cliente cadastrado!")
        
        input("\nPressione Enter para continuar...")
    
    def clientes_por_marca(self):
        """Lista clientes por marca de carro"""
        marca = input("\n🚗 Digite a marca do carro: ").strip()
        
        if marca:
            clientes = self.sistema.buscar_clientes_por_marca(marca)
            
            if not clientes.empty:
                print(f"\n👥 Clientes com carros {marca}:")
                print("-" * 40)
                for _, cliente in clientes.iterrows():
                    print(f"• {cliente['nome']} - {cliente['modelo_carro']} ({cliente['ano_carro']})")
            else:
                print(f"❌ Nenhum cliente com carro {marca} encontrado!")
        
        input("\nPressione Enter para continuar...")
    
    def menu_consultas(self):
        """Menu para consultas de peças"""
        while True:
            print("\n🔍 CONSULTAS DE PEÇAS")
            print("="*22)
            print("1. Buscar por categoria")
            print("2. Buscar por fabricante")
            print("3. Buscar por nome/descrição")
            print("4. Peças mais caras")
            print("5. Peças mais baratas")
            print("0. Voltar ao menu principal")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.buscar_por_categoria()
            elif opcao == '2':
                self.buscar_por_fabricante()
            elif opcao == '3':
                self.buscar_por_nome()
            elif opcao == '4':
                self.pecas_mais_caras()
            elif opcao == '5':
                self.pecas_mais_baratas()
            elif opcao == '0':
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def buscar_por_categoria(self):
        """Busca peças por categoria"""
        print("\n📦 CATEGORIAS DISPONÍVEIS:")
        print("• Motor")
        print("• Suspensão")
        print("• Arrefecimento")
        print("• Ar Condicionado")
        print("• Injeção Eletrônica")
        print("• Freios")
        print("• Elétrica")
        print("• Transmissão")
        
        categoria = input("\nDigite a categoria: ").strip()
        
        if categoria:
            pecas = self.sistema.buscar_pecas_por_categoria(categoria)
            
            if not pecas.empty:
                print(f"\n🔧 Peças da categoria '{categoria}':")
                print("=" * 50)
                
                for _, peca in pecas.head(10).iterrows():  # Mostrar apenas 10 primeiras
                    preco_str = f"R$ {peca['preco']:.2f}" if peca['preco'] > 0 else "Preço sob consulta"
                    print(f"• {peca['nome']}")
                    print(f"  Fabricante: {peca['fabricante']} | Preço: {preco_str}")
                    print()
                
                if len(pecas) > 10:
                    print(f"... e mais {len(pecas) - 10} peças")
            else:
                print(f"❌ Nenhuma peça encontrada na categoria '{categoria}'!")
        
        input("\nPressione Enter para continuar...")
    
    def buscar_por_fabricante(self):
        """Busca peças por fabricante"""
        fabricante = input("\n🏭 Digite o fabricante: ").strip()
        
        if fabricante:
            pecas = self.sistema.db.buscar_pecas(fabricante=fabricante)
            
            if not pecas.empty:
                print(f"\n🔧 Peças do fabricante '{fabricante}':")
                print("=" * 50)
                
                for _, peca in pecas.head(10).iterrows():
                    preco_str = f"R$ {peca['preco']:.2f}" if peca['preco'] > 0 else "Sob consulta"
                    print(f"• {peca['nome']} - {preco_str}")
                    print(f"  Categoria: {peca['categoria_nome']}")
                    print()
            else:
                print(f"❌ Nenhuma peça do fabricante '{fabricante}' encontrada!")
        
        input("\nPressione Enter para continuar...")
    
    def buscar_por_nome(self):
        """Busca peças por nome/descrição"""
        nome_busca = input("\n🔍 Digite o nome ou descrição da peça: ").strip()
        
        if nome_busca:
            try:
                # Buscar no banco de dados
                conn = sqlite3.connect(self.sistema.db.db_name)
                
                query = '''
                    SELECT p.nome, c.nome as categoria, p.preco, p.fabricante, p.codigo_peca, p.aplicacao
                    FROM pecas p
                    LEFT JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.nome LIKE ? OR p.descricao LIKE ? OR p.aplicacao LIKE ?
                    ORDER BY p.preco ASC
                '''
                
                termo_like = f'%{nome_busca}%'
                cursor = conn.cursor()
                cursor.execute(query, (termo_like, termo_like, termo_like))
                resultados = cursor.fetchall()
                conn.close()
                
                if resultados:
                    print(f"\n� Encontradas {len(resultados)} peças:")
                    print("=" * 60)
                    
                    for resultado in resultados[:10]:  # Mostrar até 10 resultados
                        nome, categoria, preco, fabricante, codigo, aplicacao = resultado
                        preco_str = f"R$ {preco:.2f}" if preco > 0 else "Sob consulta"
                        
                        print(f"• {nome}")
                        print(f"  Categoria: {categoria} | Preço: {preco_str}")
                        print(f"  Fabricante: {fabricante} | Código: {codigo}")
                        if aplicacao:
                            print(f"  Aplicação: {aplicacao}")
                        print()
                    
                    if len(resultados) > 10:
                        print(f"... e mais {len(resultados) - 10} peças encontradas")
                else:
                    print(f"❌ Nenhuma peça encontrada com '{nome_busca}'")
                    
                    # Sugerir busca online
                    buscar_online = input("\nDeseja buscar online? (s/n): ").lower()
                    if buscar_online == 's':
                        print("🌐 Buscando online...")
                        
                        # Buscar nas fontes online
                        pecas_online = self.sistema.scraper.extrair_pecas_autopecas(nome_busca, 5)
                        
                        if pecas_online:
                            print(f"\n🎯 Encontradas {len(pecas_online)} peças online:")
                            for peca in pecas_online:
                                print(f"  • {peca.nome} - R$ {peca.preco:.2f} ({peca.fabricante})")
                                if hasattr(peca, 'montadora') and peca.montadora != "Não especificado":
                                    print(f"    🚗 Compatível: {peca.montadora} {peca.modelo_carro} ({peca.motor}) - {peca.anos_compativel}")
                                print()
                        else:
                            print("❌ Nenhuma peça encontrada online também")
                            
            except Exception as e:
                print(f"❌ Erro na busca: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def pecas_mais_caras(self):
        """Mostra as peças mais caras"""
        pecas_top = self.relatorios.pecas_mais_caras_por_categoria(3)
        
        if not pecas_top.empty:
            print("\n💎 PEÇAS MAIS CARAS POR CATEGORIA:")
            print("=" * 45)
            
            for categoria in pecas_top['categoria'].unique():
                print(f"\n📦 {categoria}:")
                categoria_pecas = pecas_top[pecas_top['categoria'] == categoria]
                
                for _, peca in categoria_pecas.iterrows():
                    print(f"  {peca['ranking']}º - {peca['peca_nome']}")
                    print(f"       R$ {peca['preco']:.2f} ({peca['fabricante']})")
        else:
            print("❌ Nenhuma peça com preço encontrada!")
        
        input("\nPressione Enter para continuar...")
    
    def pecas_mais_baratas(self):
        """Mostra as peças mais baratas"""
        try:
            conn = sqlite3.connect(self.sistema.db.db_name)
            
            query = '''
                SELECT 
                    c.nome as categoria,
                    p.nome as peca_nome,
                    p.preco,
                    p.fabricante,
                    ROW_NUMBER() OVER (PARTITION BY c.nome ORDER BY p.preco ASC) as ranking
                FROM pecas p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.preco > 0
            '''
            
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            conn.close()
            
            if resultados:
                # Organizar por categoria
                categorias = {}
                for resultado in resultados:
                    categoria, peca_nome, preco, fabricante, ranking = resultado
                    if ranking <= 3:  # Top 3 mais baratas por categoria
                        if categoria not in categorias:
                            categorias[categoria] = []
                        categorias[categoria].append((peca_nome, preco, fabricante, ranking))
                
                print("\n💰 TOP 3 PEÇAS MAIS BARATAS POR CATEGORIA:")
                print("=" * 50)
                
                for categoria, pecas in categorias.items():
                    print(f"\n📦 {categoria}:")
                    for peca_nome, preco, fabricante, ranking in pecas:
                        print(f"  {ranking}º - {peca_nome}: R$ {preco:.2f} ({fabricante})")
            else:
                print("❌ Nenhuma peça com preço encontrada!")
                
        except Exception as e:
            print(f"❌ Erro ao buscar peças: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        while True:
            print("\n📊 RELATÓRIOS E ANÁLISES")
            print("="*25)
            print("1. Estatísticas gerais")
            print("2. Relatório de estoque")
            print("3. Análise de preços")
            print("4. Clientes por marca")
            print("5. Gerar dashboard HTML")
            print("0. Voltar ao menu principal")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.mostrar_estatisticas()
            elif opcao == '2':
                self.relatorio_estoque()
            elif opcao == '3':
                self.analise_precos()
            elif opcao == '4':
                self.relatorio_clientes_marca()
            elif opcao == '5':
                self.gerar_dashboard()
            elif opcao == '0':
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas gerais"""
        stats = self.relatorios.estatisticas_gerais()
        
        print("\n📈 ESTATÍSTICAS GERAIS")
        print("=" * 22)
        print(f"🔧 Total de peças: {stats.get('total_pecas', 0)}")
        print(f"👥 Total de clientes: {stats.get('total_clientes', 0)}")
        print(f"📦 Categorias ativas: {stats.get('categorias_ativas', 0)}")
        print(f"💰 Preço médio: R$ {stats.get('preco_medio', 0):.2f}")
        
        if 'marca_mais_comum' in stats:
            print(f"🚗 Marca mais comum: {stats['marca_mais_comum']} ({stats['clientes_marca_comum']} clientes)")
        
        input("\nPressione Enter para continuar...")
    
    def relatorio_estoque(self):
        """Mostra relatório de estoque"""
        relatorio = self.sistema.relatorio_estoque()
        
        if not relatorio.empty:
            print("\n📊 RELATÓRIO DE ESTOQUE")
            print("=" * 25)
            
            for _, row in relatorio.iterrows():
                print(f"\n📦 {row['categoria']}:")
                print(f"   Quantidade: {row['quantidade_pecas']} peças")
                print(f"   Preço médio: R$ {row['preco_medio']:.2f}")
                print(f"   Faixa: R$ {row['menor_preco']:.2f} - R$ {row['maior_preco']:.2f}")
        else:
            print("❌ Nenhum dado de estoque disponível!")
        
        input("\nPressione Enter para continuar...")
    
    def analise_precos(self):
        """Análise de preços por categoria"""
        print("\n💰 Gerando análise de preços...")
        df_precos = self.relatorios.analise_precos_por_categoria()
        
        if not df_precos.empty:
            print("✅ Gráfico salvo como 'precos_por_categoria.png'")
            
            # Mostrar resumo estatístico
            resumo = df_precos.groupby('categoria')['preco'].agg(['count', 'mean', 'std', 'min', 'max'])
            print("\n📊 Resumo estatístico:")
            print(resumo.round(2))
        else:
            print("❌ Nenhum dado de preço disponível!")
        
        input("\nPressione Enter para continuar...")
    
    def relatorio_clientes_marca(self):
        """Relatório de clientes por marca"""
        relatorio = self.relatorios.relatorio_clientes_por_marca()
        
        if not relatorio.empty:
            print("\n🚗 CLIENTES POR MARCA DE CARRO")
            print("=" * 32)
            
            for _, row in relatorio.iterrows():
                print(f"\n• {row['marca_carro']}:")
                print(f"   Clientes: {row['total_clientes']}")
                print(f"   Ano médio: {row['ano_medio']:.0f}")
                print(f"   Faixa de anos: {row['ano_mais_antigo']} - {row['ano_mais_novo']}")
        else:
            print("❌ Nenhum cliente cadastrado!")
        
        input("\nPressione Enter para continuar...")
    
    def gerar_dashboard(self):
        """Gera dashboard HTML"""
        print("\n🎨 Gerando dashboard HTML...")
        
        try:
            self.relatorios.gerar_dashboard_html("dashboard.html")
            print("✅ Dashboard gerado com sucesso!")
            print("📁 Arquivo salvo como: dashboard.html")
            
            # Tentar abrir o arquivo
            abrir = input("\nDeseja abrir o dashboard no navegador? (s/n): ").lower()
            if abrir == 's':
                import webbrowser
                webbrowser.open("dashboard.html")
                
        except Exception as e:
            print(f"❌ Erro ao gerar dashboard: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def menu_importacao(self):
        """Menu de importação/exportação"""
        while True:
            print("\n📥 IMPORTAR/EXPORTAR DADOS")
            print("="*27)
            print("1. Criar templates CSV")
            print("2. Importar peças de CSV")
            print("3. Importar clientes de CSV")
            print("4. Exportar peças para CSV")
            print("5. Exportar clientes para CSV")
            print("0. Voltar ao menu principal")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.criar_templates()
            elif opcao == '2':
                self.importar_pecas()
            elif opcao == '3':
                self.importar_clientes()
            elif opcao == '4':
                self.exportar_pecas()
            elif opcao == '5':
                self.exportar_clientes()
            elif opcao == '0':
                break
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def criar_templates(self):
        """Cria templates CSV"""
        print("\n📄 Criando templates CSV...")
        self.importador.criar_templates_csv()
        input("\nPressione Enter para continuar...")
    
    def importar_pecas(self):
        """Importa peças de CSV"""
        arquivo = input("\n📁 Nome do arquivo CSV de peças: ").strip()
        
        if arquivo and os.path.exists(arquivo):
            print(f"📥 Importando peças de {arquivo}...")
            pecas_importadas = self.importador.importar_pecas_csv(arquivo)
            print(f"✅ {pecas_importadas} peças importadas com sucesso!")
        else:
            print("❌ Arquivo não encontrado!")
        
        input("\nPressione Enter para continuar...")
    
    def importar_clientes(self):
        """Importa clientes de CSV"""
        arquivo = input("\n📁 Nome do arquivo CSV de clientes: ").strip()
        
        if arquivo and os.path.exists(arquivo):
            print(f"📥 Importando clientes de {arquivo}...")
            clientes_importados = self.importador.importar_clientes_csv(arquivo)
            print(f"✅ {clientes_importados} clientes importados com sucesso!")
        else:
            print("❌ Arquivo não encontrado!")
        
        input("\nPressione Enter para continuar...")
    
    def exportar_pecas(self):
        """Exporta peças para CSV"""
        arquivo = input("\n📁 Nome do arquivo de saída (ex: pecas.csv): ").strip()
        if not arquivo:
            arquivo = "pecas_export.csv"
        
        print(f"📤 Exportando peças para {arquivo}...")
        total = self.importador.exportar_pecas_csv(arquivo)
        print(f"✅ {total} peças exportadas com sucesso!")
        
        input("\nPressione Enter para continuar...")
    
    def exportar_clientes(self):
        """Exporta clientes para CSV"""
        arquivo = input("\n📁 Nome do arquivo de saída (ex: clientes.csv): ").strip()
        if not arquivo:
            arquivo = "clientes_export.csv"
        
        print(f"📤 Exportando clientes para {arquivo}...")
        total = self.importador.exportar_clientes_csv(arquivo)
        print(f"✅ {total} clientes exportados com sucesso!")
        
        input("\nPressione Enter para continuar...")
    
    def menu_configuracoes(self):
        """Menu de configurações"""
        print("\n⚙️  CONFIGURAÇÕES")
        print("="*15)
        print("1. Verificar dependências")
        print("2. Limpar cache")
        print("3. Backup do banco de dados")
        print("4. Restaurar banco de dados")
        print("0. Voltar ao menu principal")
        
        opcao = input("\n➤ Escolha uma opção: ").strip()
        
        if opcao == '1':
            self.verificar_dependencias()
        elif opcao == '2':
            print("🧹 Limpando cache...")
            print("✅ Cache limpo!")
        elif opcao == '3':
            self.fazer_backup()
        elif opcao == '4':
            self.restaurar_backup()
        
        input("\nPressione Enter para continuar...")
    
    def verificar_dependencias(self):
        """Verifica se todas as dependências estão instaladas"""
        print("\n🔍 Verificando dependências...")
        
        dependencias = [
            'requests', 'beautifulsoup4', 'pandas', 'sqlite3',
            'matplotlib', 'seaborn', 'plotly'
        ]
        
        for dep in dependencias:
            try:
                __import__(dep)
                print(f"✅ {dep}")
            except ImportError:
                print(f"❌ {dep} - NÃO INSTALADO")
        
        input("\nPressione Enter para continuar...")
    
    def fazer_backup(self):
        """Faz backup do banco de dados"""
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_automotivas_{timestamp}.db"
        
        try:
            shutil.copy2("automotivas.db", backup_name)
            print(f"✅ Backup criado: {backup_name}")
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
        
        input("\nPressione Enter para continuar...")
    
    def restaurar_backup(self):
        """Restaura backup do banco de dados"""
        import glob
        
        # Listar backups disponíveis
        backups = glob.glob("backup_automotivas_*.db")
        
        if not backups:
            print("❌ Nenhum backup encontrado!")
            input("\nPressione Enter para continuar...")
            return
        
        print("\n📁 Backups disponíveis:")
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup}")
        
        try:
            escolha = int(input("\nEscolha o backup para restaurar (número): ").strip())
            
            if 1 <= escolha <= len(backups):
                backup_escolhido = backups[escolha - 1]
                
                # Confirmar restauração
                confirmacao = input(f"\n⚠️  Confirma restaurar '{backup_escolhido}'? (s/n): ").lower()
                
                if confirmacao == 's':
                    # Fazer backup do atual antes de restaurar
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_atual = f"backup_antes_restauracao_{timestamp}.db"
                    
                    shutil.copy2("automotivas.db", backup_atual)
                    print(f"🔄 Backup atual salvo como: {backup_atual}")
                    
                    # Restaurar o backup escolhido
                    shutil.copy2(backup_escolhido, "automotivas.db")
                    print(f"✅ Banco restaurado com sucesso!")
                    print("⚠️  Reinicie o sistema para aplicar as mudanças.")
                else:
                    print("❌ Restauração cancelada!")
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Digite um número válido!")
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
        
        input("\nPressione Enter para continuar...")

def main():
    """Função principal"""
    try:
        menu = MenuPrincipal()
        menu.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema finalizado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("Por favor, relate este erro ao desenvolvedor.")

if __name__ == "__main__":
    main()
