# Configuración AutoCAD

## Objetivo

AutoCAD es la fuente **2D de referencia**: ejes, niveles, contornos de arquitectura, vanos y cotas que guían el modelado en Tekla. El agente **no abre AutoCAD**; trabaja sobre **DXF exportado** y puede proponer correcciones en forma de capas/listados.

## Configuración en AutoCAD (tu PC)

### Unidades y sistema

- Unidades: **metros** (recomendado) o milímetros — declarar en `config/criterios-proyecto.yaml`
- INSUNITS coherente con export DXF
- UCS alineado con ejes estructurales del edificio

### Capas estándar (prefijo `SUM_`)

| Capa | Contenido | Color sugerido |
|------|-----------|----------------|
| `SUM_EJES` | Ejes grid | 8 |
| `SUM_NIVEL` | Líneas de nivel / cota 0 | 3 |
| `SUM_COL` | Ejes de columnas | 1 |
| `SUM_VIG` | Ejes de vigas | 4 |
| `SUM_ARQ` | Muros / límites arquitectura | 9 |
| `SUM_SEC` | Líneas de sección para Tekla | 6 |
| `SUM_TEXTO` | Cotas y anotaciones | 7 |

### Bloques

- Evitar bloques anónimos no explotables en DXF
- Insertar columnas como **círculo + cruz** en `SUM_COL` o polilínea de centro

### Exportación DXF para el agente y Tekla

1. `EXPORT` o `DXFOUT`
2. Versión: **AutoCAD 2018 DXF** (buena compatibilidad Tekla / netDxf)
3. Guardar en: `exchange/autocad/out/SUM_layout_v01.dxf`
4. Incluir solo capas `SUM_*` si el archivo debe ser liviano

## Qué hace el agente con el DXF

Ejecutar (en CI o local con Python):

```bash
python scripts/dxf/validate_layout.py exchange/autocad/out/SUM_layout_v01.dxf
```

Salida: `exchange/reports/dxf-validation.json` con:

- Unidades detectadas
- Capas presentes / faltantes
- Entidades en capas incorrectas
- Bounding box del layout

## Lectura / modificación programática

| Método | Dónde corre | Uso |
|--------|-------------|-----|
| **ezdxf** (Python) | Nube / Linux | Validar, extraer líneas/ejes, generar DXF corregido |
| **netDxf / ACadSharp** (.NET) | Windows | Edición avanzada offline |
| **AutoCAD .NET API** | Windows + AutoCAD abierto | Solo en estación local |

Para **modificar** DWG nativo sin exportar: requiere AutoCAD instalado; el agente prepara scripts `.lsp` o instrucciones paso a paso.

## Plantilla de checklist antes de exportar

- [ ] Todas las capas `SUM_*` creadas
- [ ] Origen (0,0) en intersección de ejes A-1 o documentado
- [ ] Sin geometría duplicada superpuesta
- [ ] Cotas críticas (vanos, altura entrepiso) en `SUM_TEXTO`
- [ ] Archivo nombrado con versión `v01`, `v02`, …

## Integración con Tekla

- Tekla: **Archivo → Importar → DXF/DWG** usando el DXF de `exchange/autocad/out/`
- Alternativa: recrear grilla en Tekla desde CSV de ejes generado por el script (futuro: `scripts/dxf/export_grid_csv.py`)
