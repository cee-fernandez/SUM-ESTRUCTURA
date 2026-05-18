#!/usr/bin/env python3
"""
Plantilla para batch de conexiones IDEA vía Connection REST API.
Ejecutar SOLO en PC Windows con IDEA StatiCa y el servicio REST activo:

  IdeaStatiCa.ConnectionRestApi.exe -port:5193

Requiere: pip install ideastatica-connection-api
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN_DIR = ROOT / "exchange" / "idea" / "in"
OUT_DIR = ROOT / "exchange" / "idea" / "out"
PORT = 5193


def main() -> int:
    try:
        from ideastatica_connection_api.ideastatica_connection_api import (
            ConnectionApiServiceAttacher,
        )
    except ImportError:
        print(
            "Instalar: pip install ideastatica-connection-api\n"
            "Este script no corre en cloud sin el servicio IDEA local.",
            file=sys.stderr,
        )
        return 2

    inputs = [p for p in IN_DIR.glob("*.json") if not p.name.endswith(".example.json")]
    if not inputs:
        print(f"No hay JSON en {IN_DIR}", file=sys.stderr)
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    attacher = ConnectionApiServiceAttacher(port=PORT)
    api = attacher.create_connection_api()

    for path in inputs:
        node_id = path.stem
        payload = json.loads(path.read_text(encoding="utf-8"))
        _ = api  # usar cuando se implemente open/calculate/export
        print(f"Procesando {node_id} ... (ajustar según API para abrir/calcular/exportar)")
        # TODO: mapear payload → operaciones Connection API del proyecto
        (OUT_DIR / f"{node_id}_status.json").write_text(
            json.dumps(
                {
                    "node_id": node_id,
                    "status": "pending_implementation",
                    "payload_keys": list(payload.keys()),
                }
            ),
            encoding="utf-8",
        )

    print(f"Listo. Revisar {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
