#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch FLAG : remplace le systeme de rang (base sur la streak) par un systeme
Niveau + XP base sur les MINUTES REELLEMENT PROUVEES, avec maitrise par
categorie. La streak reste affichee (badge de regularite), separee du rang.
Sans risque : chaque etape est independante, rien n'est ecrase si une ancre
ne correspond pas exactement.
Lance-le depuis la racine du repo : python3 patch_levels.py
"""
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
        report.append("SKIP  " + label + " : ancre trouvee " + str(n) + " fois, attendu " + str(expect))
        return False
    src = src.replace(old, new)
    report.append("OK    " + label)
    return True

if "levelFromXP" in src:
    print("SKIP  deja installe.")
    sys.exit(0)

# 1) fonctions Niveau/XP + rangs par niveau, juste apres gradeFor existant
try_replace(
    "Fonctions Niveau/XP + rangs par niveau",
    "const gradeFor = (streak) => {",
    "const xpForLevel = (level) => Math.round(15 * level * level);\n"
    "const levelFromXP = (totalMin) => {\n"
    "  let level = 1;\n"
    "  while (xpForLevel(level + 1) <= totalMin) level++;\n"
    "  const base = xpForLevel(level);\n"
    "  const nextNeed = xpForLevel(level + 1);\n"
    "  const prog = Math.min(1, (totalMin - base) / (nextNeed - base));\n"
    "  return { level, totalMin, base, nextNeed, prog };\n"
    "};\n"
    "const RANK_LEVELS = [\n"
    "  { atLevel: 1, name: \"Fer\", icon: \"🔩\", color: \"#8A93A6\" },\n"
    "  { atLevel: 3, name: \"Bronze\", icon: \"🥉\", color: \"#CD7F32\" },\n"
    "  { atLevel: 6, name: \"Argent\", icon: \"🥈\", color: \"#9AA6B5\" },\n"
    "  { atLevel: 10, name: \"Or\", icon: \"🥇\", color: \"#E8B33A\" },\n"
    "  { atLevel: 15, name: \"Platine\", icon: \"💠\", color: \"#23C4A9\" },\n"
    "  { atLevel: 21, name: \"Diamant\", icon: \"💎\", color: \"#2FA6E8\" },\n"
    "  { atLevel: 31, name: \"Ascendant\", icon: \"🔮\", color: \"#8B4CE8\" },\n"
    "  { atLevel: 46, name: \"Immortel\", icon: \"⚡\", color: \"#E83A5C\" },\n"
    "  { atLevel: 66, name: \"Radiant\", icon: \"👑\", color: \"#E8A13A\" },\n"
    "];\n"
    "const rankForLevel = (level) => {\n"
    "  let r = RANK_LEVELS[0];\n"
    "  for (const x of RANK_LEVELS) if (level >= x.atLevel) r = x;\n"
    "  const next = RANK_LEVELS[RANK_LEVELS.indexOf(r) + 1] || null;\n"
    "  return { current: r, next };\n"
    "};\n"
    "const gradeFor = (streak) => {",
)

# 2) valeurs derivees dans le composant, juste apres la ligne grade existante
try_replace(
    "Calcul du niveau, du rang et de la maitrise par categorie",
    "const grade = gradeFor(data.streak);",
    "const grade = gradeFor(data.streak);\n"
    "  const allVerified = data.tasks.filter((t) => t.status === \"verified\");\n"
    "  const totalMinutesAll = allVerified.reduce((s, t) => s + (t.minutes || 0), 0);\n"
    "  const levelInfo = levelFromXP(totalMinutesAll);\n"
    "  const rank = rankForLevel(levelInfo.level);\n"
    "  const catXP = {};\n"
    "  allVerified.forEach((t) => { catXP[t.cat] = (catXP[t.cat] || 0) + (t.minutes || 0); });",
)

# 3) remplace la carte de rang par la version niveau + anneau + maitrise
try_replace(
    "Nouvelle carte : anneau de niveau + maîtrise par catégorie",
    '      <section\n'
    '        className="art grade-card rise"\n'
    '        onClick={() => setShowGrades(true)}\n'
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
    '        <div className="grade-more">Tous les rangs ›</div>\n'
    '      </section>',
    #
    '      <section\n'
    '        className="art grade-card rise"\n'
    '        onClick={() => setShowGrades(true)}\n'
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
    '        <div className="grade-more">Tous les rangs ›</div>\n'
    '      </section>',
)

# 4) sheet "tous les rangs" : bascule streak -> niveau
try_replace(
    "Sheet « tous les rangs » basée sur les niveaux",
    '              {GRADES.map((g) => {\n'
    '                const reached = data.streak >= g.min;\n'
    '                const current = grade.current.name === g.name;\n'
    '                return (\n'
    '                  <div key={g.name} className={"grade-row2" + (reached ? "" : " gr-locked")} style={current ? { borderColor: g.color, background: g.color + "14" } : {}}>\n'
    '                    <span className="gr-icon" style={{ background: g.color + "22", border: "1px solid " + (reached ? g.color : "transparent") }}>{g.icon}</span>\n'
    '                    <span className="task-body">\n'
    '                      <span className="task-title" style={reached ? { color: g.color } : {}}>{g.name}</span>\n'
    '                      <span className="label">{g.min === 0 ? "Départ" : `${g.min} jour${g.min > 1 ? "s" : ""} de régularité`}</span>\n'
    '                    </span>\n'
    '                    {current ? <span className="gr-badge" style={{ color: g.color, borderColor: g.color }}>ACTUEL</span> : reached ? <span className="label">✓</span> : <span className="label">🔒</span>}\n'
    '                  </div>\n'
    '                );\n'
    '              })}',
    #
    '              {RANK_LEVELS.map((g) => {\n'
    '                const reached = levelInfo.level >= g.atLevel;\n'
    '                const current = rank.current.name === g.name;\n'
    '                return (\n'
    '                  <div key={g.name} className={"grade-row2" + (reached ? "" : " gr-locked")} style={current ? { borderColor: g.color, background: g.color + "14" } : {}}>\n'
    '                    <span className="gr-icon" style={{ background: g.color + "22", border: "1px solid " + (reached ? g.color : "transparent") }}>{g.icon}</span>\n'
    '                    <span className="task-body">\n'
    '                      <span className="task-title" style={reached ? { color: g.color } : {}}>{g.name}</span>\n'
    '                      <span className="label">Niveau {g.atLevel}+</span>\n'
    '                    </span>\n'
    '                    {current ? <span className="gr-badge" style={{ color: g.color, borderColor: g.color }}>ACTUEL</span> : reached ? <span className="label">✓</span> : <span className="label">🔒</span>}\n'
    '                  </div>\n'
    '                );\n'
    '              })}',
)

# 5) déclenchement de la fête de montée de rang : basé sur le niveau, pas la streak
try_replace(
    "Montée de rang déclenchée par le niveau",
    "    if (verdict.valide) {\n"
    "      const before = gradeFor(data.streak).current;\n"
    "      let { streak, lastDay } = data;\n"
    "      if (lastDay !== today) {\n"
    "        streak = lastDay === yesterdayKey() ? streak + 1 : 1;\n"
    "        lastDay = today;\n"
    "      }\n"
    "      const after = gradeFor(streak).current;\n"
    "      persist({\n"
    "        ...data,\n"
    "        streak,\n"
    "        lastDay,\n"
    "        totalVerified: (data.totalVerified || 0) + 1,\n"
    "        tasks: data.tasks.map((t) =>\n"
    "          t.id === verif.taskId ? { ...t, status: \"verified\", at: nowHM(), motif: verdict.motif, thumb: verif.thumb, proof: verif.mid, startedAt: null } : t\n"
    "        ),\n"
    "      });\n"
    "      if (after.name !== before.name) setTimeout(() => setGradeUp(after), 600);\n"
    "      if (data.uid) window.storage.delete(\"live:\" + data.uid, true).catch(() => {});\n"
    "    } else {",
    #
    "    if (verdict.valide) {\n"
    "      const beforeRank = rank.current;\n"
    "      let { streak, lastDay } = data;\n"
    "      if (lastDay !== today) {\n"
    "        streak = lastDay === yesterdayKey() ? streak + 1 : 1;\n"
    "        lastDay = today;\n"
    "      }\n"
    "      const newTasks = data.tasks.map((t) =>\n"
    "        t.id === verif.taskId ? { ...t, status: \"verified\", at: nowHM(), motif: verdict.motif, thumb: verif.thumb, proof: verif.mid, startedAt: null } : t\n"
    "      );\n"
    "      const newTotalMin = newTasks.filter((t) => t.status === \"verified\").reduce((s, t) => s + (t.minutes || 0), 0);\n"
    "      const afterRank = rankForLevel(levelFromXP(newTotalMin).level).current;\n"
    "      persist({\n"
    "        ...data,\n"
    "        streak,\n"
    "        lastDay,\n"
    "        totalVerified: (data.totalVerified || 0) + 1,\n"
    "        tasks: newTasks,\n"
    "      });\n"
    "      if (afterRank.name !== beforeRank.name) setTimeout(() => setGradeUp(afterRank), 600);\n"
    "      if (data.uid) window.storage.delete(\"live:\" + data.uid, true).catch(() => {});\n"
    "    } else {",
)

# 6) styles : anneau de niveau + barres de maîtrise
try_replace(
    "Styles de l'anneau de niveau et des barres de maîtrise",
    '/* tous les rangs */\n.grade-card{cursor:pointer;}',
    '/* niveau + maîtrise */\n'
    '.lvl-top{display:flex; align-items:center; gap:14px; margin-bottom:12px;}\n'
    '.lvl-ring-wrap{position:relative; width:64px; height:64px; flex-shrink:0;}\n'
    '.lvl-ring{width:64px; height:64px; transform:rotate(-90deg);}\n'
    '.lvl-ring circle{fill:none; stroke-width:5; stroke-linecap:round;}\n'
    '.lvl-ring-bg{stroke:rgba(255,255,255,.22);}\n'
    '.lvl-ring-fg{stroke:#fff; transition:stroke-dasharray .5s ease; filter:drop-shadow(0 0 4px rgba(255,255,255,.5));}\n'
    '.lvl-ring-icon{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:24px;}\n'
    '.lvl-mid{flex:1; min-width:0;}\n'
    '.lvl-num{font-size:12px; font-weight:800; letter-spacing:1px; opacity:.9; text-transform:uppercase;}\n'
    '.cat-bars{display:flex; flex-direction:column; gap:8px; margin-top:12px;}\n'
    '.cat-bar-top{display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px; opacity:.95;}\n'
    '.cat-bar-track{height:4px; background:rgba(255,255,255,.22); border-radius:99px; overflow:hidden;}\n'
    '.cat-bar-fill{height:100%; background:#fff; border-radius:99px; transition:width .5s ease;}\n'
    '\n'
    '/* tous les rangs */\n.grade-card{cursor:pointer;}',
)

print("\n".join(report))

if src == original:
    print("\nRien n'a change - fichier non modifie.")
    sys.exit(0)

backup = PATH + ".backup-lvl-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("\nFichier mis a jour. Sauvegarde : " + backup)
