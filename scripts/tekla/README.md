# Tekla Open API — scripts locales

Compilar y ejecutar **con Tekla Structures abierto** en Windows.

## Setup Visual Studio

1. Crear proyecto **Class Library (.NET Framework 4.8)** o .NET Standard 2.0 según versión Tekla
2. Referencias desde carpeta Tekla (ej. `C:\Program Files\Tekla Structures\2024.0\nt\bin\`):
   - `Tekla.Structures.Model.dll`
   - `Tekla.Structures.dll`
3. Copiar el `.dll` resultante a la carpeta de extensiones Tekla o ejecutar como aplicación externa

## Scripts planificados para SUM-ESTRUCTURA

| Script | Función |
|--------|---------|
| `ExportConnectionNodes.cs` | CSV de nodos viga-columna → `exchange/tekla/out/connection-nodes.csv` |
| `AssignUdasFromCsv.cs` | Asignar `SUM_NODO_IDEA` desde CSV |
| `CreateBeamsFromGrid.cs` | Vigas entre puntos de grilla (CSV desde DXF) |

Documentación: https://developer.tekla.com/documentation/get-started-tekla-structures-open-api

## Ejemplo mínimo (crear viga)

Ver código oficial: [Create beam using two points](https://developer.tekla.com/documentation/code-example-create-beam-using-two-points)
