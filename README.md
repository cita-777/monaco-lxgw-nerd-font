# Monaco LXGW Nerd Font Mono

Monaco LXGW Nerd Font Mono is a terminal font family that combines:

- `MonacoLigaturized Nerd Font Mono` for Latin glyphs, programming ligatures,
  Powerline symbols, and Nerd Font icons.
- `LXGW WenKai Mono` for Chinese, CJK punctuation, kana, and fullwidth forms.

The goal is a Monaco-style programming font with usable Chinese fallback in the
same installable font family.

## Download

Download the prebuilt zip from the latest GitHub Release:

```text
MonacoLXGWNerdFontMono.zip
```

Install the four `.ttf` files inside it:

- `MonacoLXGWNerdFontMono-Regular.ttf`
- `MonacoLXGWNerdFontMono-Bold.ttf`
- `MonacoLXGWNerdFontMono-Italic.ttf`
- `MonacoLXGWNerdFontMono-BoldItalic.ttf`

Then set your terminal font family to:

```text
Monaco LXGW Nerd Font Mono
```

## Build Locally

```sh
python3 -m pip install -r requirements.txt
python3 scripts/fetch_sources.py
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/package.py
```

Generated fonts are written to `fonts/`. The release zip is written to `dist/`.

## Upstream Automation

This repository includes a GitHub Actions workflow that can rebuild from upstream
sources automatically.

- `workflow_dispatch` runs on demand.
- `schedule` checks upstream weekly.
- The workflow downloads the latest Monaco and LXGW WenKai release assets.
- It rebuilds the fonts, validates required glyph coverage, commits changed
  generated fonts plus `upstream.lock.json`, and creates a release asset when
  upstream versions changed.

Tracked upstreams:

- `thep0y/monaco-nerd-font`, asset `MonacoLigaturizedNerdFontMono.zip`
- `lxgw/LxgwWenKai`, assets `LXGWWenKaiMono-Regular.ttf` and
  `LXGWWenKaiMono-Medium.ttf`

## Licensing

See `NOTICE.md`. LXGW WenKai is SIL OFL 1.1. The upstream Monaco Nerd Font repo
does not declare a GitHub license at the time this repository was created.

