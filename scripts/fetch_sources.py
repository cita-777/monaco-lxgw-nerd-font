#!/usr/bin/env python3
"""Fetch upstream font inputs used by the build."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
LOCK = ROOT / "upstream.lock.json"

MONACO_REPO = "thep0y/monaco-nerd-font"
MONACO_ASSET = "MonacoLigaturizedNerdFontMono.zip"
LXGW_REPO = "lxgw/LxgwWenKai"
LXGW_ASSETS = [
    "LXGWWenKaiMono-Regular.ttf",
    "LXGWWenKaiMono-Medium.ttf",
]


def request_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "monaco-lxgw-nerd-font-builder",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def latest_release(repo: str) -> dict:
    return request_json(f"https://api.github.com/repos/{repo}/releases/latest")


def asset_url(release: dict, asset_name: str) -> str:
    for asset in release["assets"]:
        if asset["name"] == asset_name:
            return asset["browser_download_url"]
    names = ", ".join(asset["name"] for asset in release["assets"])
    raise SystemExit(f"asset {asset_name!r} not found; available: {names}")


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(req, timeout=300) as response:
        with destination.open("wb") as output:
            shutil.copyfileobj(response, output)


def fetch_monaco(release: dict) -> None:
    target = SOURCES / "MonacoLigaturizedNerdFontMono"
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / MONACO_ASSET
        download(asset_url(release, MONACO_ASSET), archive)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(target)


def fetch_lxgw(release: dict) -> None:
    target = SOURCES / "LXGWWenKaiMono"
    target.mkdir(parents=True, exist_ok=True)
    for asset in LXGW_ASSETS:
        download(asset_url(release, asset), target / asset)


def write_lock(monaco_release: dict, lxgw_release: dict) -> None:
    lock = {
        "monaco_nerd_font": {
            "repo": MONACO_REPO,
            "tag": monaco_release["tag_name"],
            "asset": MONACO_ASSET,
            "url": asset_url(monaco_release, MONACO_ASSET),
        },
        "lxgw_wenkai": {
            "repo": LXGW_REPO,
            "tag": lxgw_release["tag_name"],
            "assets": {
                name: asset_url(lxgw_release, name)
                for name in LXGW_ASSETS
            },
        },
    }
    LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    monaco_release = latest_release(MONACO_REPO)
    lxgw_release = latest_release(LXGW_REPO)
    fetch_monaco(monaco_release)
    fetch_lxgw(lxgw_release)
    write_lock(monaco_release, lxgw_release)
    print(f"Fetched Monaco {monaco_release['tag_name']} and LXGW WenKai {lxgw_release['tag_name']}")


if __name__ == "__main__":
    main()

