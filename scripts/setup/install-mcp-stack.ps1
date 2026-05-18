# SUM-ESTRUCTURA — Instala servidores MCP y dependencias (Windows)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

Write-Host "==> Raiz proyecto: $Root"
Set-Location $Root

Write-Host "==> Python MCP (sum-exchange, sum-idea)"
python -m pip install --upgrade pip
pip install -r mcp\requirements.txt
pip install -r scripts\requirements.txt
pip install ideastatica-connection-api

Write-Host "==> AutoCAD MCP (vendor/autocad-mcp)"
if (-not (Test-Path "$Root\vendor\autocad-mcp")) {
    git clone https://github.com/moisesbritez92/autocad-mcp.git "$Root\vendor\autocad-mcp"
}
Set-Location "$Root\vendor\autocad-mcp"
npm install
npm run build
Set-Location "$Root\vendor\autocad-mcp\autocad-plugin"
dotnet build -c Release

Write-Host "==> Tekla svMCP (vendor/svMCP)"
Set-Location $Root
if (-not (Test-Path "$Root\vendor\svMCP")) {
    git clone https://github.com/40ushek/svMCP.git "$Root\vendor\svMCP"
}
Set-Location "$Root\vendor\svMCP"
dotnet build

Write-Host "==> Cursor MCP config"
$dest = "$Root\.cursor\mcp.json"
$src = "$Root\mcp\mcp.windows.full.json"
Copy-Item $src $dest -Force
Write-Host "Copiado $src -> $dest"

Write-Host ""
Write-Host "LISTO. Pasos manuales:"
Write-Host "  1. AutoCAD 2026: NETLOAD plugin en vendor\autocad-mcp\autocad-plugin\bin\Release\net8.0-windows\"
Write-Host "  2. Tekla 2026 abierto antes de usar MCP tekla"
Write-Host "  3. IDEA: IdeaStatiCa.ConnectionRestApi.exe -port:5193"
Write-Host "  4. Reiniciar Cursor para cargar MCP"
Write-Host "  5. Subir DWG/DXF a exchange\autocad\in\ y git push"
