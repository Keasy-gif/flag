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

if "showGrades" in src and "exportBlocks" in src:
    print("SKIP  déjà installé.")
    sys.exit(0)

# 1) état showGrades
try_replace(
    "État showGrades",
    "const [wall, setWall] = useState(false);",
    "const [wall, setWall] = useState(false);\n  const [showGrades, setShowGrades] = useState(false);",
)

# 2) ref pour l'import de fichier
try_replace(
    "Référence pour l'import de blocs",
    "const avatarRef = useRef(null);",
    "const avatarRef = useRef(null);\n  const importRef = useRef(null);",
)

# 3) fonctions export / import
try_replace(
    "Fonctions Partager / Importer des blocs",
    "const removeTask = (id) => persist({ ...data, tasks: data.tasks.filter((t) => t.id !== id) });",
    "const removeTask = (id) => persist({ ...data, tasks: data.tasks.filter((t) => t.id !== id) });\n\n"
    "  const exportBlocks = () => {\n"
    "    const blocks = tasks.filter((t) => t.status !== \"verified\").map((t) => ({ titre: t.title, cat: t.cat, minutes: t.minutes }));\n"
    "    if (!blocks.length) return;\n"
    "    const payload = JSON.stringify({ v: 1, from: data.user.pseudo, blocks });\n"
    "    const blob = new Blob([payload], { type: \"application/json\" });\n"
    "    const file = new File([blob], \"flag-blocs.json\", { type: \"application/json\" });\n"
    "    if (navigator.canShare && navigator.canShare({ files: [file] })) {\n"
    "      navigator.share({ files: [file], title: \"Mes blocs FLAG\" }).catch(() => {});\n"
    "    } else {\n"
    "      const url = URL.createObjectURL(blob);\n"
    "      const a = document.createElement(\"a\");\n"
    "      a.href = url; a.download = \"flag-blocs.json\"; a.click();\n"
    "      URL.revokeObjectURL(url);\n"
    "    }\n"
    "  };\n\n"
    "  const importBlocks = (e) => {\n"
    "    const file = e.target.files && e.target.files[0];\n"
    "    e.target.value = \"\";\n"
    "    if (!file) return;\n"
    "    const reader = new FileReader();\n"
    "    reader.onload = () => {\n"
    "      try {\n"
    "        const parsed = JSON.parse(reader.result);\n"
    "        const blocks = (parsed.blocks || []).slice(0, 10);\n"
    "        const added = blocks.map((b) => ({\n"
    "          id: uid(),\n"
    "          date: today,\n"
    "          title: String(b.titre || \"Bloc importé\").slice(0, 80),\n"
    "          cat: CATS.includes(b.cat) ? b.cat : \"Autre\",\n"
    "          minutes: Math.min(180, Math.max(15, Number(b.minutes) || 30)),\n"
    "          status: \"pending\",\n"
    "        }));\n"
    "        if (added.length) persist({ ...data, tasks: [...data.tasks, ...added] });\n"
    "      } catch {}\n"
    "    };\n"
    "    reader.readAsText(file);\n"
    "  };",
)

# 4) onClick sur la carte + lien "Tous les rangs"
try_replace(
    "Carte cliquable + lien Tous les rangs",
    '      <section className="art art-blue rank-card rise" style={{ animationDelay: ".1s" }}>',
    '      <section className="art art-blue rank-card rise" onClick={() => setShowGrades(true)} style={{ animationDelay: ".1s" }}>',
)
try_replace(
    "Lien Tous les rangs (fin de carte)",
    '          })}\n        </div>\n      </section>\n\n      {/* le rival */}',
    '          })}\n        </div>\n        <div className="grade-more">Tous les rangs ›</div>\n      </section>\n\n      {/* le rival */}',
)

