#!/usr/bin/env python3
"""
Script para verificar e instalar dependências do Sistema Automotivo
"""

import sys
import subprocess
import os

def verificar_python():
    """Verifica a versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} detectado.")
        print("⚠️  É necessário Python 3.7 ou superior.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def instalar_pacote(pacote):
    """Instala um pacote Python"""
    try:
        print(f"📦 Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        print(f"✅ {pacote} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {pacote}: {e}")
        return False

def verificar_dependencias():
    """Verifica e instala as dependências necessárias"""
    dependencias = [
        'requests',
        'beautifulsoup4', 
        'pandas',
        'lxml',
        'selenium',
        'webdriver-manager',
        'sqlalchemy',
        'python-dotenv',
        'matplotlib',
        'seaborn',
        'plotly'
    ]
    
    print("🔍 Verificando dependências...")
    
    instaladas = []
    nao_instaladas = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
            instaladas.append(dep)
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")
            nao_instaladas.append(dep)
    
    if nao_instaladas:
        print(f"\n📋 Dependências faltando: {len(nao_instaladas)}")
        resposta = input("\nDeseja instalar as dependências faltando? (s/n): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            print("\n📦 Iniciando instalação...")
            
            # Atualizar pip primeiro
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                print("✅ pip atualizado!")
            except:
                print("⚠️  Aviso: Não foi possível atualizar o pip")
            
            # Instalar dependências
            sucesso = 0
            for dep in nao_instaladas:
                if instalar_pacote(dep):
                    sucesso += 1
            
            print(f"\n📊 Resultado: {sucesso}/{len(nao_instaladas)} pacotes instalados")
            
            if sucesso == len(nao_instaladas):
                print("🎉 Todas as dependências foram instaladas com sucesso!")
                return True
            else:
                print("⚠️  Algumas dependências falharam na instalação.")
                return False
        else:
            print("⚠️  Instalação cancelada pelo usuário.")
            return False
    else:
        print("\n🎉 Todas as dependências estão instaladas!")
        return True

def verificar_arquivos():
    """Verifica se os arquivos principais existem"""
    arquivos_necessarios = [
        'main.py',
        'sistema_automotivo.py', 
        'relatorios.py',
        'importador.py'
    ]
    
    print("\n📁 Verificando arquivos do sistema...")
    
    todos_existem = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - ARQUIVO FALTANDO")
            todos_existem = False
    
    return todos_existem

def criar_banco_inicial():
    """Cria o banco de dados inicial"""
    try:
        print("\n🗄️  Inicializando banco de dados...")
        from sistema_automotivo import DatabaseManager
        
        db = DatabaseManager()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def main():
    """Função principal de verificação"""
    print("🔧 VERIFICADOR DE SISTEMA - PEÇAS AUTOMOTIVAS")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        return False
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Alguns arquivos estão faltando!")
        print("Certifique-se de que todos os arquivos do sistema estão presentes.")
        return False
    
    # Verificar e instalar dependências
    if not verificar_dependencias():
        return False
    
    # Criar banco inicial
    if not criar_banco_inicial():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 SISTEMA VERIFICADO E PRONTO PARA USO!")
    print("=" * 50)
    print("\nPara executar o sistema:")
    print("  python main.py")
    print("\nPara mais informações, consulte o README.md")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = main()
        if not sucesso:
            input("\n❌ Verificação falhou. Pressione Enter para sair...")
            sys.exit(1)
        else:
            input("\n✅ Verificação concluída. Pressione Enter para continuar...")
    except KeyboardInterrupt:
        print("\n\n👋 Verificação interrompida pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)
