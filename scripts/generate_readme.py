#!/usr/bin/env python3
"""Build the README image catalogue from Git-tracked files (standard library only)."""

import argparse
import html
from pathlib import Path
import subprocess
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN IMAGE CATALOG -->"
END = "<!-- END IMAGE CATALOG -->"
EXTENSIONS = {".apng", ".avif", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def image_paths(root: Path) -> list[str]:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode("utf-8")
    return sorted(
        (
            name for name in tracked.split("\0")
            if name and (root / name).suffix.lower() in EXTENSIONS
            and (root / name).is_file() and not (root / name).is_symlink()
        ),
        key=lambda name: (name.casefold(), name),
    )


def image_url(repository: str, branch: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{quote(repository, safe='/')}/{quote(branch, safe='')}/{quote(path, safe='/')}"


def render_gallery(paths: list[str], repository: str, branch: str) -> str:
    if not paths:
        return "Aucune image pour le moment. Ajoutez une image au dépôt pour la voir apparaître ici."

    label = "image disponible" if len(paths) == 1 else "images disponibles"
    rows = [f"**{len(paths)} {label}.**", ""]
    for path in paths:
        name = html.escape(path)
        url = image_url(repository, branch, path)
        rows.extend([
            f"<h3>{name}</h3>",
            "",
            f'<a href="{url}"><img src="{url}" alt="{name}" width="140" align="left"></a>',
            "",
            "```text",
            url,
            "```",
            "",
            f'<a href="{url}">Ouvrir l’image en taille réelle ↗</a>',
            "",
            '<br clear="all">',
            "",
        ])
    return "\n".join(rows).rstrip()


def update_readme(content: str, gallery: str) -> str:
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("Le README doit contenir exactement une paire de marqueurs de catalogue.")
    before, remaining = content.split(START)
    if END not in remaining:
        raise ValueError("Les marqueurs de catalogue sont inversés.")
    _, after = remaining.split(END)
    return f"{before}{START}\n\n{gallery}\n\n{END}{after}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default="Seiven-Public/Login", help="Dépôt utilisé pour les URL : propriétaire/nom")
    parser.add_argument("--branch", default="main", help="Branche contenant les images")
    args = parser.parse_args()
    readme = ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")
    gallery = render_gallery(image_paths(ROOT), args.repository, args.branch)
    updated = update_readme(content, gallery)
    if updated != content:
        readme.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
