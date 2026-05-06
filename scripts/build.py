#!/usr/bin/env python3
"""Build Monaco LXGW Nerd Font Mono.

The build keeps Latin, ligatures, and Nerd Font glyphs from MonacoLigaturized
Nerd Font Mono. It adds CJK/fullwidth glyphs from LXGW WenKai Mono so terminal
icons and Monaco-style ASCII are not overwritten by the Chinese source font.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from fontTools.misc.fixedTools import otRound
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
OUT = ROOT / "fonts"
LOCK = ROOT / "upstream.lock.json"

FAMILY = "Monaco LXGW Nerd Font Mono"
PS_FAMILY = "MonacoLXGWNerdFontMono"

STYLES = [
    {
        "style": "Regular",
        "base": "MonacoLigaturizedNerdFontMono-Regular.ttf",
        "cjk": "LXGWWenKaiMono-Regular.ttf",
        "file": "MonacoLXGWNerdFontMono-Regular.ttf",
        "ps": "Regular",
    },
    {
        "style": "Bold",
        "base": "MonacoLigaturizedNerdFontMono-Bold.ttf",
        "cjk": "LXGWWenKaiMono-Medium.ttf",
        "file": "MonacoLXGWNerdFontMono-Bold.ttf",
        "ps": "Bold",
    },
    {
        "style": "Italic",
        "base": "MonacoLigaturizedNerdFontMono-Italic.ttf",
        "cjk": "LXGWWenKaiMono-Regular.ttf",
        "file": "MonacoLXGWNerdFontMono-Italic.ttf",
        "ps": "Italic",
    },
    {
        "style": "Bold Italic",
        "base": "MonacoLigaturizedNerdFontMono-BoldItalic.ttf",
        "cjk": "LXGWWenKaiMono-Medium.ttf",
        "file": "MonacoLXGWNerdFontMono-BoldItalic.ttf",
        "ps": "BoldItalic",
    },
]

CJK_RANGES = [
    (0x2E80, 0x2EFF),   # CJK Radicals Supplement
    (0x2F00, 0x2FDF),   # Kangxi Radicals
    (0x3000, 0x303F),   # CJK Symbols and Punctuation
    (0x3040, 0x30FF),   # Hiragana and Katakana
    (0x3100, 0x312F),   # Bopomofo
    (0x31A0, 0x31BF),   # Bopomofo Extended
    (0x31C0, 0x31EF),   # CJK Strokes
    (0x31F0, 0x31FF),   # Katakana Phonetic Extensions
    (0x3200, 0x32FF),   # Enclosed CJK Letters and Months
    (0x3300, 0x33FF),   # CJK Compatibility
    (0x3400, 0x4DBF),   # CJK Unified Ideographs Extension A
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
    (0xFE10, 0xFE1F),   # Vertical Forms
    (0xFE30, 0xFE4F),   # CJK Compatibility Forms
    (0xFF00, 0xFFEF),   # Halfwidth and Fullwidth Forms
    (0x16FE0, 0x16FFF), # Ideographic Symbols and Punctuation
    (0x1F200, 0x1F2FF), # Enclosed Ideographic Supplement
    (0x20000, 0x3FFFF), # CJK extensions B and later planes
]


def unicode_cmap(font: TTFont) -> dict[int, str]:
    cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        if table.isUnicode():
            cmap.update(table.cmap)
    return cmap


def is_cjk_codepoint(codepoint: int) -> bool:
    return any(start <= codepoint <= end for start, end in CJK_RANGES)


def safe_tag(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z.]+", "-", value).strip("-") or "unknown"


def build_version() -> str:
    if not LOCK.exists():
        return "Version 0.1.0"
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    monaco = lock["monaco_nerd_font"]["tag"]
    lxgw = lock["lxgw_wenkai"]["tag"]
    return f"Version 0.1.0; Monaco Nerd Font {monaco}; LXGW WenKai {lxgw}"


def set_font_names(font: TTFont, style: str, ps_style: str) -> None:
    full_name = FAMILY if style == "Regular" else f"{FAMILY} {style}"
    postscript = f"{PS_FAMILY}-{ps_style}"
    version = build_version()
    unique = f"{full_name}; {version}"
    values = {
        1: FAMILY,
        2: style,
        3: unique,
        4: full_name,
        5: version,
        6: postscript,
        16: FAMILY,
        17: style,
    }
    name_table = font["name"]
    for name_id, text in values.items():
        name_table.setName(text, name_id, 3, 1, 0x409)
        name_table.setName(text, name_id, 1, 0, 0)
    name_table.setName(
        "Latin, ligatures, and Nerd Font glyphs from MonacoLigaturized Nerd Font Mono; CJK glyphs from LXGW WenKai Mono.",
        10,
        3,
        1,
        0x409,
    )
    name_table.setName("cita-777", 8, 3, 1, 0x409)


def scale_simple_glyph(glyph: Glyph, scale: float, glyf_table) -> None:
    glyph.expand(glyf_table)
    if glyph.numberOfContours <= 0 or not hasattr(glyph, "coordinates"):
        return
    glyph.coordinates.transform(((scale, 0), (0, scale)))
    glyph.coordinates.toInt()


def scale_composite_glyph(glyph: Glyph, scale: float, name_map: dict[str, str]) -> None:
    for component in glyph.components:
        component.glyphName = name_map[component.glyphName]
        component.x = otRound(component.x * scale)
        component.y = otRound(component.y * scale)


def copy_lxgw_glyphs(base: TTFont, cjk: TTFont) -> dict[str, str]:
    scale = base["head"].unitsPerEm / cjk["head"].unitsPerEm
    src_order = [name for name in cjk.getGlyphOrder() if name != ".notdef"]
    name_map = {name: f"lxgw{index:05d}" for index, name in enumerate(src_order)}

    base_order = base.getGlyphOrder()
    base_glyf = base["glyf"]
    cjk_glyf = cjk["glyf"]
    base_hmtx = base["hmtx"]
    cjk_hmtx = cjk["hmtx"]

    for old_name in src_order:
        new_name = name_map[old_name]
        glyph = copy.deepcopy(cjk_glyf[old_name])
        if glyph.isComposite():
            scale_composite_glyph(glyph, scale, name_map)
        else:
            scale_simple_glyph(glyph, scale, cjk_glyf)
        base_glyf.glyphs[new_name] = glyph
        advance, lsb = cjk_hmtx.metrics[old_name]
        base_hmtx.metrics[new_name] = (otRound(advance * scale), otRound(lsb * scale))

    base.setGlyphOrder(base_order + list(name_map.values()))
    base["maxp"].numGlyphs = len(base.getGlyphOrder())
    return name_map


def update_cmaps(base: TTFont, cjk: TTFont, name_map: dict[str, str]) -> int:
    cjk_cmap = unicode_cmap(cjk)
    merged = {
        codepoint: name_map[glyph_name]
        for codepoint, glyph_name in cjk_cmap.items()
        if is_cjk_codepoint(codepoint) and glyph_name in name_map
    }
    for table in base["cmap"].tables:
        if not table.isUnicode():
            continue
        for codepoint, glyph_name in merged.items():
            if codepoint <= 0xFFFF or table.format in {12, 13}:
                table.cmap[codepoint] = glyph_name
    return len(merged)


def normalize_tables(font: TTFont) -> None:
    if "DSIG" in font:
        del font["DSIG"]
    if "post" in font:
        font["post"].formatType = 3.0
    font["head"].modified = 0
    font["head"].created = 0


def build_one(style_config: dict[str, str]) -> Path:
    base_path = SOURCES / "MonacoLigaturizedNerdFontMono" / style_config["base"]
    cjk_path = SOURCES / "LXGWWenKaiMono" / style_config["cjk"]
    if not base_path.exists():
        raise SystemExit(f"missing source: {base_path}")
    if not cjk_path.exists():
        raise SystemExit(f"missing source: {cjk_path}")

    base = TTFont(base_path, recalcBBoxes=True, recalcTimestamp=False)
    cjk = TTFont(cjk_path, recalcBBoxes=True, recalcTimestamp=False)
    name_map = copy_lxgw_glyphs(base, cjk)
    mapped = update_cmaps(base, cjk, name_map)
    set_font_names(base, style_config["style"], style_config["ps"])
    normalize_tables(base)

    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / style_config["file"]
    base.save(output, reorderTables=True)
    print(f"built {output.name}: added {len(name_map)} LXGW glyphs, mapped {mapped} CJK codepoints")
    return output


def main() -> None:
    for style in STYLES:
        build_one(style)


if __name__ == "__main__":
    main()

