// ia-visual-radiadores.js - Sistema de IA para análise visual de radiadores

class RadiadorVisualAI {
    constructor() {
        this.catalogoZelukar = this.carregarCatalogoZelukar();
        this.padroesDimensoes = this.carregarPadroesDimensoes();
        this.caracteristicasVisuais = this.carregarCaracteristicasVisuais();
        this.modeloTreinado = this.inicializarModelo();
    }

    // Carregar catálogo Zelukar expandido
    carregarCatalogoZelukar() {
        return {
            volkswagen: {
                gol: {
                    g5_g6: {
                        superior: { 
                            codigo: 'VW-001', 
                            dimensoes: [480, 335, 26], 
                            fabricante: 'Valeo',
                            anos: '2008-2016',
                            motor: '1.0/1.6 8V Flex',
                            caracteristicas: ['plástico_preto', 'formato_retangular', 'dois_bocais', 'logo_valeo']
                        },
                        inferior: { 
                            codigo: 'VW-002', 
                            dimensoes: [480, 335, 26], 
                            fabricante: 'Valeo',
                            anos: '2008-2016',
                            motor: '1.0/1.6 8V Flex',
                            caracteristicas: ['plástico_preto', 'formato_retangular', 'um_bocal', 'dreno_inferior']
                        }
                    },
                    g7: {
                        superior: { 
                            codigo: 'VW-003', 
                            dimensoes: [490, 340, 28], 
                            fabricante: 'Valeo',
                            anos: '2016+',
                            motor: '1.0/1.6 MSI',
                            caracteristicas: ['plástico_cinza', 'formato_moderno', 'dois_bocais', 'sensor_temperatura']
                        }
                    },
                    fox: {
                        superior: { 
                            codigo: 'VW-010', 
                            dimensoes: [460, 320, 26], 
                            fabricante: 'Valeo',
                            caracteristicas: ['plástico_preto', 'formato_compacto', 'dois_bocais']
                        },
                        inferior: { 
                            codigo: 'VW-011', 
                            dimensoes: [460, 320, 26], 
                            fabricante: 'Valeo',
                            caracteristicas: ['plástico_preto', 'formato_compacto', 'um_bocal']
                        }
                    }
                }
            },
            chevrolet: {
                onix: {
                    primeira_geracao: {
                        superior: { 
                            codigo: 'GM-123', 
                            dimensoes: [485, 340, 26], 
                            fabricante: 'Behr',
                            anos: '2012-2019',
                            motor: '1.0/1.4 8V Flex',
                            caracteristicas: ['plástico_preto', 'formato_retangular', 'logo_behr', 'dois_bocais']
                        },
                        inferior: { 
                            codigo: 'GM-124', 
                            dimensoes: [485, 340, 26], 
                            fabricante: 'Behr',
                            caracteristicas: ['plástico_preto', 'formato_retangular', 'um_bocal', 'dreno_lateral']
                        }
                    },
                    plus: {
                        superior: { 
                            codigo: 'GM-130', 
                            dimensoes: [495, 345, 28], 
                            fabricante: 'Behr',
                            anos: '2019+',
                            caracteristicas: ['plástico_cinza', 'formato_moderno', 'sensor_integrado']
                        }
                    }
                },
                prisma: {
                    primeira_geracao: {
                        superior: { codigo: 'GM-140', dimensoes: [485, 340, 26], fabricante: 'Behr' },
                        inferior: { codigo: 'GM-141', dimensoes: [485, 340, 26], fabricante: 'Behr' }
                    }
                }
            },
            fiat: {
                uno: {
                    vivace: {
                        superior: { 
                            codigo: 'FI-010', 
                            dimensoes: [440, 315, 26], 
                            fabricante: 'Magneti Marelli',
                            caracteristicas: ['plástico_preto', 'formato_curvo', 'logo_magneti']
                        },
                        inferior: { 
                            codigo: 'FI-011', 
                            dimensoes: [440, 315, 26], 
                            fabricante: 'Magneti Marelli',
                            caracteristicas: ['plástico_preto', 'formato_curvo', 'dreno_central']
                        }
                    }
                },
                doblo: {
                    primeira_geracao: {
                        superior: { 
                            codigo: 'FI-001', 
                            dimensoes: [450, 325, 26], 
                            fabricante: 'Magneti Marelli',
                            caracteristicas: ['plástico_preto', 'formato_grande', 'tres_bocais']
                        },
                        inferior: { 
                            codigo: 'FI-002', 
                            dimensoes: [450, 325, 26], 
                            fabricante: 'Magneti Marelli'
                        }
                    }
                }
            },
            ford: {
                ka: {
                    segunda_geracao: {
                        superior: { 
                            codigo: 'FD-050', 
                            dimensoes: [450, 320, 26], 
                            fabricante: 'Denso',
                            caracteristicas: ['plástico_preto', 'formato_compacto', 'logo_denso']
                        },
                        inferior: { 
                            codigo: 'FD-051', 
                            dimensoes: [450, 320, 26], 
                            fabricante: 'Denso'
                        }
                    }
                }
            },
            toyota: {
                corolla: {
                    gli_xei: {
                        superior: { 
                            codigo: 'TO-100', 
                            dimensoes: [540, 380, 26], 
                            fabricante: 'Denso',
                            caracteristicas: ['plástico_preto', 'formato_grande', 'sensor_temperatura', 'logo_denso']
                        },
                        inferior: { 
                            codigo: 'TO-101', 
                            dimensoes: [540, 380, 26], 
                            fabricante: 'Denso'
                        }
                    }
                }
            },
            honda: {
                civic: {
                    decima_geracao: {
                        superior: { 
                            codigo: 'HO-200', 
                            dimensoes: [520, 365, 26], 
                            fabricante: 'Denso',
                            caracteristicas: ['plástico_preto', 'formato_moderno', 'sensor_integrado']
                        }
                    }
                }
            }
        };
    }

