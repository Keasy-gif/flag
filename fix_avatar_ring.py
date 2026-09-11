#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src

if "rank-avatar-wrap" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

old_jsx = (
    '      <section\n'
    '        className="art grade-card rise"\n'
    '        style={{ animationDelay: ".1s", backgroundImage: `repeating-linear-gradient(90deg, rgba(255,255,255,.14) 0 1px, transparent 1px 3px), radial-gradient(circle at 30% 25%, ${rank.current.color}, transparent 60%), linear-gradient(140deg, ${rank.current.color} 0%, #1c1c1e 130%)` }}\n'
    '      >\n'
    '        <div className="lvl-top">\n'
    '          <div className="lvl-ring-wrap">\n'
    '            <svg viewBox="0 0 64 64" width="64" height="64" className="lvl-ring">\n'
    '              <circle cx="32" cy="32" r="27" fill="none" stroke="rgba(255,255,255,.22)" strokeWidth="5" className="lvl-ring-bg" />\n'
    '              <circle cx="32" cy="32" r="27" fill="none" stroke="#fff" strokeWidth="5" strokeLinecap="round" strokeDasharray={`${levelInfo.prog * 169.6} 169.6`} className="lvl-ring-fg" />\n'
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

new_jsx = (
    '      <section className="art art-blue rank-card rise" style={{ animationDelay: ".1s" }}>\n'
    '        <div className="rank-top">\n'
    '          <div className="rank-avatar-wrap">\n'
    '            <svg viewBox="0 0 96 96" width="96" height="96" className="rank-ring">\n'
    '              <defs>\n'
    '                <linearGradient id="rankRingGrad" x1="0" y1="0" x2="1" y2="1">\n'
    '                  <stop offset="0" style={{ stopColor: "var(--a1)" }} />\n'
    '                  <stop offset="1" style={{ stopColor: "var(--a3)" }} />\n'
    '                </linearGradient>\n'
    '              </defs>\n'
    '              <circle cx="48" cy="48" r="42" fill="none" stroke="rgba(255,255,255,.28)" strokeWidth="6" />\n'
    '              <circle cx="48" cy="48" r="42" fill="none" stroke="url(#rankRingGrad)" strokeWidth="6" strokeLinecap="round" strokeDasharray={`${levelInfo.prog * 263.9} 263.9`} transform="rotate(-90 48 48)" />\n'
    '            </svg>\n'
    '            <div className="rank-avatar">\n'
    '              {data.user.avatar ? <img src={data.user.avatar} alt="" /> : <Bot />}\n'
    '            </div>\n'
    '            <div className="rank-badge" style={{ background: rank.current.color }}>{rank.current.icon}</div>\n'
    '          </div>\n'
    '          <div className="rank-info">\n'
    '            <div className="rank-lvl">Niveau {levelInfo.level}</div>\n'
    '            <div className="rank-name">{rank.current.name}</div>\n'
    '            <div className="grade-streak">🔥 {data.streak} j</div>\n'
    '          </div>\n'
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

css_anchor = "/* niveau + maîtrise */"
old_css_needle = "/* niveau + maîtrise */"
new_css = (
    '/* niveau + maîtrise (v2 — avatar + anneau vif) */\n'
    '.rank-top{display:flex; align-items:center; gap:16px; margin-bottom:12px;}\n'
    '.rank-avatar-wrap{position:relative; width:96px; height:96px; flex-shrink:0;}\n'
    '.rank-ring{position:absolute; inset:0;}\n'
    '.rank-avatar{\n'
    '  position:absolute; inset:11px; border-radius:50%; overflow:hidden;\n'
    '  background:rgba(255,255,255,.16); display:flex; align-items:center; justify-content:center;\n'
    '  border:2px solid rgba(255,255,255,.25);\n'
    '}\n'
    '.rank-avatar img{width:100%; height:100%; object-fit:cover; display:block;}\n'
    '.rank-avatar .bot{width:58%; height:58%;}\n'
    '.rank-badge{\n'
    '  position:absolute; bottom:-3px; right:-3px; width:32px; height:32px; border-radius:50%;\n'
    '  display:flex; align-items:center; justify-content:center; font-size:16px;\n'
    '  border:3px solid #1c1c1e; box-shadow:0 2px 10px rgba(0,0,0,.35);\n'
    '}\n'
    '.rank-info{flex:1; min-width:0;}\n'
    '.rank-lvl{font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; opacity:.85;}\n'
    '.rank-name{font-size:25px; font-weight:900; letter-spacing:-.8px; text-shadow:0 1px 10px rgba(0,0,0,.25); margin:2px 0 8px;}\n\n'
    '/* niveau + maîtrise */'
)

report = []
n1 = src.count(old_jsx)
if n1 == 1:
    src = src.replace(old_jsx, new_jsx)
    report.append("OK    Carte remplacée (avatar + anneau vif + badge de rang)")
else:
    report.append("SKIP  Carte : ancre trouvée " + str(n1) + " fois (attendu 1) — rien touché")

n2 = src.count(old_css_needle)
if n2 == 1:
    src = src.replace(old_css_needle, new_css)
    report.append("OK    Styles avatar/anneau/badge ajoutés")
else:
    report.append("SKIP  CSS : ancre trouvée " + str(n2) + " fois (attendu 1) — rien touché")

print("\n".join(report))

if src == original:
    print("\nRien n'a changé.")
    sys.exit(0)

backup = PATH + ".backup-avatar-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("\nFichier mis à jour. Sauvegarde : " + backup)
