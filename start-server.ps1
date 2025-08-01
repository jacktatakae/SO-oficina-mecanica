# Script PowerShell para iniciar o Sistema VRS Universal
# Inicia servidor HTTP local para teste completo de PWA

Write-Host "🚀 Iniciando Servidor VRS Universal..." -ForegroundColor Green
Write-Host ""

# Verificar se Python está disponível
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
        
        # Verificar porta disponível
        $port = 8080
        $portInUse = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        
        if ($portInUse) {
            Write-Host "⚠️  Porta 8080 em uso, tentando 8081..." -ForegroundColor Yellow
            $port = 8081
        }
        
        Write-Host "🌐 Iniciando servidor na porta $port..." -ForegroundColor Blue
        Write-Host ""
        Write-Host "📱 URLs para teste:" -ForegroundColor Cyan
        Write-Host "   Sistema Principal: http://localhost:$port" -ForegroundColor White
        Write-Host "   Mobile: http://localhost:$port/inventario-mobile.html" -ForegroundColor White
        Write-Host "   Scanner: http://localhost:$port/scanner-visual.html" -ForegroundColor White
        Write-Host ""
        Write-Host "🔧 Funcionalidades disponíveis:" -ForegroundColor Cyan
        Write-Host "   ✅ PWA completo (instalável)" -ForegroundColor Green
        Write-Host "   ✅ Funcionamento offline" -ForegroundColor Green
        Write-Host "   ✅ Service Worker ativo" -ForegroundColor Green
        Write-Host "   ✅ Backup automático" -ForegroundColor Green
        Write-Host "   ✅ Scanner IA" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 Para instalar como app:" -ForegroundColor Yellow
        Write-Host "   1. Abra no navegador" -ForegroundColor White
        Write-Host "   2. Procure ícone 'Instalar' na barra de endereços" -ForegroundColor White
        Write-Host "   3. Clique e confirme instalação" -ForegroundColor White
        Write-Host ""
        Write-Host "🛑 Pressione Ctrl+C para parar o servidor" -ForegroundColor Red
        Write-Host ""
        
        # Tentar abrir no navegador automaticamente
        Start-Process "http://localhost:$port"
        
        # Iniciar servidor
        python -m http.server $port
        
    } else {
        Write-Host "❌ Python não encontrado" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 Alternativas:" -ForegroundColor Yellow
        Write-Host "   1. Instale Python: https://python.org" -ForegroundColor White
        Write-Host "   2. Ou abra index.html diretamente no navegador" -ForegroundColor White
        Write-Host "   3. Para PWA completo, use servidor local" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Erro ao verificar Python: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Solução: Abra index.html diretamente no navegador" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
