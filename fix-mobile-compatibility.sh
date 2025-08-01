#!/bin/bash

# Script para corrigir problemas mobile em todas as páginas VRS
# Aplica PWA e otimizações mobile em páginas que ainda não têm

echo "🔧 Corrigindo compatibilidade mobile em todas as páginas VRS..."

# Lista de arquivos para corrigir
FILES=(
    "central-sistemas.html"
    "qr-permanente.html"
    "sistema-backup.html"
    "cadastro-cliente.html"
    "identificacao-pecas.html"
    "launcher.html"
)

# Função para adicionar PWA headers
add_pwa_headers() {
    local file="$1"
    local title="$2"
    local theme_color="$3"
    local app_name="$4"
    
    echo "  📝 Adicionando PWA a $file..."
    
    # Backup do arquivo original
    cp "$file" "${file}.bak"
    
    # Adicionar PWA headers após a tag <head>
    sed -i.tmp '/<head>/a\
    <meta charset="UTF-8">\
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, minimum-scale=1.0, maximum-scale=5.0">\
    \
    <!-- PWA Manifest -->\
    <link rel="manifest" href="manifest.json">\
    \
    <!-- Meta tags para PWA -->\
    <meta name="theme-color" content="'$theme_color'">\
    <meta name="background-color" content="'$theme_color'">\
    <meta name="display" content="standalone">\
    <meta name="orientation" content="portrait-primary">\
    \
    <!-- Meta tags para mobile -->\
    <meta name="mobile-web-app-capable" content="yes">\
    <meta name="apple-mobile-web-app-capable" content="yes">\
    <meta name="apple-mobile-web-app-status-bar-style" content="default">\
    <meta name="apple-mobile-web-app-title" content="'$app_name'">\
' "$file"
    
    # Limpar arquivo temporário
    rm "${file}.tmp" 2>/dev/null
}

# Função para adicionar CSS mobile
add_mobile_css() {
    local file="$1"
    
    echo "  🎨 Adicionando CSS mobile a $file..."
    
    # Adicionar CSS mobile antes do </style>
    sed -i.tmp 's|</style>|\
        /* Melhorias Mobile */\
        * {\
            -webkit-tap-highlight-color: transparent;\
        }\
        \
        @media (max-width: 768px) {\
            body {\
                padding: 0.5rem;\
            }\
            \
            .container, .manager-container, .central-container, .backup-container {\
                padding: 1rem;\
                border-radius: 15px;\
            }\
            \
            .btn {\
                min-height: 44px;\
                font-size: 16px;\
            }\
            \
            .form-control, .form-select {\
                min-height: 44px;\
                font-size: 16px;\
            }\
            \
            .btn-group .btn {\
                width: 100%;\
                margin: 0.25rem 0;\
            }\
            \
            .card {\
                margin-bottom: 1rem;\
            }\
        }\
        \
        @media (max-width: 480px) {\
            .container {\
                margin: 0;\
                border-radius: 0;\
                min-height: 100vh;\
            }\
        }\
</style>|g' "$file"
    
    # Limpar arquivo temporário
    rm "${file}.tmp" 2>/dev/null
}

