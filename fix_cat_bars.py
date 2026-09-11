#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

old = (
    '        <div className="cat-bars">\n'
    '          {CATS.map((c) => {\n'
    '            const m = catXP[c.id] || 0;\n'
    '            const li = levelFromXP(m);\n'
    '            return (\n'
    '              <div key={c.id} className="cat-bar">\n'
    '                <div className="cat-bar-top"><span>{c.icon} {c.id}</span><span>Niv.{li.level}</span></div>\n'
    '                <div className="cat-bar-track"><div className="cat-bar-fill" style={{ width: Math.round(li.prog * 100) + "%" }} /></div>\n'
    '              </div>\n'
    '            );\n'
    '          })}\n'
    '        </div>'
)
new = (
    '        <div className="cat-bars">\n'
    '          {CATS.map((c) => {\n'
    '            const catIcons = { "Études": "📘", "Sport": "🏋️", "Autre": "⚡" };\n'
    '            const m = catXP[c] || 0;\n'
    '            const li = levelFromXP(m);\n'
    '            return (\n'
    '              <div key={c} className="cat-bar">\n'
    '                <div className="cat-bar-top"><span>{catIcons[c] || "⚡"} {c}</span><span>Niv.{li.level}</span></div>\n'
    '                <div className="cat-bar-track"><div className="cat-bar-fill" style={{ width: Math.round(li.prog * 100) + "%" }} /></div>\n'
    '              </div>\n'
    '            );\n'
    '          })}\n'
    '        </div>'
)

n = src.count(old)
if n == 0:
    print("SKIP : ancre introuvable.")
    sys.exit(0)
if n > 1:
    print("SKIP : ancre trouvée " + str(n) + " fois, trop risqué.")
    sys.exit(0)

src = src.replace(old, new)
backup = PATH + ".backup-catbars-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : barres de catégories réparées (Études/Sport/Autre affichés).")
print("Sauvegarde : " + backup)
