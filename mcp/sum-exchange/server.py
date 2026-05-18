#!/usr/bin/env python3
"""MCP SUM-ESTRUCTURA: lectura/validación de exchange/ (funciona sin AutoCAD/Tekla/IDEA)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[2]
EXCHANGE = ROOT / "exchange"
VALIDATE = ROOT / "scripts" / "dxf" / "validate_layout.py"

mcp = FastMCP(
    "sum-exchange",
    instructions="Herramientas de archivos del proyecto SUM-ESTRUCTURA (DXF, normativa, reportes).",
)


def _glob_paths(folder: str, patterns: str) -> list[str]:
    base = EXCHANGE / folder
    if not base.is_dir():
        return []
    out: list[str] = []
    for pat in patterns.split(","):
        out.extend(str(p.relative_to(ROOT)) for p in base.rglob(pat.strip()))
    return sorted(out)


@mcp.tool()
def list_exchange_files(subfolder: str = "", pattern: str = "*") -> str:
    """Lista archivos bajo exchange/. subfolder ej: autocad/in. pattern ej: *.dwg,*.dxf,*.pdf"""
    base = EXCHANGE / subfolder if subfolder else EXCHANGE
    if not base.exists():
        return json.dumps({"error": f"No existe {base.relative_to(ROOT)}", "files": []})
    files = []
    for p in base.rglob(pattern if pattern != "*" else "*"):
        if p.is_file() and p.name != ".gitkeep":
            files.append(
                {
                    "path": str(p.relative_to(ROOT)),
                    "size_bytes": p.stat().st_size,
                    "suffix": p.suffix.lower(),
                }
            )
    return json.dumps({"count": len(files), "files": files}, ensure_ascii=False, indent=2)


@mcp.tool()
def read_text_asset(relative_path: str, max_chars: int = 12000) -> str:
    """Lee un archivo de texto/YAML/JSON/MD del repo (ruta relativa desde raíz)."""
    path = (ROOT / relative_path).resolve()
    if not str(path).startswith(str(ROOT.resolve())):
        return json.dumps({"error": "Ruta fuera del proyecto"})
    if not path.is_file():
        return json.dumps({"error": f"No encontrado: {relative_path}"})
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n... [truncado, total {len(text)} chars]"
    return text


@mcp.tool()
def validate_dxf(relative_path: str) -> str:
    """Valida un DXF contra capas SUM_* y escribe exchange/reports/dxf-validation.json."""
    dxf = (ROOT / relative_path).resolve()
    if not dxf.is_file():
        return json.dumps({"error": f"DXF no encontrado: {relative_path}"})
    if not VALIDATE.is_file():
        return json.dumps({"error": "Falta scripts/dxf/validate_layout.py"})
    proc = subprocess.run(
        [sys.executable, str(VALIDATE), str(dxf)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    report_path = EXCHANGE / "reports" / "dxf-validation.json"
    report = report_path.read_text(encoding="utf-8") if report_path.is_file() else proc.stdout
    return json.dumps(
        {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "report": json.loads(report) if report.strip().startswith("{") else report,
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def read_criterios_proyecto() -> str:
    """Devuelve config/criterios-proyecto.yaml (normativa, versiones, materiales)."""
    p = ROOT / "config" / "criterios-proyecto.yaml"
    return p.read_text(encoding="utf-8") if p.is_file() else "archivo no encontrado"


if __name__ == "__main__":
    mcp.run()
