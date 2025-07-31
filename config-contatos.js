// config-contatos.js - Configurações de Contato da Oficina VRS
const CONFIG_CONTATOS = {
    // Informações principais da oficina VRS
    oficina: {
        nome: 'Oficina VRS',
        nomeCompleto: 'VRS - Radiadores e Peças Automotivas',
        slogan: 'Radiadores e Peças Automotivas',
        endereco: 'São Paulo - SP'
    },

    // Contatos da OFICINA VRS (atualizados)
    contatos: {
        whatsapp: {
            numero: '5511971960699', // Formato internacional
            numeroFormatado: '(11) 97196-0699', // Formato brasileiro
            link: 'https://wa.me/5511971960699'
        },
        email: {
            principal: 'samusan18@gmail.com',
            suporte: 'samusan18@gmail.com'
        },
        telefone: {
            principal: '(11) 97196-0699'
        }
    },

    // Contatos dos FORNECEDORES (mantidos originais)
    fornecedores: {
        zelukar: {
            contato: '(11) 2359-6457',
            whatsapp: '5511981150782',
            email: 'contato@zelukar.com.br'
        },
        cofap: {
            contato: '(11) 2345-6789',
            email: 'cofap@cofap.com.br'
        },
        bosch: {
            contato: '(11) 1234-5678',
            email: 'bosch@bosch.com.br'
        }
    },

    // Mensagens padrão para WhatsApp
    mensagens: {
        cadastroCliente: (url) => `🚗 *Cadastro de Cliente - Oficina VRS*

Olá! Para se cadastrar como cliente da nossa oficina, acesse o link abaixo:

${url}

Ou escaneie o QR Code que foi apresentado.

✅ Cadastro rápido e seguro
📱 Otimizado para celular
🔧 Especialistas em radiadores

Qualquer dúvida, entre em contato!`,

        consultaPeca: (codigo) => `🔧 *Consulta de Peça - Oficina VRS*

Olá! Gostaria de consultar informações sobre o código: *${codigo}*

Podem me ajudar com:
- Disponibilidade
- Preço
- Compatibilidade
- Prazo de entrega

Obrigado!`,

        suporte: () => `🔧 *Suporte Técnico - Oficina VRS*

Olá! Preciso de ajuda com o sistema.

Aguardo retorno.

Obrigado!`
    },

    // URLs do sistema
    urls: {
        github: 'https://jacktatakae.github.io/SO-oficina-mecanica',
        cadastro: 'https://jacktatakae.github.io/SO-oficina-mecanica/cadastro-cliente.html',
        encurtado: 'https://qrco.de/bgBsmb'
    },

    // Configurações de notificação
    notificacoes: {
        novoCadastro: {
            ativo: true,
            whatsapp: '5511971960699',
            email: 'samusan18@gmail.com'
        }
    }
};

// Funções auxiliares
const ContatosHelper = {
    // Gerar link do WhatsApp com mensagem
    gerarLinkWhatsApp: function(tipo, dados = {}) {
        const numero = CONFIG_CONTATOS.contatos.whatsapp.numero;
        let mensagem = '';

        switch(tipo) {
            case 'cadastro':
                mensagem = CONFIG_CONTATOS.mensagens.cadastroCliente(dados.url || CONFIG_CONTATOS.urls.cadastro);
                break;
            case 'peca':
                mensagem = CONFIG_CONTATOS.mensagens.consultaPeca(dados.codigo || 'FI-001');
                break;
            case 'suporte':
                mensagem = CONFIG_CONTATOS.mensagens.suporte();
                break;
            default:
                mensagem = dados.mensagem || 'Olá! Entre em contato.';
        }

        return `https://wa.me/${numero}?text=${encodeURIComponent(mensagem)}`;
    },

    // Gerar link de email
    gerarLinkEmail: function(assunto, corpo) {
        const email = CONFIG_CONTATOS.contatos.email.principal;
        return `mailto:${email}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(corpo)}`;
    },

    // Obter informações de contato formatadas
    obterContatos: function() {
        return {
            whatsapp: CONFIG_CONTATOS.contatos.whatsapp.numeroFormatado,
            email: CONFIG_CONTATOS.contatos.email.principal,
            telefone: CONFIG_CONTATOS.contatos.telefone.principal
        };
    },

    // Atualizar contatos em elementos HTML
    atualizarElementosHTML: function() {
        // Atualizar WhatsApp
        const whatsappElements = document.querySelectorAll('[data-whatsapp]');
        whatsappElements.forEach(el => {
            el.textContent = CONFIG_CONTATOS.contatos.whatsapp.numeroFormatado;
            if (el.tagName === 'A') {
                el.href = CONFIG_CONTATOS.contatos.whatsapp.link;
            }
        });

        // Atualizar Email
        const emailElements = document.querySelectorAll('[data-email]');
        emailElements.forEach(el => {
            el.textContent = CONFIG_CONTATOS.contatos.email.principal;
            if (el.tagName === 'A') {
                el.href = `mailto:${CONFIG_CONTATOS.contatos.email.principal}`;
            }
        });

        // Atualizar Telefone
        const telefoneElements = document.querySelectorAll('[data-telefone]');
        telefoneElements.forEach(el => {
            el.textContent = CONFIG_CONTATOS.contatos.telefone.principal;
            if (el.tagName === 'A') {
                el.href = `tel:${CONFIG_CONTATOS.contatos.telefone.principal}`;
            }
        });
    }
};

// Exportar configurações
if (typeof window !== 'undefined') {
    window.CONFIG_CONTATOS = CONFIG_CONTATOS;
    window.ContatosHelper = ContatosHelper;
} else {
    module.exports = { CONFIG_CONTATOS, ContatosHelper };
}