    // Carregar padrões de dimensões conhecidos
    carregarPadroesDimensoes() {
        return {
            compactos: { largura: [440, 480], altura: [315, 340], profundidade: [24, 28] },
            medios: { largura: [480, 520], altura: [335, 365], profundidade: [26, 30] },
            grandes: { largura: [520, 580], altura: [365, 400], profundidade: [28, 32] }
        };
    }

    // Carregar características visuais conhecidas
    carregarCaracteristicasVisuais() {
        return {
            fabricantes: {
                valeo: ['logo_v', 'plástico_preto_brilhante', 'acabamento_liso'],
                behr: ['logo_b', 'plástico_texturizado', 'nervuras_laterais'],
                magneti_marelli: ['logo_mm', 'plástico_fosco', 'formato_curvo'],
                denso: ['logo_denso', 'plástico_cinza', 'sensor_integrado'],
                mobis: ['logo_mobis', 'plástico_preto', 'formato_angular'],
                calsonic: ['logo_calsonic', 'plástico_brilhante', 'bocais_cromados']
            },
            tipos: {
                superior: ['bocais_multiplos', 'tampa_expansao', 'sensor_temperatura'],
                inferior: ['bocal_unico', 'dreno_agua', 'sem_sensores'],
                completo: ['radiador_acoplado', 'ventoinhas', 'reservatorio']
            },
            materiais: {
                plastico: ['superficie_lisa', 'reflexo_baixo', 'cor_uniforme'],
                aluminio: ['superficie_metalica', 'reflexo_alto', 'cor_prateada'],
                metal: ['superficie_rugosa', 'oxidacao_possivel', 'peso_elevado']
            }
        };
    }

    // Inicializar modelo de IA (simulado)
    inicializarModelo() {
        return {
            versao: '2.1.0',
            precisao: 0.89,
            treinamento: '2024-07-15',
            datasets: ['zelukar', 'autopeças_br', 'radiadores_oem']
        };
    }

    // Analisar imagem (função principal)
    async analisarImagem(imagemFile) {
        try {
            // Simular processamento de IA
            const analiseBasica = await this.extrairCaracteristicasBasicas(imagemFile);
            const dimensoesDetectadas = await this.detectarDimensoes(imagemFile);
            const caracteristicasVisuais = await this.identificarCaracteristicasVisuais(imagemFile);
            const fabricanteDetectado = await this.identificarFabricante(imagemFile);
            
            // Buscar correspondências
            const correspondencias = this.buscarCorrespondencias(
                dimensoesDetectadas, 
                caracteristicasVisuais, 
                fabricanteDetectado
            );

            return {
                dimensoes: dimensoesDetectadas,
                caracteristicas: caracteristicasVisuais,
                fabricante: fabricanteDetectado,
                correspondencias: correspondencias,
                confianca: this.calcularConfiancaGeral(correspondencias),
                metadata: {
                    tempo_processamento: '2.3s',
                    modelo_usado: this.modeloTreinado.versao,
                    timestamp: new Date().toISOString()
                }
            };

        } catch (error) {
            throw new Error(`Erro na análise da imagem: ${error.message}`);
        }
    }

    // Extrair características básicas
    async extrairCaracteristicasBasicas(imagemFile) {
        return new Promise(resolve => {
            setTimeout(() => {
                // Simular análise de IA
                resolve({
                    formato: 'retangular',
                    orientacao: 'horizontal',
                    cor_dominante: 'preto',
                    textura: 'lisa',
                    bordas_detectadas: true,
                    qualidade_imagem: 0.85
                });
            }, 800);
        });
    }

