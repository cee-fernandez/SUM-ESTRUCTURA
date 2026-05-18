# Handoff — seguir en casa (10 min setup)

**Fecha de corte:** generado al cerrar jornada en PC trabajo.  
**Repo:** https://github.com/cee-fernandez/SUM-ESTRUCTURA (rama `main`)

---

## Lo que ya está hecho (no repetir)

- [x] Proyecto completo en GitHub `main` (docs, MCP, scripts, `config/`)
- [x] Criterios CIRSOC + software **2026** en `config/criterios-proyecto.yaml`
- [x] Servidores MCP definidos (`.cursor/mcp.json`)
- [x] Script fin de jornada: `scripts/end-of-day.ps1`

---

## En la PC de trabajo AHORA (2 minutos)

En PowerShell, carpeta del proyecto:

```powershell
cd C:\ruta\donde\clonaste\SUM-ESTRUCTURA
.\scripts\end-of-day.ps1
```

Eso copia DWG/DXF recientes del Escritorio/Descargas a `exchange/autocad/in/` y hace **git push**.

Si el DWG está en otra carpeta, copialo manualmente a `exchange\autocad\in\` y volvé a ejecutar el script.

**Modelo Tekla:** si ya existe `.db1`, copialo a pendrive/OneDrive (Tekla no va a Git).

---

## En casa (orden exacto)

### 1. Clonar o actualizar

```powershell
cd C:\Proyectos
git clone https://github.com/cee-fernandez/SUM-ESTRUCTURA.git
# si ya clonaste antes:
# cd SUM-ESTRUCTURA && git pull
```

### 2. Instalar MCP (una vez por PC)

```powershell
cd SUM-ESTRUCTURA
.\scripts\setup\install-mcp-stack.ps1
```

### 3. Cursor

- Abrir carpeta `SUM-ESTRUCTURA` en **Cursor Desktop** (misma cuenta).
- Verificar MCP activos en Settings.

### 4. Antes de pedirle algo al agente

| Programa | Acción |
|----------|--------|
| AutoCAD 2026 | Abierto + plugin NETLOAD (ver `docs/07-CONFIGURACION-MCP.md`) |
| Tekla 2026 | Abierto + modelo `.db1` si lo copiaste |
| IDEA 2026 | `IdeaStatiCa.ConnectionRestApi.exe -port:5193` |

### 5. Primer mensaje al agente en casa

> "Hice git pull. Revisá exchange/autocad/in, validá el DXF y decime los pasos para la grilla Tekla."

---

## Archivos que el agente busca

| Ruta | Contenido |
|------|-----------|
| `exchange/autocad/in/*.dwg` o `*.dxf` | Layout estructura |
| `exchange/normativa/*.pdf` | CIRSOC / memorias |
| `config/criterios-proyecto.yaml` | Criterios (editar `conexiones` cuando definan) |
| `exchange/tekla/in/grid-from-dxf.csv` | Grilla extraída del DXF (si corrimos export) |

---

## Pendientes del proyecto

1. **Subir DWG/DXF real** a `exchange/autocad/in/` (bloqueante modelado)
2. **Definir criterio de conexiones** → `config/criterios-proyecto.yaml` sección `conexiones`
3. **Normativa PDF** en `exchange/normativa/` si no se subió con end-of-day
4. **Tekla:** importar DXF o CSV grilla → modelo esqueleto
5. **IDEA:** nodos en `exchange/tekla/out/connection-nodes.csv`

---

## Comandos útiles

```powershell
git pull
python scripts\sync\ingest-github-assets.py
python scripts\dxf\validate_layout.py exchange\autocad\in\TU_ARCHIVO.dxf
python scripts\dxf\export_grid_csv.py exchange\autocad\in\TU_ARCHIVO.dxf
.\scripts\end-of-day.ps1
```

---

## Contacto con el agente cloud

Cada `git push` desde casa o trabajo actualiza lo que el agente ve en la nube. No hace falta reconfigurar GitHub.
