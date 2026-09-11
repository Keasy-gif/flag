#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

old = (
    '            <svg viewBox="0 0 64 64" className="lvl-ring">\n'
    '              <circle cx="32" cy="32" r="27" className="lvl-ring-bg" />\n'
    '              <circle cx="32" cy="32" r="27" className="lvl-ring-fg" strokeDasharray={`${levelInfo.prog * 169.6} 169.6`} />\n'
    '            </svg>'
)
new = (
    '            <svg viewBox="0 0 64 64" width="64" height="64" className="lvl-ring">\n'
    '              <circle cx="32" cy="32" r="27" fill="none" stroke="rgba(255,255,255,.22)" strokeWidth="5" className="lvl-ring-bg" />\n'
    '              <circle cx="32" cy="32" r="27" fill="none" stroke="#fff" strokeWidth="5" strokeLinecap="round" strokeDasharray={`${levelInfo.prog * 169.6} 169.6`} className="lvl-ring-fg" />\n'
    '            </svg>'
)

n = src.count(old)
if n == 0:
    print("SKIP : ancre introuvable — colle-moi ce que donne : grep -n \"lvl-ring\" src/App.jsx")
    sys.exit(0)
if n > 1:
    print("SKIP : ancre trouvée " + str(n) + " fois, trop risqué.")
    sys.exit(0)

src = src.replace(old, new)
backup = PATH + ".backup-ringfix-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : anneau corrigé (tailles + contours forcés en attributs SVG).")
print("Sauvegarde : " + backup)
