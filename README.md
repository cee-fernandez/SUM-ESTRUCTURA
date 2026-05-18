# SUM-ESTRUCTURA

Proyecto de diseño y modelado estructural en acero: **AutoCAD** (referencia y detalle 2D) → **Tekla Structures** (modelo 3D, planos de fabricación y montaje) → **IDEA StatiCa** (diseño de conexiones).

Este repositorio es el **centro de coordinación**: plan de trabajo, estándares, archivos de intercambio y automatización. Las aplicaciones CAD/BIM se ejecutan en una **estación Windows local** con licencias; el agente trabaja sobre exportaciones, scripts y documentación en este repo.

## Inicio rápido

1. Leer el plan maestro: [docs/00-PLAN-MAESTRO.md](docs/00-PLAN-MAESTRO.md)
2. Completar el checklist de requisitos: [docs/06-REQUISITOS-Y-CHECKLIST.md](docs/06-REQUISITOS-Y-CHECKLIST.md)
3. Colocar el layout de referencia en `exchange/autocad/in/`
4. Seguir las guías por herramienta en `docs/02` a `docs/04`

## Estructura del repositorio

| Carpeta | Uso |
|---------|-----|
| `docs/` | Plan, flujos, configuración y QA |
| `config/` | Nomenclatura, perfiles, plantillas Tekla/IDEA |
| `exchange/` | DXF/DWG, IFC, CSV, reportes entre herramientas |
| `scripts/` | Utilidades (validación DXF, cliente IDEA, etc.) |
| `templates/` | Plantillas de planos y listados |
| `.cursor/rules/` | Reglas para el agente en Cursor |

## Flujo resumido

```
AutoCAD (layout 2D) ──DXF/DWG──► Agente valida / extrae geometría
        │
        ▼
Tekla (modelo 3D + GA + fab + montaje) ◄── macros / Open API (local)
        │
        ▼
IDEA StatiCa (conexiones a medida) ◄── export nodos/perfiles + diseño CBFEM
```

## MCP — control de AutoCAD, Tekla e IDEA desde Cursor

Configuración lista en el repo:

- `.cursor/mcp.json` — servidores base (`sum-exchange`, `sum-idea-statika`)
- `mcp/mcp.windows.full.json` — stack completo 2026 (AutoCAD + Tekla + IDEA)
- Guía: [docs/07-CONFIGURACION-MCP.md](docs/07-CONFIGURACION-MCP.md)
- Instalador Windows: `scripts/setup/install-mcp-stack.ps1`

## Licencias (2026 en tu PC)

- AutoCAD 2026
- Tekla Structures 2026 (acero)
- IDEA StatiCa 2026 Steel + Connection
