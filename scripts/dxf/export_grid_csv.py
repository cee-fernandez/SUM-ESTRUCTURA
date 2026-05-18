#!/usr/bin/env python3
"""Extrae líneas de capas SUM_EJES / SUM_COL a CSV para grilla Tekla."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import ezdxf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exchange" / "tekla" / "in" / "grid-from-dxf.csv"
LAYERS = {"SUM_EJES", "SUM_COL", "SUM_VIG", "SUM_NIVEL"}


def export(dxf_path: Path) -> int:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    rows: list[dict] = []
    for e in msp:
        layer = getattr(e.dxf, "layer", "0")
        if layer not in LAYERS:
            continue
        t = e.dxftype()
        if t == "LINE":
            s, end = e.dxf.start, e.dxf.end
            rows.append(
                {
                    "layer": layer,
                    "type": "LINE",
                    "x1": round(s.x, 4),
                    "y1": round(s.y, 4),
                    "z1": round(s.z, 4),
                    "x2": round(end.x, 4),
                    "y2": round(end.y, 4),
                    "z2": round(end.z, 4),
                }
            )
        elif t == "LWPOLYLINE":
            pts = list(e.get_points())
            for i in range(len(pts) - 1):
                rows.append(
                    {
                        "layer": layer,
                        "type": "LWPOLYLINE",
                        "x1": round(pts[i][0], 4),
                        "y1": round(pts[i][1], 4),
                        "z1": 0,
                        "x2": round(pts[i + 1][0], 4),
                        "y2": round(pts[i + 1][1], 4),
                        "z2": 0,
                    }
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        print(f"Sin geometría en capas {LAYERS}", file=sys.stderr)
        return 1
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"OK: {len(rows)} segmentos -> {OUT.relative_to(ROOT)}")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: export_grid_csv.py <archivo.dxf>", file=sys.stderr)
        return 2
    return export(Path(sys.argv[1]))


if __name__ == "__main__":
    raise SystemExit(main())
