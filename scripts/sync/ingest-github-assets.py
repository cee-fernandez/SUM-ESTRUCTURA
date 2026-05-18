#!/usr/bin/env python3
"""
Organiza archivos de entrada en exchange/ y actualiza inventario.
Ejecutar tras git pull cuando subas DWG, normativa PDF, etc.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCHANGE = ROOT / "exchange"
IN_ACAD = EXCHANGE / "autocad" / "in"
IN_NORM = EXCHANGE / "normativa"
REPORT = EXCHANGE / "reports" / "assets-inventory.json"

EXTENSIONS_ACAD = {".dwg", ".dxf", ".dwf"}
EXTENSIONS_NORM = {".pdf", ".md", ".yaml", ".yml", ".docx", ".txt"}


def scan(root: Path, exts: set[str]) -> list[dict]:
    found = []
    if not root.is_dir():
        return found
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            found.append(
                {
                    "path": str(p.relative_to(ROOT)),
                    "size_bytes": p.stat().st_size,
                    "suffix": p.suffix.lower(),
                }
            )
    return sorted(found, key=lambda x: x["path"])


def promote_loose_files() -> list[str]:
    """Mueve DWG/DXF sueltos en la raíz del repo hacia exchange/autocad/in/."""
    moved = []
    for p in ROOT.iterdir():
        if p.is_file() and p.suffix.lower() in EXTENSIONS_ACAD:
            dest = IN_ACAD / p.name
            IN_ACAD.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest))
            moved.append(str(dest.relative_to(ROOT)))
    norm_root = ROOT / "normativa"
    if norm_root.is_dir():
        IN_NORM.mkdir(parents=True, exist_ok=True)
        for p in norm_root.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTENSIONS_NORM:
                dest = IN_NORM / p.name
                if not dest.exists():
                    shutil.copy2(p, dest)
                    moved.append(str(dest.relative_to(ROOT)))
    return moved


def main() -> None:
    IN_ACAD.mkdir(parents=True, exist_ok=True)
    IN_NORM.mkdir(parents=True, exist_ok=True)
    moved = promote_loose_files()
    inventory = {
        "autocad_in": scan(IN_ACAD, EXTENSIONS_ACAD),
        "normativa": scan(IN_NORM, EXTENSIONS_NORM),
        "also_scan_repo_exchange": scan(EXCHANGE, EXTENSIONS_ACAD | EXTENSIONS_NORM),
        "moved_this_run": moved,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(inventory, indent=2, ensure_ascii=False))
    if not inventory["autocad_in"]:
        print(
            "\nAVISO: No hay DWG/DXF en exchange/autocad/in/. "
            "Subilos a GitHub en esa carpeta o en la raíz del repo."
        )


if __name__ == "__main__":
    main()
