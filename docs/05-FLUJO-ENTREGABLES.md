# Flujo de entregables

## Lista de entregables finales

| # | Entregable | Formato | Origen |
|---|------------|---------|--------|
| 1 | Modelo estructural 3D | `.db1` + IFC | Tekla |
| 2 | Planos GA | PDF + DWG | Tekla Drawings |
| 3 | Planos fabricación | PDF + DXF piezas | Tekla |
| 4 | Planos montaje | PDF | Tekla |
| 5 | Lista de materiales | PDF / XSR | Tekla Reports |
| 6 | Memorias conexiones | PDF + `.ideaCon` | IDEA |
| 7 | Layout de referencia | DXF | AutoCAD |
| 8 | Informe QA cierre | MD/PDF | Repo `exchange/reports/` |

## Gates de calidad (no avanzar sin cumplir)

### Gate 1 — Layout

- DXF validado sin errores críticos en `dxf-validation.json`
- Ejes y niveles acordados por escrito en `config/criterios-proyecto.yaml`

### Gate 2 — Modelo Tekla

- IFC exportado y revisado
- BOM coherente con estimación (tolerancia definida en criterios)
- Lista `connection-nodes.csv` completa

### Gate 3 — Conexiones

- 100 % nodos críticos con PDF IDEA aprobado
- Tekla actualizado con geometría final

### Gate 4 — Planos

- Numeración de revisiones en todos los PDF
- Lista de planos (índice) en `exchange/reports/drawing-index.md`

## Convención de nombres de archivos

```
SUM_{disciplina}_{tipo}_{descripcion}_v{NN}.{ext}

Ejemplos:
SUM_ACO_GA_planta-nivel-01_v03.pdf
SUM_ACO_FAB_viga-V12_v02.pdf
SUM_IDEA_VB_COL_BOLT_nodo-N14_v01.pdf
```

## Plantilla informe QA cierre

Copiar a `exchange/reports/qa-cierre.md` y completar:

```markdown
# QA Cierre — SUM-ESTRUCTURA

- Fecha:
- Revisión modelo Tekla (UDA SUM_REVISION):
- Normativa:
- Responsable:

## Checklist
- [ ] Layout DXF v__
- [ ] IFC emitido
- [ ] Conexiones IDEA (n/N)
- [ ] Planos GA / FAB / MON indexados
- [ ] BOM final adjunto

## Pendientes
- 

## Aprobación
- Nombre / firma:
```