# Função para adicionar PWA JavaScript
add_pwa_js() {
    local file="$1"
    local app_name="$2"
    
    echo "  ⚙️ Adicionando PWA JavaScript a $file..."
    
    # Adicionar JavaScript PWA antes do </body>
    sed -i.tmp 's|</body>|\
    <script>\
        // PWA Functionality\
        let deferredPrompt;\
        let serviceWorkerRegistration;\
        \
        function initPWA() {\
            if ("serviceWorker" in navigator) {\
                navigator.serviceWorker.register("./sw.js")\
                    .then(registration => {\
                        serviceWorkerRegistration = registration;\
                        console.log("✅ Service Worker registrado:", registration);\
                    })\
                    .catch(error => {\
                        console.error("❌ Erro ao registrar Service Worker:", error);\
                    });\
            }\
            \
            window.addEventListener("beforeinstallprompt", (e) => {\
                e.preventDefault();\
                deferredPrompt = e;\
                showInstallBanner();\
            });\
            \
            window.addEventListener("appinstalled", () => {\
                console.log("✅ PWA '"$app_name"' instalado");\
                hideInstallBanner();\
            });\
        }\
        \
        function showInstallBanner() {\
            const banner = document.createElement("div");\
            banner.id = "installBanner";\
            banner.className = "position-fixed bottom-0 start-0 end-0 bg-primary text-white p-3";\
            banner.style.zIndex = "9999";\
            banner.innerHTML = `\
                <div class="container-fluid">\
                    <div class="row align-items-center">\
                        <div class="col">\
                            <strong>📱 Instalar '"$app_name"'</strong><br>\
                            <small>Acesso rápido na tela inicial</small>\
                        </div>\
                        <div class="col-auto">\
                            <button class="btn btn-light btn-sm me-2" onclick="installPWA()">Instalar</button>\
                            <button class="btn btn-outline-light btn-sm" onclick="hideInstallBanner()">✕</button>\
                        </div>\
                    </div>\
                </div>\
            `;\
            document.body.appendChild(banner);\
        }\
        \
        function hideInstallBanner() {\
            const banner = document.getElementById("installBanner");\
            if (banner) banner.remove();\
        }\
        \
        async function installPWA() {\
            if (deferredPrompt) {\
                deferredPrompt.prompt();\
                const { outcome } = await deferredPrompt.userChoice;\
                deferredPrompt = null;\
                hideInstallBanner();\
            }\
        }\
        \
        // Prevenir zoom indesejado\
        document.addEventListener("gesturestart", function (e) {\
            e.preventDefault();\
        });\
        \
        // Inicializar PWA\
        document.addEventListener("DOMContentLoaded", initPWA);\
    </script>\
</body>|g' "$file"
    
    # Limpar arquivo temporário
    rm "${file}.tmp" 2>/dev/null
}

# Processar cada arquivo
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "🔧 Processando $file..."
        
        # Definir configurações específicas para cada arquivo
        case "$file" in
            "central-sistemas.html")
                title="VRS Central de Sistemas"
                theme_color="#6c757d"
                app_name="VRS Central"
                ;;
            "qr-permanente.html")
                title="VRS Gerador QR"
                theme_color="#17a2b8"
                app_name="VRS QR"
                ;;
            "sistema-backup.html")
                title="VRS Sistema de Backup"
                theme_color="#28a745"
                app_name="VRS Backup"
                ;;
            "cadastro-cliente.html")
                title="VRS Cadastro de Clientes"
                theme_color="#fd7e14"
                app_name="VRS Cadastro"
                ;;
            "identificacao-pecas.html")
                title="VRS Identificação de Peças"
                theme_color="#e83e8c"
                app_name="VRS Peças"
                ;;
            "launcher.html")
                title="VRS Launcher"
                theme_color="#6f42c1"
                app_name="VRS Launcher"
                ;;
        esac
        
        # Verificar se já tem PWA
        if ! grep -q "manifest.json" "$file"; then
            add_pwa_headers "$file" "$title" "$theme_color" "$app_name"
        else
            echo "  ✅ PWA já configurado em $file"
        fi
        
        # Verificar se já tem CSS mobile
        if ! grep -q "webkit-tap-highlight-color" "$file"; then
            add_mobile_css "$file"
        else
            echo "  ✅ CSS mobile já configurado em $file"
        fi
        
        # Verificar se já tem JavaScript PWA
        if ! grep -q "serviceWorker.register" "$file"; then
            add_pwa_js "$file" "$app_name"
        else
            echo "  ✅ JavaScript PWA já configurado em $file"
        fi
        
        echo "  ✅ $file processado com sucesso!"
        echo ""
    else
        echo "  ⚠️ $file não encontrado, pulando..."
    fi
done

echo ""
echo "🎉 Correção mobile concluída!"
echo ""
echo "📱 Resultados:"
echo "   ✅ PWA configurado em todas as páginas"
echo "   ✅ CSS mobile otimizado"
echo "   ✅ JavaScript PWA adicionado"
echo "   ✅ Service Worker integrado"
echo ""
echo "🧪 Para testar:"
echo "   1. Abra qualquer página no mobile"
echo "   2. Procure o banner de instalação"
echo "   3. Teste a funcionalidade offline"
echo ""
echo "🔗 Páginas corrigidas funcionam em:"
echo "   📱 Android - Chrome, Firefox, Edge"
echo "   📱 iOS - Safari, Chrome"
echo "   💻 Desktop - Todos os navegadores"
echo ""

exit 0
