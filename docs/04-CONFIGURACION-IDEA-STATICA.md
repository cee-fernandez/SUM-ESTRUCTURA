# Configuración IDEA StatiCa (conexiones)

## Objetivo

Diseñar **conexiones a medida** (no solo catalogadas Tekla): rigidizadores, placas, soldaduras, tornilleros, comprobación CBFEM según norma del proyecto.

## Requisitos

- IDEA StatiCa **Steel** + licencia **Connection**
- Misma norma que Tekla (declarar en `config/criterios-proyecto.yaml`)

## Servicio REST local (automatización)

En la PC con IDEA instalado:

```powershell
cd "C:\Program Files\IDEA StatiCa\StatiCa 24.1"
.\IdeaStatiCa.ConnectionRestApi.exe -port:5193
```

Cliente Python (agente genera scripts en `scripts/idea/`):

```bash
pip install ideastatica-connection-api
python scripts/idea/run_connection_batch.py
```

Documentación: [Connection API overview](https://developer.ideastatica.com/docs/api/connection-api/connection_api_overview.html)

## Flujo manual + asistido por agente

1. **Tekla** exporta `exchange/tekla/out/connection-nodes.csv` con:
   - `node_id`, perfiles, ángulos, material, combinación, cortantes/momentos (o referencia a caso)
2. **Agente** genera por nodo un JSON en `exchange/idea/in/{node_id}.json` con geometría propuesta inicial
3. **Humano** abre IDEA Connection, importa o replica geometría, ajusta rigidizadores
4. **IDEA** calcula → export PDF + `.ideaCon` a `exchange/idea/out/`
5. **Tekla** modela conexión final según geometría aprobada (componentes custom o detalle atornillado)

## Tipologías esperadas en SUM-ESTRUCTURA

Definir en `config/idea/connection-types.yaml`:

| Tipo | Código | Descripción |
|------|--------|-------------|
| Viga a columna perno | `VB_COL_BOLT` | Cartela / fin plate |
| Viga a columna rígida | `VB_COL_MOM` | Placas almas + alas + rigidizadores |
| Viga a viga | `VB_VB` | Unión con rigidizador intermedio |
| Base columna | `BASE_COL` | Placa base + anclajes |
| Arriostre | `BRACE` | Placa o tornillo único |

## Plantillas IDEA

Guardar plantillas reutilizables en:

`config/idea/templates/` (archivos `.ideaCon` de referencia, sin datos de proyecto sensibles)

## Criterios de aceptación de una conexión

- [ ] Utilización ≤ 1,0 (o factor definido en criterios)
- [ ] Deformación dentro de límite si aplica
- [ ] Detalle constructible (soldadura accesible, apriete tornillos)
- [ ] Coherencia con modelo Tekla (perfiles, inclinación)
- [ ] Memoria PDF archivada en `exchange/idea/out/`

## Enlace con Tekla

Tras aprobar en IDEA:

1. Actualizar UDA `SUM_NODO_IDEA` en miembros Tekla
2. Modelar placas/rigidizadores con **componente personalizado** o **detalle de conexión**
3. En plano de montaje: nota “Conexión según memoria IDEA {node_id} rev{n}”
