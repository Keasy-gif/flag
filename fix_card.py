#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

old = (
    '      <section\n'
    '        className="art grade-card rise"\n'
    '        style={{ animationDelay: ".1s", backgroundImage: `repeating-linear-gradient(90deg, rgba(255,255,255,.14) 0 1px, transparent 1px 3px), radial-gradient(circle at 30% 25%, ${grade.current.color}, transparent 60%), linear-gradient(140deg, ${grade.current.color} 0%, #1c1c1e 130%)` }}\n'
    '      >\n'
    '        <div className="grade-top">\n'
    '          <div className="grade-name">{grade.current.icon} {grade.current.name}</div>\n'
    '          <div className="grade-streak">🔥 {data.streak} j</div>\n'
    '        </div>\n'
    '        <div className="grade-bar"><div className="grade-fill" style={{ width: Math.round(grade.prog * 100) + "%" }} /></div>\n'
    '        <div className="grade-hint">\n'
    '          {grade.next ? `${grade.next.icon} ${grade.next.name} dans ${grade.next.min - data.streak} jour${grade.next.min - data.streak > 1 ? "s" : ""}` : "Grade maximum. Respect."}\n'
    '        </div>\n'
    '      </section>'
)

new = (
    '      <section\n'
    '        className="art grade-card rise"\n'
    '        style={{ animationDelay: ".1s", backgroundImage: `repeating-linear-gradient(90deg, rgba(255,255,255,.14) 0 1px, transparent 1px 3px), radial-gradient(circle at 30% 25%, ${rank.current.color}, transparent 60%), linear-gradient(140deg, ${rank.current.color} 0%, #1c1c1e 130%)` }}\n'
    '      >\n'
    '        <div className="lvl-top">\n'
    '          <div className="lvl-ring-wrap">\n'
    '            <svg viewBox="0 0 64 64" className="lvl-ring">\n'
    '              <circle cx="32" cy="32" r="27" className="lvl-ring-bg" />\n'
    '              <circle cx="32" cy="32" r="27" className="lvl-ring-fg" strokeDasharray={`${levelInfo.prog * 169.6} 169.6`} />\n'
    '            </svg>\n'
    '            <div className="lvl-ring-icon">{rank.current.icon}</div>\n'
    '          </div>\n'
    '          <div className="lvl-mid">\n'
    '            <div className="lvl-num">Niv. {levelInfo.level}</div>\n'
    '            <div className="grade-name">{rank.current.name}</div>\n'
    '          </div>\n'
    '          <div className="grade-streak">🔥 {data.streak} j</div>\n'
    '        </div>\n'
    '        <div className="grade-hint">\n'
    '          {rank.next ? `${rank.next.icon} ${rank.next.name} au niveau ${rank.next.atLevel}` : "Rang maximum. Légende vivante."}\n'
    '        </div>\n'
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
    '        </div>\n'
    '      </section>'
)

n = src.count(old)
if n == 0:
    print("SKIP : ancre introuvable — colle-moi le contenu autour de \"grade-top\" à nouveau.")
    sys.exit(0)
if n > 1:
    print("SKIP : ancre trouvée " + str(n) + " fois (attendu 1) — trop risqué, rien touché.")
    sys.exit(0)

src = src.replace(old, new)
backup = PATH + ".backup-cardfix-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("OK : carte remplacée par la version niveau + maîtrise.")
print("Sauvegarde : " + backup)
