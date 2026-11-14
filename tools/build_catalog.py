#!/usr/bin/env python3
"""Regenerate catalog.json and CATALOG.md from the asset folders.

Run from anywhere:  python3 tools/build_catalog.py

A pack is a direct sub-folder of a category folder (2d/, 3d/, ...). Display
names already present in catalog.json are kept; a new pack gets its name from
its License.txt title, or from its folder name.
"""
import json
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# folder -> (title, description). Order here is the order in CATALOG.md.
CATEGORIES = {
    "2d": ("2D", "Sprites, tilesets, personnages, décors, particules."),
    "3d": ("3D", "Kits de modèles low-poly (FBX, OBJ, GLB/GLTF, DAE, STL)."),
    "ui": ("UI", "Éléments d'interface, curseurs, contrôles mobiles."),
    "icons": ("Icônes", "Icônes de jeu et prompts d'entrée (clavier, manettes)."),
    "audio": ("Audio", "Effets sonores, jingles, boucles musicales, voix (OGG)."),
    "fonts": ("Polices", "Polices Kenney (TTF) et webfonts (WOFF/WOFF2)."),
    "extras": ("Extras", "Exemples Construct, miniguides, fonds d'écran."),
    "early-access": ("Early access", "Packs presque finalisés, utilisables tels quels."),
    "archive": ("Archive", "Packs dépréciés, remplacés ou refaits."),
}
# Categories that are one pack on their own (no sub-folder per pack).
SINGLE_PACK = {"fonts": "Kenney Fonts"}

# Extensions that are documentation or tooling rather than assets.
NOT_ASSETS = {"txt", "html", "md", "pdf", "import", "cfg", "meta", "json"}


def scan(path):
    files, size, formats = 0, 0, {}
    for folder, _, names in os.walk(path):
        for name in names:
            files += 1
            size += os.path.getsize(os.path.join(folder, name))
            ext = os.path.splitext(name)[1].lstrip(".").lower() or "(none)"
            formats[ext] = formats.get(ext, 0) + 1
    return files, size, dict(sorted(formats.items(), key=lambda kv: (-kv[1], kv[0])))


def license_title(path):
    """First non-empty line of License.txt, e.g. 'Coaster Kit (1.0)'."""
    try:
        with open(os.path.join(path, "License.txt"), encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.strip():
                    return line.strip()
    except OSError:
        pass
    return ""


def preview(path):
    names = sorted(n for n in os.listdir(path) if os.path.isfile(os.path.join(path, n)))
    for pattern in (r"preview\.png$", r"preview.*\.(png|jpg)$", r"sample.*\.(png|jpg)$"):
        for name in names:
            if re.match(pattern, name, re.I):
                return name
    return None


def build():
    try:
        with open(os.path.join(ROOT, "catalog.json"), encoding="utf-8") as f:
            known = {p["path"]: p["name"] for p in json.load(f)["packs"]}
    except (OSError, ValueError, KeyError):
        known = {}

    packs = []
    for category in CATEGORIES:
        base = os.path.join(ROOT, category)
        if not os.path.isdir(base):
            continue
        if category in SINGLE_PACK:
            entries = [(category, SINGLE_PACK[category])]
        else:
            entries = [
                (f"{category}/{d}", None)
                for d in sorted(os.listdir(base))
                if os.path.isdir(os.path.join(base, d))
            ]
        for rel, fixed_name in entries:
            path = os.path.join(ROOT, rel)
            title = license_title(path)
            version = re.search(r"\((\d+(?:\.\d+)*)\)\s*$", title)
            files, size, formats = scan(path)
            shot = preview(path)
            packs.append({
                "path": rel,
                "category": category,
                "name": fixed_name
                or known.get(rel)
                or re.sub(r"\s*\(\d+(?:\.\d+)*\)\s*$", "", title)
                or os.path.basename(rel).replace("-", " ").title(),
                "version": version.group(1) if version else None,
                "files": files,
                "bytes": size,
                "formats": formats,
                "preview": f"{rel}/{shot}" if shot else None,
                "license": "CC0-1.0",
            })
    return packs


def human(size):
    return f"{size / 1e6:.1f} Mo" if size >= 1e5 else f"{size / 1e3:.0f} Ko"


def write_markdown(packs):
    out = [
        "# Catalogue des assets",
        "",
        "> Fichier généré par `tools/build_catalog.py` — ne pas modifier à la main.",
        "> La même liste est disponible en JSON dans [`catalog.json`](catalog.json).",
        "",
        f"**{len(packs)} packs · {sum(p['files'] for p in packs):,} fichiers · "
        f"{sum(p['bytes'] for p in packs) / 1e9:.2f} Go**".replace(",", " "),
        "",
        "| Catégorie | Dossier | Packs | Fichiers | Taille |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    by_cat = {c: [p for p in packs if p["category"] == c] for c in CATEGORIES}
    for cat, (title, _) in CATEGORIES.items():
        group = by_cat[cat]
        if group:
            anchor = title.lower().replace(" ", "-")  # GitHub heading anchor
            out.append(
                f"| [{title}](#{anchor}) | [`{cat}/`]({cat}) | {len(group)} | "
                f"{sum(p['files'] for p in group)} | {human(sum(p['bytes'] for p in group))} |"
            )
    for cat, (title, description) in CATEGORIES.items():
        group = by_cat[cat]
        if not group:
            continue
        out += [
            "",
            f"## {title}",
            "",
            f"{description} Dossier : [`{cat}/`]({cat})",
            "",
            "| Pack | Version | Fichiers | Taille | Formats | Aperçu |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
        for p in group:
            formats = ", ".join(e for e in p["formats"] if e not in NOT_ASSETS)
            shot = f"[aperçu]({quote(p['preview'])})" if p["preview"] else "—"
            out.append(
                f"| [{p['name']}]({quote(p['path'])}) | {p['version'] or '—'} | {p['files']} | "
                f"{human(p['bytes'])} | {formats or '—'} | {shot} |"
            )
    with open(os.path.join(ROOT, "CATALOG.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    packs = build()
    with open(os.path.join(ROOT, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump({"source": "Kenney Game Assets All-in-1 3.8.0", "packs": packs}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    write_markdown(packs)
    print(f"{len(packs)} packs, {sum(p['files'] for p in packs)} fichiers")


if __name__ == "__main__":
    main()
