#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

if "rank-avatar-wrap{" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

anchor = "const css = `"
n = src.count(anchor)
if n != 1:
    print("SKIP : ancre 'const css = `' trouvée " + str(n) + " fois (attendu 1) — rien touché.")
    sys.exit(0)

block = (
    "\n/* niveau + maîtrise (v2) */\n"
    ".cat-bars{display:flex; flex-direction:column; gap:8px; margin-top:12px;}\n"
    ".cat-bar-top{display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px; opacity:.95;}\n"
    ".cat-bar-track{height:4px; background:rgba(255,255,255,.22); border-radius:99px; overflow:hidden;}\n"
    ".cat-bar-fill{height:100%; background:#fff; border-radius:99px; transition:width .5s ease;}\n"
    ".rank-top{display:flex; align-items:center; gap:16px; margin-bottom:12px;}\n"
    ".rank-avatar-wrap{position:relative; width:96px; height:96px; flex-shrink:0;}\n"
    ".rank-ring{position:absolute; inset:0;}\n"
    ".rank-avatar{position:absolute; inset:11px; border-radius:50%; overflow:hidden; background:rgba(255,255,255,.16); display:flex; align-items:center; justify-content:center; border:2px solid rgba(255,255,255,.25);}\n"
    ".rank-avatar img{width:100%; height:100%; object-fit:cover; display:block;}\n"
    ".rank-avatar .bot{width:58%; height:58%;}\n"
    ".rank-badge{position:absolute; bottom:-3px; right:-3px; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px; border:3px solid #1c1c1e; box-shadow:0 2px 10px rgba(0,0,0,.35);}\n"
    ".rank-info{flex:1; min-width:0;}\n"
    ".rank-lvl{font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; opacity:.85;}\n"
    ".rank-name{font-size:25px; font-weight:900; letter-spacing:-.8px; text-shadow:0 1px 10px rgba(0,0,0,.25); margin:2px 0 8px;}\n"
)

src = src.replace(anchor, anchor + block, 1)
backup = PATH + ".backup-cssfinal-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : styles carte niveau + maîtrise insérés.")
print("Sauvegarde : " + backup)
