#!/usr/bin/env python3
"""Print the release tag derived from upstream source versions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "upstream.lock.json"


def clean(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z.]+", "-", value).strip("-")


def main() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    monaco = clean(lock["monaco_nerd_font"]["tag"])
    lxgw = clean(lock["lxgw_wenkai"]["tag"])
    tag = f"monaco-{monaco}-lxgw-{lxgw}"
    if "--name" in sys.argv:
        print(f"Monaco LXGW Nerd Font bundle ({monaco} + {lxgw})")
    else:
        print(tag)


if __name__ == "__main__":
    main()
