// catalogo-manager.js - Sistema de Gerenciamento de Catálogos
class CatalogoManager {
    constructor() {
        this.catalogos = new Map();
        this.pecas = new Map();
        this.initializeCatalogos();
    }

    // Inicializar catálogos conhecidos
    initializeCatalogos() {
        // Catálogo Zelukar - Radiadores
        this.addCatalogo('ZELUKAR', {
            nome: 'Zelukar Radiadores',
            prefixos: ['FI-', 'VW-', 'GM-', 'FD-', 'HY-', 'TO-'],
            categoria: 'Radiadores e Sistema de Arrefecimento',
            formato: {
                codigo: /^(FI|VW|GM|FD|HY|TO)-\d{3,4}$/i,
                descricao: 'Código do fabricante seguido de hífen e número (ex: FI-001)'
            },
            url: 'https://www.zelukar.com.br/e-catalogo/',
            urlPdf: 'https://zelukar.com.br/catalogo/catalogo-zelukar.pdf',
            contato: '(11) 2359-6457',
            whatsapp: '5511981150782',
            email: 'contato@zelukar.com.br',
            endereco: 'Rua Dona Vitória Speers, 1022 | Vila Formosa São Paulo-SP',
            tipoIntegracao: 'manual', // visual, manual, api
            observacoes: 'Catálogo eletrônico visual - consulta manual necessária'
        });

        // Catálogo Cofap - Filtros
        this.addCatalogo('COFAP', {
            nome: 'Cofap Filtros',
            prefixos: ['CF-', 'C'],
            categoria: 'Filtros Automotivos',
            formato: {
                codigo: /^(CF-\d{4}|C\d{3,5})$/i,
                descricao: 'CF- seguido de 4 dígitos ou C seguido de 3-5 dígitos'
            },
            url: 'https://cofap.com.br',
            contato: '(11) 2345-6789'
        });

        // Catálogo Bosch
        this.addCatalogo('BOSCH', {
            nome: 'Robert Bosch',
            prefixos: ['B', 'F', '0'],
            categoria: 'Peças Elétricas e Eletrônicas',
            formato: {
                codigo: /^(B\d{3,4}|F\d{6}|0\d{9})$/i,
                descricao: 'B + 3-4 dígitos, F + 6 dígitos ou 0 + 9 dígitos'
            },
            url: 'https://bosch.com.br',
            contato: '(11) 1234-5678'
        });

        // Catálogo Delphi
        this.addCatalogo('DELPHI', {
            nome: 'Delphi Technologies',
            prefixos: ['D', 'DG', 'AF'],
            categoria: 'Sistema de Combustível e Ignição',
            formato: {
                codigo: /^(D\d{3,4}|DG\d{6}|AF\d{4})$/i,
                descricao: 'D + 3-4 dígitos, DG + 6 dígitos ou AF + 4 dígitos'
            },
            url: 'https://delphi.com',
            contato: '(11) 9876-5432'
        });

        // Catálogo Mahle
        this.addCatalogo('MAHLE', {
            nome: 'Mahle Metal Leve',
            prefixos: ['M', 'ML', 'KC'],
            categoria: 'Componentes do Motor',
            formato: {
                codigo: /^(M\d{3,4}|ML\d{4}|KC\d{3})$/i,
                descricao: 'M + 3-4 dígitos, ML + 4 dígitos ou KC + 3 dígitos'
            },
            url: 'https://mahle.com',
            contato: '(11) 5432-1098'
        });
    }

    // Adicionar catálogo
    addCatalogo(id, catalogoData) {
        this.catalogos.set(id, catalogoData);
    }

    // Identificar catálogo pelo código
    identificarCatalogo(codigo) {
        const codigoUpper = codigo.toUpperCase();
        
        for (const [id, catalogo] of this.catalogos) {
            // Verificar por prefixo
            for (const prefixo of catalogo.prefixos) {
                if (codigoUpper.startsWith(prefixo)) {
                    return {
                        id,
                        catalogo,
                        confianca: 'alta'
                    };
                }
            }
            
            // Verificar por regex
            if (catalogo.formato.codigo.test(codigo)) {
                return {
                    id,
                    catalogo,
                    confianca: 'media'
                };
            }
        }
        
        return null;
    }

    // Buscar peça por código
    buscarPeca(codigo) {
        const resultado = this.identificarCatalogo(codigo);
        
        if (!resultado) {
            return {
                encontrada: false,
                erro: 'Formato de código não reconhecido',
                sugestoes: this.gerarSugestoes(codigo)
            };
        }

        // Simular busca na base de dados
        const peca = this.buscarNaBaseDados(codigo);
        
        if (peca) {
            return {
                encontrada: true,
                peca: {
                    ...peca,
                    catalogo: resultado.catalogo,
                    confianca: resultado.confianca
                }
            };
        }

        return {
            encontrada: false,
            catalogoIdentificado: resultado.catalogo,
            erro: 'Peça não encontrada na base local',
            acoes: [
                'Consultar catálogo online',
                'Solicitar importação automática',
                'Adicionar manualmente'
            ]
        };
    }

