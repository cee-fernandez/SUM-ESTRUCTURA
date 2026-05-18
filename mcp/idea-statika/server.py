#!/usr/bin/env python3
"""
MCP IDEA StatiCa Connection API (2026).
Requiere en Windows: IdeaStatiCa.ConnectionRestApi.exe -port:5193
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[2]
IDEA_IN = ROOT / "exchange" / "idea" / "in"
IDEA_OUT = ROOT / "exchange" / "idea" / "out"
DEFAULT_PORT = int(os.environ.get("IDEA_REST_PORT", "5193"))

mcp = FastMCP(
    "sum-idea-statika",
    instructions="Conexiones de acero IDEA StatiCa vía Connection REST API local.",
)


def _rest_up(port: int) -> bool:
    try:
        with urlopen(f"http://127.0.0.1:{port}/", timeout=2) as _:
            return True
    except (URLError, OSError):
        return False


@mcp.tool()
def idea_health(port: int = DEFAULT_PORT) -> str:
    """Comprueba si el servicio IDEA Connection REST responde en localhost."""
    up = _rest_up(port)
    return json.dumps(
        {
            "port": port,
            "reachable": up,
            "hint": (
                r'Iniciar: "C:\Program Files\IDEA StatiCa\StatiCa 26.0\IdeaStatiCa.ConnectionRestApi.exe" -port:5193'
                if not up
                else "OK"
            ),
        },
        indent=2,
    )


@mcp.tool()
def list_connection_inputs() -> str:
    """Lista JSON de nodos en exchange/idea/in/ (excluye .example.json)."""
    if not IDEA_IN.is_dir():
        return json.dumps({"files": []})
    files = [
        p.name
        for p in IDEA_IN.glob("*.json")
        if p.is_file() and not p.name.endswith(".example.json")
    ]
    return json.dumps({"directory": str(IDEA_IN.relative_to(ROOT)), "files": sorted(files)}, indent=2)


@mcp.tool()
def read_connection_input(node_id: str) -> str:
    """Lee exchange/idea/in/{node_id}.json"""
    path = IDEA_IN / f"{node_id}.json"
    if not path.is_file():
        path = IDEA_IN / f"{node_id}"
    if not path.is_file():
        return json.dumps({"error": f"No existe input para {node_id}"})
    return path.read_text(encoding="utf-8")


@mcp.tool()
def run_connection_batch(port: int = DEFAULT_PORT) -> str:
    """
    Ejecuta scripts/idea/run_connection_batch.py (requiere ideastatica-connection-api instalado).
    """
    import subprocess
    import sys

    script = ROOT / "scripts" / "idea" / "run_connection_batch.py"
    env = {**os.environ, "IDEA_REST_PORT": str(port)}
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=env,
    )
    return json.dumps(
        {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "output_dir": str(IDEA_OUT.relative_to(ROOT)),
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
