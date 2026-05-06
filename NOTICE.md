# Notice

This repository builds composite fonts from two upstream font sources:

- Monaco Nerd Font variants downloaded from `thep0y/monaco-nerd-font`.
- LXGW WenKai Mono downloaded from `lxgw/LxgwWenKai`.

Generated variants:

- `Monaco LXGW Nerd Font`: no ligatures, original/proportional Nerd Font icon widths.
- `Monaco LXGW Nerd Font Mono`: no ligatures, single-cell Nerd Font icon widths.
- `Monaco LXGW Ligaturized Nerd Font`: ligatures, original/proportional Nerd Font icon widths.
- `Monaco LXGW Ligaturized Nerd Font Mono`: ligatures, single-cell Nerd Font icon widths.

The generated fonts keep Latin glyphs, ligatures when present, Powerline symbols,
and Nerd Font private-use glyphs from the selected Monaco upstream asset. They
add CJK/fullwidth glyphs from LXGW WenKai Mono.

LXGW WenKai is licensed under the SIL Open Font License 1.1. The upstream
`thep0y/monaco-nerd-font` repository does not currently declare a GitHub license.
Check upstream licensing before redistributing binaries outside your own use.
