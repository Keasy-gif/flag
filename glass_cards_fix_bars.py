#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

if "/* liquid glass sur les grandes cartes" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

anchor = ".dark button:focus-visible, .dark input:focus-visible, .dark select:focus-visible{outline-color:#F4F4F6;}"
n = src.count(anchor)
if n != 1:
    print("SKIP : ancre de fin introuvable (trouvée " + str(n) + " fois) — rien touché.")
    sys.exit(0)

block = (
    "\n\n/* liquid glass sur les grandes cartes + fix barres catégories */\n"
    ".art{box-shadow:0 14px 34px rgba(11,11,12,.18), inset 0 1.5px 2px rgba(255,255,255,.4), inset 0 -16px 26px -10px rgba(0,0,0,.3) !important;}\n"
    ".cat-bar-top{display:flex !important; justify-content:space-between !important; align-items:center; font-size:11px; font-weight:700; margin-bottom:4px; opacity:.95; color:#fff;}\n"
    ".cat-bar-track{height:4px !important; background:rgba(255,255,255,.22); border-radius:99px; overflow:hidden; width:100%;}\n"
    ".cat-bar-fill{height:100% !important; background:#fff; border-radius:99px; transition:width .5s ease; display:block;}\n"
)

src = src.replace(anchor, anchor + block, 1)
backup = PATH + ".backup-glasscards-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : verre ajouté aux grandes cartes + barres de catégories réparées.")
print("Sauvegarde : " + backup)