    // Detectar dimensões
    async detectarDimensoes(imagemFile) {
        return new Promise(resolve => {
            setTimeout(() => {
                // Simular detecção de dimensões com variação realista
                const baseWidth = 480 + (Math.random() * 20 - 10);
                const baseHeight = 335 + (Math.random() * 15 - 7.5);
                const baseDepth = 26 + (Math.random() * 4 - 2);
                
                resolve({
                    largura: Math.round(baseWidth * 10) / 10,
                    altura: Math.round(baseHeight * 10) / 10,
                    profundidade: Math.round(baseDepth * 10) / 10,
                    unidade: 'mm',
                    metodo: 'ai_vision',
                    confianca: 0.82 + Math.random() * 0.15
                });
            }, 1200);
        });
    }

    // Identificar características visuais
    async identificarCaracteristicasVisuais(imagemFile) {
        return new Promise(resolve => {
            setTimeout(() => {
                const caracteristicas = [
                    'plástico_preto',
                    'formato_retangular',
                    'dois_bocais',
                    'superficie_lisa'
                ];
                
                // Adicionar características aleatórias baseadas em probabilidade
                if (Math.random() > 0.6) caracteristicas.push('logo_visivel');
                if (Math.random() > 0.7) caracteristicas.push('sensor_temperatura');
                if (Math.random() > 0.8) caracteristicas.push('acabamento_texturizado');
                
                resolve({
                    detectadas: caracteristicas,
                    confianca_media: 0.75 + Math.random() * 0.2,
                    detalhes: {
                        material: 'plástico',
                        cor: 'preto/cinza',
                        acabamento: 'liso',
                        bocais: 2,
                        sensores: Math.random() > 0.5 ? 1 : 0
                    }
                });
            }, 1000);
        });
    }

    // Identificar fabricante
    async identificarFabricante(imagemFile) {
        return new Promise(resolve => {
            setTimeout(() => {
                const fabricantes = ['Valeo', 'Behr', 'Magneti Marelli', 'Denso', 'Mobis'];
                const fabricanteDetectado = fabricantes[Math.floor(Math.random() * fabricantes.length)];
                
                resolve({
                    nome: fabricanteDetectado,
                    confianca: 0.6 + Math.random() * 0.3,
                    metodo: Math.random() > 0.5 ? 'logo_detection' : 'style_analysis',
                    alternativas: fabricantes.filter(f => f !== fabricanteDetectado).slice(0, 2)
                });
            }, 900);
        });
    }

    // Buscar correspondências no catálogo
    buscarCorrespondencias(dimensoes, caracteristicas, fabricante) {
        const correspondencias = [];
        
        // Percorrer catálogo
        Object.keys(this.catalogoZelukar).forEach(montadora => {
            Object.keys(this.catalogoZelukar[montadora]).forEach(modelo => {
                Object.keys(this.catalogoZelukar[montadora][modelo]).forEach(variante => {
                    Object.keys(this.catalogoZelukar[montadora][modelo][variante]).forEach(tipo => {
                        const item = this.catalogoZelukar[montadora][modelo][variante][tipo];
                        
                        // Calcular score de similaridade
                        const scoreDimensao = this.calcularScoreDimensao(dimensoes, item.dimensoes);
                        const scoreFabricante = this.calcularScoreFabricante(fabricante, item.fabricante);
                        const scoreCaracteristicas = this.calcularScoreCaracteristicas(caracteristicas, item.caracteristicas || []);
                        
                        const scoreGeral = (scoreDimensao * 0.5) + (scoreFabricante * 0.3) + (scoreCaracteristicas * 0.2);
                        
                        if (scoreGeral > 0.5) {
                            correspondencias.push({
                                montadora,
                                modelo,
                                variante,
                                tipo,
                                codigo: item.codigo,
                                fabricante: item.fabricante,
                                dimensoes: item.dimensoes,
                                anos: item.anos || 'Consultar',
                                motor: item.motor || 'Não especificado',
                                score: scoreGeral,
                                detalhes_score: {
                                    dimensao: scoreDimensao,
                                    fabricante: scoreFabricante,
                                    caracteristicas: scoreCaracteristicas
                                }
                            });
                        }
                    });
                });
            });
        });
        
        // Ordenar por score e retornar top 5
        return correspondencias
            .sort((a, b) => b.score - a.score)
            .slice(0, 5);
    }

    // Calcular score de dimensão
    calcularScoreDimensao(dimensoesDetectadas, dimensoesReferencia) {
        const d1 = [dimensoesDetectadas.largura, dimensoesDetectadas.altura, dimensoesDetectadas.profundidade];
        const d2 = dimensoesReferencia;
        
        let somaErros = 0;
        for (let i = 0; i < 3; i++) {
            const erro = Math.abs(d1[i] - d2[i]) / d2[i];
            somaErros += erro;
        }
        
        const erroMedio = somaErros / 3;
        return Math.max(0, 1 - erroMedio);
    }

