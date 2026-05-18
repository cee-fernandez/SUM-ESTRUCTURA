# Arquitectura y roles

## Roles

| Rol | Función |
|-----|---------|
| **Agente (Cursor)** | Planifica, escribe scripts/macros, valida intercambios, documenta criterios, revisa reportes, mantiene el repo |
| **Ingeniero estructural (humano)** | Aprueba criterios, normativa, combinaciones de carga, aceptación de conexiones y planos |
| **Modelador Tekla (humano o mismo ingeniero)** | Opera Tekla, ejecuta plugins, emite planos |
| **Runner local (opcional)** | Script en Windows que ejecuta Tekla Open API / IDEA API bajo demanda |

## Carpetas de intercambio

```
exchange/
├── autocad/
│   ├── in/          # DWG/DXF que subes desde AutoCAD
│   └── out/         # DXF limpio exportado para Tekla
├── tekla/
│   ├── in/          # DXF referencia, perfiles CSV
│   └── out/         # IFC, BOM, lista nodos conexión
├── idea/
│   ├── in/          # Inputs por nodo (JSON/CSV)
│   └── out/         # .ideaCon, PDF memoria
└── reports/         # Validaciones y QA generados por scripts
```

## Versiones de software recomendadas

Alinear **una misma generación** entre herramientas (ej. Tekla 2024 + IDEA 24.x). Anotar versiones reales en `config/criterios-proyecto.yaml` al iniciar.

| Software | Uso en el proyecto |
|----------|-------------------|
| AutoCAD 2024+ | Layout, detalles 2D, export DXF |
| Tekla Structures (Steel) | Modelo, drawings, NC si aplica |
| IDEA StatiCa Steel + Connection | Conexiones viga-columna, viga-viga, bases, rigidizadores |
| Visual Studio 2022 | Compilar plugins Tekla / runner C# |
| Python 3.10+ | Cliente IDEA Connection API, utilidades DXF |

## Sincronización Git ↔ estación local

1. Clonar este repo en la PC de diseño
2. Trabajar en Tekla/AutoCAD/IDEA con rutas relativas al clone (ej. `C:\Proyectos\SUM-ESTRUCTURA\exchange\`)
3. Tras cada sesión: copiar exportaciones a `exchange/`, `git commit`, `git push`
4. El agente en la nube analiza el push y devuelve instrucciones o nuevos scripts

## Seguridad y licencias

- No commitear licencias, claves ni rutas absolutas de red interna en scripts públicos
- Modelos Tekla grandes: usar Git LFS o solo IFC + reportes en repo, `.db1` en backup local documentado
