# En casa — un solo comando (después del clone)

## Lo que ya está en GitHub (no tenés que armarlo vos)

Todo el marco del proyecto, MCP, scripts y configuración están en:

https://github.com/cee-fernandez/SUM-ESTRUCTURA

Rama `main` (actualizada).

## En la PC de casa (único paso manual inevitable)

1. Instalá **Cursor**, **Git**, **Python**, **Node**, **.NET 8** y tus licencias **AutoCAD / Tekla / IDEA 2026** (si aún no están).
2. En PowerShell:

```powershell
git clone https://github.com/cee-fernandez/SUM-ESTRUCTURA.git
cd SUM-ESTRUCTURA
.\scripts\setup\install-mcp-stack.ps1
```

3. Abrí la carpeta en **Cursor Desktop** (misma cuenta).
4. Antes de modelar: AutoCAD + Tekla abiertos, IDEA RestApi en puerto 5193.

El agente en Cursor hace el resto (validar DXF, Tekla, conexiones) cuando los archivos estén en `exchange/` o uses MCP.

## Modelo Tekla (.db1)

No va a GitHub. Copialo del trabajo con pendrive/nube a la misma carpeta que uses en Tekla.

## Sincronizar trabajo ↔ casa

Solo hace falta `git push` en una PC y `git pull` en la otra. El agente cloud actualiza `exchange/` cuando pusheás.
