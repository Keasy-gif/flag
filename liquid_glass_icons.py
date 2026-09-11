#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src
report = []

def try_replace(label, old, new, expect=1):
    global src
    n = src.count(old)
    if n == 0:
        report.append("SKIP  " + label + " : ancre introuvable")
        return False
    if expect and n != expect:
        report.append("SKIP  " + label + " : ancre trouvée " + str(n) + " fois, attendu " + str(expect))
        return False
    src = src.replace(old, new)
    report.append("OK    " + label)
    return True

if "rgi-emoji" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

# 1) JSX : emoji dans un span (pour rester au-dessus du reflet)
try_replace(
    "Icône : emoji isolé dans son propre calque",
    '                    <div className="rank-glass-icon" style={{ background: g.color + "26", borderColor: reached ? g.color : "transparent" }}>{g.icon}</div>',
    '                    <div className="rank-glass-icon" style={{ background: g.color + "26", borderColor: reached ? g.color : "transparent" }}><span className="rgi-emoji">{g.icon}</span></div>',
)

# 2) CSS : vrai traitement liquid glass (flou+saturation, reflet, ombres internes)
try_replace(
    "Icône : vrai rendu liquid glass (flou, reflet, relief)",
    '.rank-glass-icon{width:64px; height:64px; border-radius:20px; flex-shrink:0; font-size:32px; display:flex; align-items:center; justify-content:center; border:2px solid transparent;}',
    '.rank-glass-icon{\n'
    '  position:relative; overflow:hidden;\n'
    '  width:64px; height:64px; border-radius:20px; flex-shrink:0; font-size:32px;\n'
    '  display:flex; align-items:center; justify-content:center; border:2px solid transparent;\n'
    '  backdrop-filter:blur(16px) saturate(2.1);\n'
    '  -webkit-backdrop-filter:blur(16px) saturate(2.1);\n'
    '  box-shadow:\n'
    '    inset 0 1.5px 1.5px rgba(255,255,255,.65),\n'
    '    inset 0 -9px 14px -6px rgba(0,0,0,.35),\n'
    '    0 6px 16px rgba(0,0,0,.18);\n'
    '}\n'
    '.rank-glass-icon::before{\n'
    '  content:"";\n'
    '  position:absolute; top:-40%; left:-18%; width:80%; height:80%;\n'
    '  background:radial-gradient(circle, rgba(255,255,255,.65), transparent 70%);\n'
    '  pointer-events:none;\n'
    '}\n'
    '.rgi-emoji{position:relative; z-index:1; filter:drop-shadow(0 1px 2px rgba(0,0,0,.3));}',
)

print("\n".join(report))

if src == original:
    print("\nRien n'a changé.")
    sys.exit(0)

backup = PATH + ".backup-glassicons-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("\nFichier mis à jour. Sauvegarde : " + backup)