# 5) nouvelle section + sheet, juste avant "le rival" (ancre confirmée)
try_replace(
    "Bloc Partage de blocs + Sheet Tous les rangs",
    "      {/* le rival */}",
    '      <input ref={importRef} type="file" accept="application/json" style={{ display: "none" }} onChange={importBlocks} />\n\n'
    '      <section className="card share-blocks rise" style={{ animationDelay: ".14s" }}>\n'
    '        <div className="rival-head">\n'
    '          <span className="rival-title">🔁 Partage de blocs</span>\n'
    '          <span className="label">envoie ton planning, importe celui d\'un pote</span>\n'
    '        </div>\n'
    '        <div className="row-btns">\n'
    '          <button className="btn-ghost" onClick={() => importRef.current && importRef.current.click()}>Importer</button>\n'
    '          <button className="btn-black" onClick={exportBlocks} disabled={!pending.length}>Partager mes blocs</button>\n'
    '        </div>\n'
    '      </section>\n\n'
    '      {showGrades && (\n'
    '        <div className="overlay" onClick={() => setShowGrades(false)}>\n'
    '          <div className="sheet" onClick={(e) => e.stopPropagation()}>\n'
    '            <button className="circle-btn sheet-close" onClick={() => setShowGrades(false)} aria-label="Fermer">×</button>\n'
    '            <div className="sheet-title">Les rangs</div>\n'
    '            <div className="sheet-body ranks-glass-list">\n'
    '              {RANK_LEVELS.map((g) => {\n'
    '                const reached = levelInfo.level >= g.atLevel;\n'
    '                const current = rank.current.name === g.name;\n'
    '                return (\n'
    '                  <div key={g.name} className={"rank-glass-row" + (reached ? "" : " rank-glass-locked") + (current ? " rank-glass-current" : "")} style={current ? { borderColor: g.color } : {}}>\n'
    '                    <div className="rank-glass-icon" style={{ background: g.color + "26", borderColor: reached ? g.color : "transparent" }}>{g.icon}</div>\n'
    '                    <div className="task-body">\n'
    '                      <span className="task-title" style={reached ? { color: g.color } : {}}>{g.name}</span>\n'
    '                      <span className="label">Niveau {g.atLevel}+</span>\n'
    '                    </div>\n'
    '                    {current ? <span className="gr-badge" style={{ color: g.color, borderColor: g.color }}>ACTUEL</span> : reached ? <span className="label">✓</span> : <span className="label">🔒</span>}\n'
    '                  </div>\n'
    '                );\n'
    '              })}\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '      )}\n\n'
    '      {/* le rival */}',
)

# 6) CSS — ancre bulletproof, ne dépend d'aucun marqueur interne
if "ranks-glass-list{" not in src:
    anchor = "const css = `"
    n = src.count(anchor)
    if n == 1:
        block = (
            "\n/* rangs en verre + partage de blocs */\n"
            ".grade-card{cursor:pointer;}\n"
            ".grade-more{font-size:12px; font-weight:700; margin-top:9px; opacity:.92;}\n"
            ".ranks-glass-list{display:flex; flex-direction:column; gap:10px; max-height:60vh; overflow-y:auto;}\n"
            ".rank-glass-row{display:flex; align-items:center; gap:14px; padding:12px 14px; border-radius:18px; background:var(--glass); backdrop-filter:blur(16px) saturate(1.3); -webkit-backdrop-filter:blur(16px) saturate(1.3); border:1.5px solid var(--glass-b); transition:opacity .15s;}\n"
            ".rank-glass-locked{opacity:.4;}\n"
            ".rank-glass-current{border-width:2px;}\n"
            ".rank-glass-icon{width:64px; height:64px; border-radius:20px; flex-shrink:0; font-size:32px; display:flex; align-items:center; justify-content:center; border:2px solid transparent;}\n"
            ".gr-badge{font-size:10px; font-weight:800; letter-spacing:1px; border:1.5px solid; border-radius:99px; padding:4px 9px; flex-shrink:0;}\n"
            ".share-blocks{padding:16px;}\n"
        )
        src = src.replace(anchor, anchor + block, 1)
        report.append("OK    Styles (rangs en verre + partage)")
    else:
        report.append("SKIP  CSS : ancre 'const css = `' trouvée " + str(n) + " fois")
else:
    report.append("SKIP  CSS : déjà présent")

print("\n".join(report))

if src == original:
    print("\nRien n'a changé.")
    sys.exit(0)

backup = PATH + ".backup-ranksshare-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("\nFichier mis à jour. Sauvegarde : " + backup)
