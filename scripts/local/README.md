# Runner local (Windows)

Opcional: máquina de diseño que ejecuta tareas que el agente cloud no puede.

## Flujo sugerido

1. `git pull` del repo
2. Ejecutar `scripts\run-local.ps1` (crear cuando haya plugins compilados)
3. Copiar salidas a `exchange\`
4. `git add exchange && git commit && git push`

## Tareas del runner

- Validar DXF (`python scripts/dxf/validate_layout.py`)
- Compilar y correr plugins Tekla
- Iniciar IDEA ConnectionRestApi y batch `scripts/idea/run_connection_batch.py`

## PowerShell ejemplo (IDEA API)

```powershell
$ideaPath = "C:\Program Files\IDEA StatiCa\StatiCa 24.1"
Start-Process -FilePath "$ideaPath\IdeaStatiCa.ConnectionRestApi.exe" -ArgumentList "-port:5193"
cd C:\Proyectos\SUM-ESTRUCTURA
pip install -r scripts\requirements.txt
pip install ideastatica-connection-api
python scripts\idea\run_connection_batch.py
```
