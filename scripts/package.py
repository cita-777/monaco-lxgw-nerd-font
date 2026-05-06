#!/usr/bin/env python3
"""Create release archives."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from build import VARIANTS


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
FONTS = ROOT / "fonts"


def write_variant_zip(variant: dict[str, str]) -> Path:
    archive = DIST / variant["zip"]
    font_dir = FONTS / variant["ps_family"]
    package_root = variant["ps_family"]
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for font in sorted(font_dir.glob("*.ttf")):
            zf.write(font, f"{package_root}/{font.name}")
        for name in ["README.md", "README.zh-CN.md", "NOTICE.md", "upstream.lock.json"]:
            path = ROOT / name
            if path.exists():
                zf.write(path, f"{package_root}/{name}")
    print(f"wrote {archive}")
    return archive


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(exist_ok=True)
    for variant in VARIANTS:
        write_variant_zip(variant)


if __name__ == "__main__":
    main()
