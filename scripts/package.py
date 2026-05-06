#!/usr/bin/env python3
"""Create release archives."""

from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
FONTS = ROOT / "fonts"


def main() -> None:
    DIST.mkdir(exist_ok=True)
    archive = DIST / "MonacoLXGWNerdFontMono.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for font in sorted(FONTS.glob("*.ttf")):
            zf.write(font, f"MonacoLXGWNerdFontMono/{font.name}")
        for name in ["README.md", "NOTICE.md", "upstream.lock.json"]:
            path = ROOT / name
            if path.exists():
                zf.write(path, f"MonacoLXGWNerdFontMono/{name}")
    print(f"wrote {archive}")


if __name__ == "__main__":
    main()

