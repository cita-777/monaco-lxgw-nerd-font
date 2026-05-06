# Monaco LXGW Nerd Font

[English README](README.md)

这是一个自动生成的字体仓库：把 `thep0y/monaco-nerd-font` 的 Monaco
Nerd Font 四种变体，和 `lxgw/LxgwWenKai` 的 LXGW WenKai Mono 中文字形合并。

生成后的字体保留 Monaco 的英文、编程符号、上游变体自带的连字、Powerline
和 Nerd Font 图标；中文、CJK 标点、假名、全角字符由 LXGW WenKai Mono 补齐。

## 下载

到 GitHub Releases 下载最新产物。现在会生成四个 zip，对齐上游的两个维度：
是否连字，以及 Nerd Font 图标是否强制单格宽。

| 文件 | 是否连字 | Nerd 图标宽度 | 适合场景 | 字体名称 |
| --- | --- | --- | --- | --- |
| `MonacoLXGWNerdFont.zip` | 否 | 偏宽/原始宽度 | GUI 编辑器，图标想大一点 | `Monaco LXGW Nerd Font` |
| `MonacoLXGWNerdFontMono.zip` | 否 | 强制单格宽 | 终端 / nvim / tmux 首选 | `Monaco LXGW Nerd Font Mono` |
| `MonacoLXGWLigaturizedNerdFont.zip` | 是 | 偏宽/原始宽度 | VS Code / JetBrains，想要连字 | `Monaco LXGW Ligaturized Nerd Font` |
| `MonacoLXGWLigaturizedNerdFontMono.zip` | 是 | 强制单格宽 | 终端也想试连字，但可能有坑 | `Monaco LXGW Ligaturized Nerd Font Mono` |

每个 zip 里都有四个样式：Regular、Bold、Italic、Bold Italic。

## 为什么之前只有一个？

`thep0y/monaco-nerd-font` 的 Release 实际有四个可选包：

| 上游文件 | 是否连字 | Nerd 图标宽度 |
| --- | --- | --- |
| `MonacoNerdFont.zip` | 否 | 偏宽/原始宽度 |
| `MonacoNerdFontMono.zip` | 否 | 强制单格宽 |
| `MonacoLigaturizedNerdFont.zip` | 是 | 偏宽/原始宽度 |
| `MonacoLigaturizedNerdFontMono.zip` | 是 | 强制单格宽 |

这个仓库第一版只拉取了 `MonacoLigaturizedNerdFontMono.zip`，所以只生成了一个
`MonacoLXGWNerdFontMono.zip`。现在构建流程已经改成跟踪全部四个上游 asset，
并对应生成四个 LXGW 增强版 zip。

## 本地构建

```sh
python3 -m pip install -r requirements.txt
python3 scripts/fetch_sources.py
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/package.py
```

生成字体在 `fonts/`，打包文件在 `dist/`。

## 自动更新

GitHub Actions 支持手动触发和定时检查：

- `workflow_dispatch`：手动运行。
- `schedule`：每周自动检查上游。
- 自动下载最新 Monaco Nerd Font 和 LXGW WenKai Release 产物。
- 自动重新合并四个变体、验证关键 glyph、打包 zip。
- 如果上游版本变化，会提交生成字体和 `upstream.lock.json`，并创建或覆盖 Release asset。

跟踪的上游：

- `thep0y/monaco-nerd-font`：`MonacoNerdFont.zip`、
  `MonacoNerdFontMono.zip`、`MonacoLigaturizedNerdFont.zip`、
  `MonacoLigaturizedNerdFontMono.zip`
- `lxgw/LxgwWenKai`：`LXGWWenKaiMono-Regular.ttf`、
  `LXGWWenKaiMono-Medium.ttf`

## Related Work

- [`thep0y/monaco-nerd-font`](https://github.com/thep0y/monaco-nerd-font)：
  Monaco Nerd Font 四种变体来源。
- [`lxgw/LxgwWenKai`](https://github.com/lxgw/LxgwWenKai)：
  霞鹜文楷 / 霞鹜文楷等宽，提供中文和 CJK 字形。
- [`ryanoasis/nerd-fonts`](https://github.com/ryanoasis/nerd-fonts)：
  Nerd Fonts 项目，`thep0y/monaco-nerd-font` 的图标补丁来源。

## 许可证

见 `NOTICE.md`。LXGW WenKai 是 SIL OFL 1.1。`thep0y/monaco-nerd-font`
当前没有在 GitHub 声明 license，所以如果要在个人使用之外再分发二进制字体，需要自行确认上游授权风险。
