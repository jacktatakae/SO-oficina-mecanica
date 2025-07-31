import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class RelatoriosAvancados:
    def __init__(self, db_name="automotivas.db"):
        self.db_name = db_name
    
    def analise_precos_por_categoria(self):
        """Análise de preços por categoria"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT 
                c.nome as categoria,
                p.preco,
                p.fabricante,
                p.nome as peca_nome
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.preco > 0
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Criar gráfico
        if not df.empty:
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=df, x='categoria', y='preco')
            plt.xticks(rotation=45)
            plt.title('Distribuição de Preços por Categoria')
            plt.tight_layout()
            plt.savefig('precos_por_categoria.png')
            plt.show()
        
        return df
    
    def relatorio_clientes_por_marca(self):
        """Relatório de clientes agrupados por marca de carro"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT 
                marca_carro,
                COUNT(*) as total_clientes,
                AVG(ano_carro) as ano_medio,
                MIN(ano_carro) as ano_mais_antigo,
                MAX(ano_carro) as ano_mais_novo
            FROM clientes
            GROUP BY marca_carro
            ORDER BY total_clientes DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def pecas_mais_caras_por_categoria(self, top_n=5):
        """Lista as peças mais caras de cada categoria"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT 
                c.nome as categoria,
                p.nome as peca_nome,
                p.preco,
                p.fabricante,
                ROW_NUMBER() OVER (PARTITION BY c.nome ORDER BY p.preco DESC) as ranking
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.preco > 0
        '''
        
        df = pd.read_sql_query(query, conn)
        df_top = df[df['ranking'] <= top_n]
        conn.close()
        
        return df_top
    
    def estatisticas_gerais(self):
        """Estatísticas gerais do sistema"""
        conn = sqlite3.connect(self.db_name)
        
        stats = {}
        
        # Total de peças
        stats['total_pecas'] = pd.read_sql_query(
            'SELECT COUNT(*) as count FROM pecas', conn
        ).iloc[0]['count']
        
        # Total de clientes
        stats['total_clientes'] = pd.read_sql_query(
            'SELECT COUNT(*) as count FROM clientes', conn
        ).iloc[0]['count']
        
        # Total de categorias com peças
        stats['categorias_ativas'] = pd.read_sql_query(
            'SELECT COUNT(DISTINCT categoria_id) as count FROM pecas WHERE categoria_id IS NOT NULL', conn
        ).iloc[0]['count']
        
        # Preço médio das peças
        preco_medio = pd.read_sql_query(
            'SELECT AVG(preco) as media FROM pecas WHERE preco > 0', conn
        ).iloc[0]['media']
        stats['preco_medio'] = round(preco_medio, 2) if preco_medio else 0
        
        # Marca mais comum entre clientes
        marca_comum = pd.read_sql_query(
            'SELECT marca_carro, COUNT(*) as count FROM clientes GROUP BY marca_carro ORDER BY count DESC LIMIT 1', conn
        )
        if not marca_comum.empty:
            stats['marca_mais_comum'] = marca_comum.iloc[0]['marca_carro']
            stats['clientes_marca_comum'] = marca_comum.iloc[0]['count']
        
        conn.close()
        return stats
    
    def gerar_dashboard_html(self, arquivo_saida="dashboard.html"):
        """Gera um dashboard HTML interativo"""
        conn = sqlite3.connect(self.db_name)
        
        # Dados para gráficos
        df_precos = pd.read_sql_query('''
            SELECT c.nome as categoria, p.preco
            FROM pecas p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.preco > 0
        ''', conn)
        
        df_clientes = pd.read_sql_query('''
            SELECT marca_carro, COUNT(*) as total
            FROM clientes
            GROUP BY marca_carro
            ORDER BY total DESC
        ''', conn)
        
        conn.close()
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Preços por Categoria', 'Clientes por Marca', 
                          'Distribuição de Preços', 'Top Categorias'),
            specs=[[{"secondary_y": False}, {"type": "pie"}],
                   [{"colspan": 2}, None]],
            vertical_spacing=0.12
        )
        
        if not df_precos.empty:
            # Box plot de preços
            for categoria in df_precos['categoria'].unique():
                data = df_precos[df_precos['categoria'] == categoria]['preco']
                fig.add_trace(
                    go.Box(y=data, name=categoria),
                    row=1, col=1
                )
        
        if not df_clientes.empty:
            # Gráfico de pizza - clientes por marca
            fig.add_trace(
                go.Pie(labels=df_clientes['marca_carro'], 
                      values=df_clientes['total'],
                      name="Clientes"),
                row=1, col=2
            )
            
            # Histograma de preços
            fig.add_trace(
                go.Histogram(x=df_precos['preco'], 
                           name="Distribuição de Preços",
                           nbinsx=20),
                row=2, col=1
            )
        
        fig.update_layout(
            title_text="Dashboard - Sistema Automotivo",
            showlegend=False,
            height=800
        )
        
        fig.write_html(arquivo_saida)
        print(f"Dashboard salvo em: {arquivo_saida}")

def exemplo_uso_relatorios():
    """Exemplo de uso dos relatórios"""
    relatorios = RelatoriosAvancados()
    
    print("📊 RELATÓRIOS AVANÇADOS - SISTEMA AUTOMOTIVO")
    print("="*50)
    
    # Estatísticas gerais
    print("\n📈 Estatísticas Gerais:")
    stats = relatorios.estatisticas_gerais()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Análise de preços
    print("\n💰 Análise de Preços por Categoria:")
    df_precos = relatorios.analise_precos_por_categoria()
    if not df_precos.empty:
        resumo_precos = df_precos.groupby('categoria')['preco'].agg(['count', 'mean', 'min', 'max'])
        print(resumo_precos.round(2))
    
    # Relatório de clientes
    print("\n🚗 Clientes por Marca de Carro:")
    df_clientes_marca = relatorios.relatorio_clientes_por_marca()
    print(df_clientes_marca)
    
    # Peças mais caras
    print("\n💎 Top 3 Peças Mais Caras por Categoria:")
    df_top_pecas = relatorios.pecas_mais_caras_por_categoria(3)
    for categoria in df_top_pecas['categoria'].unique():
        print(f"\n  {categoria}:")
        categoria_data = df_top_pecas[df_top_pecas['categoria'] == categoria]
        for _, row in categoria_data.iterrows():
            print(f"    {row['ranking']}º - {row['peca_nome']}: R$ {row['preco']:.2f} ({row['fabricante']})")
    
    # Gerar dashboard
    print("\n🎨 Gerando dashboard HTML...")
    relatorios.gerar_dashboard_html()

if __name__ == "__main__":
    exemplo_uso_relatorios()
