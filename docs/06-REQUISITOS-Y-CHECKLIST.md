# Requisitos y checklist de arranque

## Lo que necesito de vos (bloqueante para modelar)

| # | Item | Dónde entregarlo |
|---|------|------------------|
| 1 | Plano/layout DWG o DXF de la estructura | `exchange/autocad/in/` |
| 2 | Normativa y país (ej. CIRSOC 301/302, Argentina) | `config/criterios-proyecto.yaml` |
| 3 | Perfiles preferidos (IPN, W, tubos) y calidades (S355, etc.) | mismo archivo |
| 4 | Combinaciones de carga o referencia a memoria existente | `exchange/docs/` o PDF en repo |
| 5 | Criterio de conexiones (rígidas, articuladas, semirrígidas) | `config/criterios-proyecto.yaml` |
| 6 | Versión exacta Tekla / AutoCAD / IDEA instalada | checklist abajo |
| 7 | Plantillas de plano de oficina (si existen) | `templates/` |

## Checklist software en PC de diseño

- [ ] Tekla Structures Steel — versión: ____
- [ ] AutoCAD — versión: ____
- [ ] IDEA StatiCa + Connection — versión: ____
- [ ] Visual Studio 2022 (para plugins Tekla)
- [ ] Python 3.10+ y `pip install -r scripts/requirements.txt`
- [ ] Git + clone de este repositorio
- [ ] (Opcional) Git LFS para modelos Tekla

## Checklist MCP (preparado en el repo)

- [ ] `scripts/setup/install-mcp-stack.ps1` en Windows
- [ ] MCP en Cursor Desktop (`docs/07-CONFIGURACION-MCP.md`)
- [ ] AutoCAD 2026 + plugin; Tekla 2026; IDEA RestApi puerto 5193
- [ ] DWG/DXF en `exchange/autocad/in/` (push a GitHub)
- [ ] Normativa en `exchange/normativa/`

## Checklist primera iteración (cuando subas el DXF)

- [ ] Ejecutar validación DXF
- [ ] Revisar reporte con el agente
- [ ] Definir grilla Tekla
- [ ] Modelo esqueleto (columnas + vigas principales)
- [ ] Primera exportación IFC a `exchange/tekla/out/`

## Preguntas a resolver en kick-off

1. ¿Estructura nueva o ampliación?
2. ¿Taller propio o tercerizado (nivel de detalle en fab)?
3. ¿Todas las conexiones en IDEA o solo las no catalogadas?
4. ¿Idioma de planos y unidades en cotas?
