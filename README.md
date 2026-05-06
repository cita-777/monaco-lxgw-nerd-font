# Monaco LXGW Nerd Font

[中文说明](README.zh-CN.md)

Monaco LXGW Nerd Font is a generated bundle that combines Monaco Nerd Font
variants from `thep0y/monaco-nerd-font` with CJK glyphs from LXGW WenKai Mono.

The generated fonts keep Monaco for Latin glyphs, programming ligatures when the
selected upstream variant has them, and Nerd Font icons. CJK/fullwidth glyphs are
added from LXGW WenKai Mono so Chinese text renders inside the same installable
font family.

## Downloads

Download the latest release assets from GitHub Releases. The four packages match
the two upstream Monaco Nerd Font dimensions: ligatures on/off and Nerd Font icon
width original/mono.

| Package | Ligatures | Nerd icon width | Recommended use | Font family |
| --- | --- | --- | --- | --- |
| `MonacoLXGWNerdFont.zip` | No | Original/proportional | GUI editors when larger icons are preferred | `Monaco LXGW Nerd Font` |
| `MonacoLXGWNerdFontMono.zip` | No | Single-cell mono | Terminals, nvim, tmux | `Monaco LXGW Nerd Font Mono` |
| `MonacoLXGWLigaturizedNerdFont.zip` | Yes | Original/proportional | VS Code / JetBrains when ligatures are wanted | `Monaco LXGW Ligaturized Nerd Font` |
| `MonacoLXGWLigaturizedNerdFontMono.zip` | Yes | Single-cell mono | Terminals that support ligatures, experimental | `Monaco LXGW Ligaturized Nerd Font Mono` |

Each package contains four styles: Regular, Bold, Italic, and Bold Italic.

## Why Four Packages?

The upstream `thep0y/monaco-nerd-font` release ships four zip assets:

| Upstream asset | Ligatures | Nerd icon width |
| --- | --- | --- |
| `MonacoNerdFont.zip` | No | Original/proportional |
| `MonacoNerdFontMono.zip` | No | Single-cell mono |
| `MonacoLigaturizedNerdFont.zip` | Yes | Original/proportional |
| `MonacoLigaturizedNerdFontMono.zip` | Yes | Single-cell mono |

The first version of this repository only used
`MonacoLigaturizedNerdFontMono.zip`, so it produced only one generated package.
The current build tracks all four upstream assets and emits all four matching
LXGW-enhanced packages.

## Build Locally

```sh
python3 -m pip install -r requirements.txt
python3 scripts/fetch_sources.py
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/package.py
```

Generated fonts are written to `fonts/`. Release zip files are written to
`dist/`.

## Upstream Automation

The GitHub Actions workflow supports both manual and scheduled rebuilds.

- `workflow_dispatch` runs on demand.
- `schedule` checks upstream weekly.
- The workflow downloads the latest Monaco Nerd Font and LXGW WenKai release
  assets.
- It rebuilds all four generated packages, validates required glyph coverage,
  commits changed generated fonts plus `upstream.lock.json`, and uploads or
  replaces Release assets when upstream versions change.

Tracked upstream assets:

- `thep0y/monaco-nerd-font`: `MonacoNerdFont.zip`,
  `MonacoNerdFontMono.zip`, `MonacoLigaturizedNerdFont.zip`,
  `MonacoLigaturizedNerdFontMono.zip`
- `lxgw/LxgwWenKai`: `LXGWWenKaiMono-Regular.ttf`,
  `LXGWWenKaiMono-Medium.ttf`

## Related Work

- [`thep0y/monaco-nerd-font`](https://github.com/thep0y/monaco-nerd-font):
  Monaco Nerd Font variants with bold, italic, bold italic, ligaturized, and
  mono-icon-width builds.
- [`lxgw/LxgwWenKai`](https://github.com/lxgw/LxgwWenKai): LXGW WenKai and
  LXGW WenKai Mono, used here for Chinese/CJK glyph coverage.
- [`ryanoasis/nerd-fonts`](https://github.com/ryanoasis/nerd-fonts): upstream
  Nerd Fonts project used by `thep0y/monaco-nerd-font`.

## Licensing

See `NOTICE.md`. LXGW WenKai is SIL OFL 1.1. The upstream Monaco Nerd Font repo
does not declare a GitHub license at the time this repository was created.