    // Buscar na base de dados local
    buscarNaBaseDados(codigo) {
        // Base de dados exemplo (integrar com o sistema principal)
        const baseDados = {
            'FI-001': {
                codigo: 'FI-001',
                nome: 'Caixa Superior Radiador Doblô',
                fabricante: 'Zelukar',
                categoria: 'Radiadores',
                preco: 450.00,
                estoque: 5,
                aplicacoes: ['Fiat Doblô 1.3', 'Fiat Doblô 1.4', 'Fiat Doblô 1.6'],
                descricao: 'Caixa superior do radiador para Fiat Doblô',
                peso: '1.2kg',
                garantia: '12 meses'
            },
            'CF-1234': {
                codigo: 'CF-1234',
                nome: 'Filtro de Óleo Motor',
                fabricante: 'Cofap',
                categoria: 'Filtros',
                preco: 25.90,
                estoque: 15,
                aplicacoes: ['VW Gol 1.0', 'VW Fox 1.0', 'Fiat Uno 1.0'],
                descricao: 'Filtro de óleo para motores 1.0 Flex',
                peso: '0.3kg',
                garantia: '6 meses'
            }
            // Adicionar mais peças conforme necessário
        };

        return baseDados[codigo.toUpperCase()];
    }

    // Gerar sugestões baseadas no código
    gerarSugestoes(codigo) {
        const sugestoes = [];
        
        // Sugestões baseadas em padrões conhecidos
        if (codigo.length >= 2) {
            const inicio = codigo.substring(0, 2).toUpperCase();
            
            for (const [id, catalogo] of this.catalogos) {
                for (const prefixo of catalogo.prefixos) {
                    if (prefixo.startsWith(inicio) || inicio.startsWith(prefixo)) {
                        sugestoes.push({
                            catalogo: catalogo.nome,
                            formato: catalogo.formato.descricao,
                            exemplo: this.gerarExemplo(prefixo)
                        });
                    }
                }
            }
        }
        
        return sugestoes;
    }

    // Gerar exemplo de código
    gerarExemplo(prefixo) {
        const exemplos = {
            'FI-': 'FI-001',
            'VW-': 'VW-123',
            'CF-': 'CF-1234',
            'B': 'B456',
            'D': 'D789',
            'M': 'M321'
        };
        
        return exemplos[prefixo] || prefixo + '123';
    }

    // Importar do catálogo online (simulado)
    async importarDoCatalogo(codigo, catalogoId) {
        return new Promise((resolve) => {
            const catalogo = this.catalogos.get(catalogoId);
            
            // Verificar tipo de integração
            if (catalogo.tipoIntegracao === 'manual') {
                resolve({
                    sucesso: false,
                    erro: 'Catálogo visual - importação manual necessária',
                    acaoSugerida: 'consultar_manual',
                    dadosCatalogo: {
                        url: catalogo.url,
                        urlPdf: catalogo.urlPdf,
                        whatsapp: catalogo.whatsapp,
                        telefone: catalogo.contato,
                        email: catalogo.email
                    }
                });
                return;
            }
            
            // Simular delay de importação para APIs futuras
            setTimeout(() => {
                // Dados simulados de importação
                const pecaImportada = {
                    codigo: codigo,
                    nome: `Peça Importada ${codigo}`,
                    fabricante: catalogo.nome,
                    categoria: catalogo.categoria,
                    preco: Math.random() * 500 + 50,
                    estoque: Math.floor(Math.random() * 20),
                    importadoEm: new Date().toISOString(),
                    fonte: 'Catálogo Online'
                };
                
                resolve({
                    sucesso: true,
                    peca: pecaImportada,
                    mensagem: 'Peça importada com sucesso do catálogo online'
                });
            }, 2000);
        });
    }

    // Listar todos os catálogos
    listarCatalogos() {
        return Array.from(this.catalogos.entries()).map(([id, catalogo]) => ({
            id,
            ...catalogo
        }));
    }

    // Estatísticas dos catálogos
    getEstatisticas() {
        return {
            totalCatalogos: this.catalogos.size,
            catalogos: this.listarCatalogos().map(cat => ({
                nome: cat.nome,
                prefixos: cat.prefixos.length,
                categoria: cat.categoria
            }))
        };
    }

    // Validar formato de código
    validarCodigo(codigo) {
        if (!codigo || codigo.trim().length === 0) {
            return {
                valido: false,
                erro: 'Código não pode estar vazio'
            };
        }

        const resultado = this.identificarCatalogo(codigo);
        
        if (!resultado) {
            return {
                valido: false,
                erro: 'Formato de código não reconhecido',
                sugestoes: this.gerarSugestoes(codigo)
            };
        }

        return {
            valido: true,
            catalogo: resultado.catalogo.nome,
            formato: resultado.catalogo.formato.descricao
        };
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.CatalogoManager = CatalogoManager;
} else {
    module.exports = CatalogoManager;
}
