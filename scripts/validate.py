#!/usr/bin/env python3
"""Validate generated fonts with lightweight metadata and cmap checks."""

from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont

from build import VARIANTS


ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
REQUIRED = {
    0x0041: "Latin A",
    0x4E2D: "CJK 中",
    0x3002: "CJK punctuation 。",
    0xFF21: "Fullwidth Ａ",
    0xE0B0: "Powerline private-use glyph",
    0xF101: "Nerd Font private-use glyph",
}


def cmap(font: TTFont) -> dict[int, str]:
    merged: dict[int, str] = {}
    for table in font["cmap"].tables:
        if table.isUnicode():
            merged.update(table.cmap)
    return merged


def name_value(font: TTFont, name_id: int) -> str:
    for record in font["name"].names:
        if record.nameID == name_id:
            return record.toUnicode()
    return "<missing>"


def validate(path: Path, expected_family: str) -> None:
    font = TTFont(path, lazy=False)
    mapping = cmap(font)
    missing = [label for codepoint, label in REQUIRED.items() if codepoint not in mapping]
    if missing:
        raise SystemExit(f"{path.name}: missing required glyphs: {', '.join(missing)}")
    family = name_value(font, 1)
    if family != expected_family:
        raise SystemExit(f"{path.name}: unexpected family name {family!r}, expected {expected_family!r}")
    latin_width = font["hmtx"].metrics[mapping[0x0041]][0]
    cjk_width = font["hmtx"].metrics[mapping[0x4E2D]][0]
    if cjk_width < latin_width:
        raise SystemExit(f"{path.name}: CJK width {cjk_width} should be >= Latin width {latin_width}")
    print(
        f"{path.relative_to(FONTS)}: ok, family={family!r}, "
        f"glyphs={len(font.getGlyphOrder())}, unicode={len(mapping)}, A={latin_width}, 中={cjk_width}"
    )


def main() -> None:
    expected_count = len(VARIANTS) * 4
    fonts = sorted(FONTS.glob("*/*.ttf"))
    if len(fonts) != expected_count:
        raise SystemExit(f"expected {expected_count} fonts, found {len(fonts)}")
    family_by_dir = {variant["ps_family"]: variant["family"] for variant in VARIANTS}
    for path in fonts:
        expected_family = family_by_dir.get(path.parent.name)
        if not expected_family:
            raise SystemExit(f"{path}: unknown variant directory")
        validate(path, expected_family)


if __name__ == "__main__":
    main()