    // Calcular score de fabricante
    calcularScoreFabricante(fabricanteDetectado, fabricanteReferencia) {
        if (!fabricanteDetectado.nome || !fabricanteReferencia) return 0.5;
        
        const nomeDetectado = fabricanteDetectado.nome.toLowerCase();
        const nomeReferencia = fabricanteReferencia.toLowerCase();
        
        if (nomeDetectado === nomeReferencia) {
            return fabricanteDetectado.confianca;
        } else if (fabricanteDetectado.alternativas && 
                   fabricanteDetectado.alternativas.some(alt => alt.toLowerCase() === nomeReferencia)) {
            return fabricanteDetectado.confianca * 0.7;
        }
        
        return 0.3;
    }

    // Calcular score de características
    calcularScoreCaracteristicas(caracteristicasDetectadas, caracteristicasReferencia) {
        if (!caracteristicasReferencia || caracteristicasReferencia.length === 0) return 0.5;
        
        const detectadas = caracteristicasDetectadas.detectadas || [];
        let matches = 0;
        
        caracteristicasReferencia.forEach(ref => {
            if (detectadas.includes(ref)) {
                matches++;
            }
        });
        
        return matches / Math.max(caracteristicasReferencia.length, 1);
    }

    // Calcular confiança geral
    calcularConfiancaGeral(correspondencias) {
        if (correspondencias.length === 0) return 0;
        
        const melhorScore = correspondencias[0].score;
        const confiancaBase = melhorScore;
        
        // Ajustar baseado no número de correspondências
        let ajuste = 1;
        if (correspondencias.length === 1) ajuste = 0.9; // Menos confiança se só uma opção
        if (correspondencias.length >= 3) ajuste = 1.1; // Mais confiança se várias opções
        
        return Math.min(1, confiancaBase * ajuste);
    }

    // Gerar relatório detalhado
    gerarRelatorioDetalhado(resultadoAnalise) {
        return {
            resumo: {
                dimensoes: `${resultadoAnalise.dimensoes.largura}x${resultadoAnalise.dimensoes.altura}x${resultadoAnalise.dimensoes.profundidade}mm`,
                fabricante_provavel: resultadoAnalise.fabricante.nome,
                melhor_correspondencia: resultadoAnalise.correspondencias[0] || null,
                confianca_geral: Math.round(resultadoAnalise.confianca * 100) + '%'
            },
            detalhes_tecnicos: {
                modelo_ia: resultadoAnalise.metadata.modelo_usado,
                tempo_processamento: resultadoAnalise.metadata.tempo_processamento,
                qualidade_analise: this.avaliarQualidadeAnalise(resultadoAnalise)
            },
            recomendacoes: this.gerarRecomendacoes(resultadoAnalise)
        };
    }

    // Avaliar qualidade da análise
    avaliarQualidadeAnalise(resultado) {
        let pontuacao = 0;
        
        // Qualidade das dimensões
        if (resultado.dimensoes.confianca > 0.8) pontuacao += 25;
        else if (resultado.dimensoes.confianca > 0.6) pontuacao += 15;
        else pontuacao += 5;
        
        // Qualidade do fabricante
        if (resultado.fabricante.confianca > 0.8) pontuacao += 25;
        else if (resultado.fabricante.confianca > 0.6) pontuacao += 15;
        else pontuacao += 5;
        
        // Número de correspondências
        if (resultado.correspondencias.length >= 3) pontuacao += 25;
        else if (resultado.correspondencias.length >= 1) pontuacao += 15;
        else pontuacao += 0;
        
        // Confiança geral
        if (resultado.confianca > 0.8) pontuacao += 25;
        else if (resultado.confianca > 0.6) pontuacao += 15;
        else pontuacao += 5;
        
        if (pontuacao >= 80) return 'Excelente';
        if (pontuacao >= 60) return 'Boa';
        if (pontuacao >= 40) return 'Regular';
        return 'Baixa';
    }

    // Gerar recomendações
    gerarRecomendacoes(resultado) {
        const recomendacoes = [];
        
        if (resultado.confianca < 0.7) {
            recomendacoes.push('Considere tirar nova foto com melhor iluminação');
        }
        
        if (resultado.fabricante.confianca < 0.6) {
            recomendacoes.push('Verifique se há logos ou etiquetas visíveis na peça');
        }
        
        if (resultado.correspondencias.length === 0) {
            recomendacoes.push('Nenhuma correspondência encontrada - pode ser modelo não catalogado');
        }
        
        if (resultado.dimensoes.confianca < 0.7) {
            recomendacoes.push('Confirme as dimensões manualmente para maior precisão');
        }
        
        return recomendacoes;
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.RadiadorVisualAI = RadiadorVisualAI;
}

// Para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RadiadorVisualAI;
}
