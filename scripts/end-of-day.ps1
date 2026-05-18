# Ejecutar antes de irte (trabajo o casa): sube CAD/normativa a GitHub
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

$inAcad = Join-Path $Root "exchange\autocad\in"
$inNorm = Join-Path $Root "exchange\normativa"
New-Item -ItemType Directory -Force -Path $inAcad, $inNorm | Out-Null

# Buscar DWG/DXF recientes en Escritorio y Descargas (ultimas 48h)
$searchRoots = @(
    [Environment]::GetFolderPath("Desktop"),
    [Join-Path $env:USERPROFILE "Downloads"]
)
$exts = @("*.dwg", "*.dxf")
$copied = @()
foreach ($dir in $searchRoots) {
    if (-not (Test-Path $dir)) { continue }
    foreach ($ext in $exts) {
        Get-ChildItem -Path $dir -Filter $ext -File -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-48) } |
            ForEach-Object {
                $dest = Join-Path $inAcad $_.Name
                if (-not (Test-Path $dest)) {
                    Copy-Item $_.FullName $dest
                    $copied += $dest
                }
            }
    }
}

# PDF normativa en Descargas
$downloads = Join-Path $env:USERPROFILE "Downloads"
if (Test-Path $downloads) {
    Get-ChildItem $downloads -Filter "*.pdf" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } |
        Select-Object -First 5 |
        ForEach-Object {
            $dest = Join-Path $inNorm $_.Name
            if (-not (Test-Path $dest)) {
                Copy-Item $_.FullName $dest
                $copied += $dest
            }
        }
}

Write-Host "Archivos copiados a exchange:"
if ($copied.Count -eq 0) { Write-Host "  (ninguno nuevo; ponelos manualmente en exchange\autocad\in\)" }
else { $copied | ForEach-Object { Write-Host "  $_" } }

python scripts\sync\ingest-github-assets.py 2>$null
if (-not $?) { python3 scripts/sync/ingest-github-assets.py }

git add exchange\ config\
$status = git status --porcelain
if ($status) {
    git commit -m "Sync fin de jornada: exchange $(Get-Date -Format yyyy-MM-dd)"
    git push origin main
    Write-Host "PUSH OK a GitHub main"
} else {
    Write-Host "Nada nuevo para commit. Copia DWG a exchange\autocad\in\ y volve a ejecutar."
}

Write-Host ""
Write-Host "Listo. En casa: git clone o git pull y install-mcp-stack.ps1"
