#!/usr/bin/env python3
# Ejecutar: python3 scripts/dxf/validate_layout.py <archivo.dxf>
"""
Valida un DXF de layout SUM contra capas y criterios definidos en config/nomenclatura.yaml.
Uso: python scripts/dxf/validate_layout.py exchange/autocad/out/SUM_layout_v01.dxf
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import ezdxf
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_NOM = ROOT / "config" / "nomenclatura.yaml"
REPORTS_DIR = ROOT / "exchange" / "reports"


def load_expected_layers() -> list[str]:
    with open(CONFIG_NOM, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return list(data.get("capas_autocad", []))


def validate(dxf_path: Path) -> dict:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    expected = set(load_expected_layers())
    found_layers: set[str] = set()
    entity_counts: dict[str, int] = {}
    errors: list[str] = []
    warnings: list[str] = []

    for e in msp:
        layer = e.dxf.layer if hasattr(e.dxf, "layer") else "0"
        found_layers.add(layer)
        entity_counts[layer] = entity_counts.get(layer, 0) + 1

    missing = sorted(expected - found_layers)
    extra_sum = sorted(l for l in found_layers if l.startswith("SUM_") and l not in expected)
    non_sum = sorted(l for l in found_layers if not l.startswith("SUM_") and l not in ("0", "Defpoints"))

    if missing:
        warnings.append(f"Capas SUM esperadas no encontradas: {missing}")
    if non_sum:
        warnings.append(f"Capas fuera del estándar SUM: {non_sum[:20]}")

    insunits = doc.header.get("$INSUNITS", 0)
    units_map = {0: "unspecified", 1: "inches", 4: "mm", 6: "meters"}
    units = units_map.get(insunits, f"code_{insunits}")

    extmin = doc.header.get("$EXTMIN")
    extmax = doc.header.get("$EXTMAX")
    bbox = None
    if extmin is not None and extmax is not None:
        bbox = {
            "min": [extmin[0], extmin[1], extmin[2] if len(extmin) > 2 else 0],
            "max": [extmax[0], extmax[1], extmax[2] if len(extmax) > 2 else 0],
        }

    if entity_counts.get("SUM_EJES", 0) == 0 and entity_counts.get("SUM_COL", 0) == 0:
        errors.append("No hay entidades en SUM_EJES ni SUM_COL; revisar capas o export.")

    status = "ok" if not errors else "fail"
    return {
        "file": str(dxf_path),
        "status": status,
        "units_insunits": units,
        "expected_layers": sorted(expected),
        "found_layers": sorted(found_layers),
        "entity_counts_by_layer": dict(sorted(entity_counts.items())),
        "missing_expected_layers": missing,
        "bbox": bbox,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: validate_layout.py <ruta.dxf>", file=sys.stderr)
        return 2

    dxf_path = Path(sys.argv[1])
    if not dxf_path.is_file():
        print(f"No existe: {dxf_path}", file=sys.stderr)
        return 2

    report = validate(dxf_path)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / "dxf-validation.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nReporte guardado: {out}")
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
