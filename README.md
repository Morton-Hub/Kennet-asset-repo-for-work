# Kennet-asset-repo-for-work

Bibliothèque d'assets de jeu (2D, 3D, UI, icônes, audio, polices) servant de source de contenu pour mes projets.

Le contenu vient du bundle **Kenney Game Assets All-in-1 3.8.0** ([kenney.nl](https://kenney.nl)), entièrement sous licence **CC0** : utilisable dans des projets personnels comme commerciaux, sans attribution obligatoire.

## Contenu

270 packs · ~106 000 fichiers · ~1 Go

| Dossier | Contenu | Packs |
| --- | --- | ---: |
| [`2d/`](2d) | Sprites, tilesets, personnages, décors, particules | 160 |
| [`3d/`](3d) | Kits de modèles low-poly (FBX, OBJ, GLB/GLTF, DAE, STL) | 54 |
| [`ui/`](ui) | Éléments d'interface, curseurs, contrôles mobiles | 10 |
| [`icons/`](icons) | Icônes de jeu, prompts d'entrée (clavier, manettes) | 8 |
| [`audio/`](audio) | Effets sonores, jingles, boucles musicales, voix (OGG) | 16 |
| [`fonts/`](fonts) | 16 polices Kenney (TTF) + webfonts (WOFF/WOFF2) | 1 |
| [`extras/`](extras) | Exemples Construct, miniguides, fonds d'écran | 4 |
| [`early-access/`](early-access) | Packs presque finalisés, utilisables tels quels | 2 |
| [`archive/`](archive) | Packs dépréciés, remplacés ou refaits | 15 |

La liste complète des packs (version, nombre de fichiers, formats, aperçu) est dans **[CATALOG.md](CATALOG.md)**, et en version exploitable par script dans [`catalog.json`](catalog.json).

## Organisation

```
<catégorie>/<pack>/…         ex. 2d/tiny-dungeon/Tilemap/tilemap.png
```

- Les dossiers de **catégorie** et de **pack** sont en `kebab-case` (minuscules, sans espaces) pour donner des chemins stables et faciles à écrire.
- **L'intérieur d'un pack est laissé tel que Kenney le livre** (noms avec majuscules et espaces compris). Les fichiers d'un pack se référencent entre eux (`.obj` → `.mtl`, `.gltf` → `.bin`, `.tmx` → `.tsx`, atlas `.xml` → `.png`) : les renommer casserait ces liens.

Un pack contient en général :

| Élément | Rôle |
| --- | --- |
| `License.txt` | Licence CC0 et version du pack |
| `Preview.png`, `Sample*.png` | Aperçu du pack et exemples d'utilisation |
| `PNG/`, `Vector/` | Sprites individuels (PNG) et sources vectorielles (SVG) |
| `Spritesheet/`, `Tilesheet/`, `Tilemap/` | Planches de sprites, avec atlas `.xml` ou description `.txt` |
| `Tiled/` | Cartes et tilesets pour [Tiled](https://www.mapeditor.org/) (`.tmx`, `.tsx`) |
| `Models/<FORMAT> format/` | Modèles 3D, un sous-dossier par format (`GLTF`, `FBX`, `OBJ`, `DAE`, `STL`) |
| `Audio/` | Sons au format `.ogg` |

## Utiliser les assets dans un projet

**Récupérer seulement quelques packs** (sans télécharger tout le dépôt) :

```bash
git clone --filter=blob:none --sparse https://github.com/Morton-Hub/Kennet-asset-repo-for-work.git assets
cd assets
git sparse-checkout set 2d/tiny-dungeon audio/ui-audio fonts
```

**Lien direct vers un fichier** (les espaces à l'intérieur d'un pack s'écrivent `%20`) :

```
https://raw.githubusercontent.com/Morton-Hub/Kennet-asset-repo-for-work/main/2d/tiny-dungeon/Tilemap/tilemap.png
https://raw.githubusercontent.com/Morton-Hub/Kennet-asset-repo-for-work/main/fonts/Kenney%20Pixel.ttf
```

**Chercher un pack par script** : `catalog.json` liste pour chaque pack son chemin, son nom, sa version, ses formats et son image d'aperçu.

```bash
# packs 3D qui contiennent des .glb
jq -r '.packs[] | select(.category == "3d" and .formats.glb) | .path' catalog.json
```

## Ajouter ou mettre à jour un pack

1. Déposer le pack dans la bonne catégorie, dans un dossier en `kebab-case` (ex. `2d/mon-nouveau-pack/`), sans toucher à son contenu.
2. Régénérer le catalogue : `python3 tools/build_catalog.py` (Python 3, aucune dépendance).
3. Committer le pack avec `CATALOG.md` et `catalog.json`.

Le fichier [`.gitattributes`](.gitattributes) désactive toute conversion de fins de ligne : les fichiers sont stockés à l'identique.

## Différences avec le zip d'origine

Le zip d'origine est attaché à la release [`V.0.0.1`](https://github.com/Morton-Hub/Kennet-asset-repo-for-work/releases/tag/V.0.0.1). Par rapport à lui :

- les dossiers de catégorie et de pack ont été renommés (`2D assets/Tiny Dungeon` → `2d/tiny-dungeon`) ; `Other/Fonts` est devenu `fonts/`, le reste de `Other/` et `Goodies/` sont dans `extras/` ;
- les 62 zips imbriqués (packs de l'archive, `sprites_isometric.zip`, webfonts…) ont été extraits sur place puis supprimés ;
- les raccourcis Windows `.url` ont été supprimés (liens repris ci-dessous) ;
- le caractère `×` dans quelques noms de dossiers a été remplacé par `x` (`Large (2x)`) ;
- `Overview.html` (index dont les liens pointaient vers les anciens chemins) est remplacé par `CATALOG.md` ; le lisez-moi d'origine avec le changelog est conservé dans [`docs/kenney-readme.html`](docs/kenney-readme.html).

## Documentation Kenney

- [Importer des modèles 3D dans un moteur de jeu](https://kenney.nl/knowledge-base/game-assets-3d/importing-3d-models-into-game-engines)
- [Utiliser les tilemaps](https://kenney.nl/documentation/game-assets/tilemaps)
- [Utiliser les kits de modèles](https://kenney.nl/documentation/game-assets/model-kits)
- [Utiliser les prompts d'entrée](https://kenney.nl/knowledge-base/game-assets-2d/using-input-prompts)
- [Importer les tuiles de la série Isometric Miniature](https://kenney.nl/knowledge-base/game-assets-2d/importing-isometric-miniature-series-tiles)
- [Utiliser les skyboxes](https://kenney.nl/knowledge-base/game-assets-2d/how-to-use-skyboxes)

## Licence et crédits

Tous les assets sont créés par **[Kenney](https://kenney.nl)** et publiés sous [Creative Commons Zero (CC0)](http://creativecommons.org/publicdomain/zero/1.0/). Chaque pack contient son propre `License.txt`. Le crédit « Kenney » ou « www.kenney.nl » est apprécié mais pas obligatoire.

Kenney demande de ne pas redistribuer le bundle All-in-1 tel quel et de renvoyer plutôt vers sa [page d'achat](https://kenney.itch.io/kenney-game-assets) ; les packs individuels, eux, peuvent être redistribués librement. Pour soutenir son travail : [kenney.nl/donate](https://kenney.nl/donate).
