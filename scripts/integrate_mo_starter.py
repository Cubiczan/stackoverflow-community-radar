"""Thin wrapper: MO starter nodes are now wired inside build_kg.py.

Prefer:
  python scripts/build_kg.py

This script remains for refreshing only the MO slice without a full rebuild
if graph.json already exists — otherwise delegates to build_kg.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print("MO starter integration lives in scripts/build_kg.py — rebuilding full KG…")
    return subprocess.call([sys.executable, str(ROOT / "scripts" / "build_kg.py")])


if __name__ == "__main__":
    raise SystemExit(main())
