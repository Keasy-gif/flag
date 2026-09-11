#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

if "/* barres categories plus douces" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

anchor = '.cat-bar-fill{height:100% !important; background:#fff; border-radius:99px; transition:width .5s ease; display:block;}'
n = src.count(anchor)
if n != 1:
    print("SKIP : ancre introuvable (trouvée " + str(n) + " fois) — rien touché.")
    sys.exit(0)

block = (
    "\n\n/* barres categories plus douces (verre, plus epaisses, lueur) */\n"
    ".cat-bars{gap:12px !important; margin-top:15px !important;}\n"
    ".cat-bar-top{font-size:12px !important; margin-bottom:6px !important;}\n"
    ".cat-bar-track{\n"
    "  height:7px !important; border-radius:99px !important; overflow:hidden; width:100%;\n"
    "  background:rgba(255,255,255,.16) !important;\n"
    "  backdrop-filter:blur(6px);\n"
    "  box-shadow:inset 0 1.5px 3px rgba(0,0,0,.22) !important;\n"
    "}\n"
    ".cat-bar-fill{\n"
    "  height:100% !important; border-radius:99px !important; transition:width .6s ease;\n"
    "  background:linear-gradient(90deg, rgba(255,255,255,.8), #fff) !important;\n"
    "  box-shadow:0 0 8px rgba(255,255,255,.55) !important;\n"
    "}\n"
)

src = src.replace(anchor, anchor + block, 1)
backup = PATH + ".backup-smoothbars-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : barres de catégories adoucies (plus épaisses, creux verre, lueur).")
print("Sauvegarde : " + backup)
