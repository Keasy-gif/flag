#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch FLAG : ajoute (si absent) les 5 themes de couleur + le Mode Focus.
Chaque etape est independante ; un echec n'empeche pas les autres.
Le fichier n'est reecrit QUE si au moins une etape a reussi.
Lance-le depuis la racine du repo : python3 patch_app.py
"""
import re, sys, shutil, datetime

PATH = "src/App.jsx"
src = open(PATH, encoding="utf-8").read()
original = src
report = []

def try_replace(label, old, new, expect=1):
    global src
    n = src.count(old)
    if n == 0:
        report.append("SKIP  " + label + " : ancre introuvable (deja fait ou fichier different)")
        return False
    if expect and n != expect:
        report.append("SKIP  " + label + " : ancre trouvee " + str(n) + " fois, attendu " + str(expect))
        return False
    src = src.replace(old, new)
    report.append("OK    " + label)
    return True

already_tints = "TINTS = [" in src
already_focus = "focusTask" in src

# ============================================================= COULEURS
if already_tints:
    report.append("SKIP  Couleurs : deja installees")
else:
    try_replace(
        "Couleurs - definition des 5 themes",
        "const personaOf = (id) => PERSONAS.find((p) => p.id === id) || PERSONAS[0];",
        "const personaOf = (id) => PERSONAS.find((p) => p.id === id) || PERSONAS[0];\n\n"
        "const TINTS = [\n"
        "  { id: \"flag\", name: \"Flag\", c: [\"#FF5A2E\", \"#FF2E63\", \"#B02AFF\"] },\n"
        "  { id: \"ocean\", name: \"Océan\", c: [\"#00C6FF\", \"#0072FF\", \"#5B2EFF\"] },\n"
        "  { id: \"neon\", name: \"Néon\", c: [\"#3DFFA2\", \"#00D9A5\", \"#00A9CC\"] },\n"
        "  { id: \"or\", name: \"Or\", c: [\"#FFD24A\", \"#FF9E2C\", \"#FF4E2E\"] },\n"
        "  { id: \"ultra\", name: \"Ultra\", c: [\"#C32EFF\", \"#7B2EFF\", \"#2E5BFF\"] },\n"
        "];\n"
        "const tintOf = (id) => TINTS.find((t) => t.id === id) || TINTS[0];",
    )

    try_replace(
        "Couleurs - variable tint dans le composant",
        "const persona = personaOf(data.persona);",
        "const persona = personaOf(data.persona);\n"
        "  const tint = tintOf(data.tint);\n"
        "  const tintStyle = { \"--a1\": tint.c[0], \"--a2\": tint.c[1], \"--a3\": tint.c[2] };",
    )

    n3 = src.count('<div className={appCls}>')
    if n3 >= 1:
        src = src.replace('<div className={appCls}>', '<div className={appCls} style={tintStyle}>')
        report.append("OK    Couleurs - style applique sur " + str(n3) + " ecran(s)")
    else:
        report.append("SKIP  Couleurs - balise racine introuvable")

    try_replace(
        "Couleurs - selecteur dans les Parametres",
        '              <div className="set-list">',
        '              <div className="set-persona">\n'
        '                <div className="label">Couleur</div>\n'
        '                <div className="chip-row">\n'
        '                  {TINTS.map((t) => (\n'
        '                    <button\n'
        '                      key={t.id}\n'
        '                      className={"swatch" + (tint.id === t.id ? " swatch-on" : "")}\n'
        '                      style={{ background: `linear-gradient(135deg, ${t.c[0]}, ${t.c[1]}, ${t.c[2]})` }}\n'
        '                      onClick={() => persist({ ...data, tint: t.id })}\n'
        '                      aria-label={t.name}\n'
        '                      title={t.name}\n'
        '                    />\n'
        '                  ))}\n'
        '                </div>\n'
        '              </div>\n'
        '\n'
        '              <div className="set-list">',
    )

    try_replace(
        "Couleurs - variables CSS racine",
        ":root{\n  --bg:#E9EAEC;",
        ":root{\n  --a1:#FF5A2E; --a2:#FF2E63; --a3:#B02AFF;\n  --bg:#E9EAEC;",
    )

    def mix(var):
        def f(m):
            pct = round(float(m.group(1)) * 100)
            return "color-mix(in srgb, var(" + var + ") " + str(pct) + "%, transparent)"
        return f
    before = src
    src = re.sub(r"rgba\(255,\s*90,\s*46,\s*(0?\.[0-9]+)\)", mix("--a1"), src)
    src = re.sub(r"rgba\(255,\s*46,\s*99,\s*(0?\.[0-9]+)\)", mix("--a2"), src)
    src = re.sub(r"rgba\(158,\s*42,\s*255,\s*(0?\.[0-9]+)\)", mix("--a3"), src)
    report.append("OK    Couleurs - halos convertis" if src != before else "SKIP  Couleurs - aucun halo a convertir")

    KEEP = "___KEEP_TINT_VARS___"
    if "const css = `" in src:
        head, cssblock = src.split("const css = `", 1)
        cssblock = cssblock.replace("--a1:#FF5A2E; --a2:#FF2E63; --a3:#B02AFF;", KEEP)
        for lit, var in [("#FF5A2E", "var(--a1)"), ("#FF2E63", "var(--a2)"), ("#B02AFF", "var(--a3)")]:
            cssblock = cssblock.replace(lit, var)
        cssblock = cssblock.replace(KEEP, "--a1:#FF5A2E; --a2:#FF2E63; --a3:#B02AFF;")
        src = head + "const css = `" + cssblock
        report.append("OK    Couleurs - litteraux CSS convertis")

    src = src.replace("background:#FF5A2E; top:-140px;", "background:var(--a1); top:-140px;")
    src = src.replace("background:#B02AFF; left:-140px;", "background:var(--a3); left:-140px;")
    src = src.replace("background:#FF2E63; bottom:4%;", "background:var(--a2); bottom:4%;")
    src = src.replace(
        "radial-gradient(circle at 55% 40%, #6A14E8 0%, #9E2AFF 24%, rgba(158,42,255,.35) 48%, transparent 66%),",
        "radial-gradient(circle at 55% 40%, color-mix(in srgb, var(--a3) 80%, #000) 0%, var(--a3) 24%, color-mix(in srgb, var(--a3) 35%, transparent) 48%, transparent 66%),",
    )

    try_replace(
        "Couleurs - style des pastilles",
        '/* persona */\n.set-persona{display:flex; flex-direction:column; gap:9px;}',
        '/* persona */\n.set-persona{display:flex; flex-direction:column; gap:9px;}\n'
        '.swatch{width:38px; height:38px; border-radius:50%; border:none; cursor:pointer; box-shadow:inset 0 0 0 2px rgba(255,255,255,.25); transition:transform .12s;}\n'
        '.swatch:active{transform:scale(.9);}\n'
        '.swatch-on{box-shadow:0 0 0 2.5px var(--card), 0 0 0 5px var(--ink);}',
    )

# ============================================================= MODE FOCUS
if already_focus:
    report.append("SKIP  Mode Focus : deja installe")
else:
    focus_state_added = False
    for anchor in [
        "const [showGrades, setShowGrades] = useState(false);",
        "const [wall, setWall] = useState(false);",
    ]:
        if anchor in src and not focus_state_added:
            src = src.replace(anchor, anchor + "\n  const [focusTask, setFocusTask] = useState(null);", 1)
            report.append("OK    Mode Focus - etat ajoute")
            focus_state_added = True
            break
    if not focus_state_added:
        report.append("SKIP  Mode Focus - aucune ancre d'etat trouvee")

    try_replace(
        "Mode Focus - ouverture au lancement du chrono",
        "if (starting) {\n      const payload = {",
        "if (starting) {\n      setFocusTask(id);\n      const payload = {",
    )

    try_replace(
        "Mode Focus - ecran allume (wake lock)",
        "  const startVoice = () => {",
        "  useEffect(() => {\n"
        "    let lock = null;\n"
        "    if (focusTask && navigator.wakeLock) {\n"
        "      navigator.wakeLock.request(\"screen\").then((l) => { lock = l; }).catch(() => {});\n"
        "    }\n"
        "    return () => { if (lock && lock.release) lock.release().catch(() => {}); };\n"
        "  }, [focusTask]);\n"
        "\n"
        "  const startVoice = () => {",
    )

    try_replace(
        "Mode Focus - chrono cliquable (reouvre le plein ecran)",
        '                {t.startedAt\n'
        '                  ? <span className="live-time">● {fmtElapsed(Date.now() - t.startedAt)} / {t.minutes} min</span>\n'
        '                  : `${t.cat} · ${t.minutes} min`}',
        '                {t.startedAt\n'
        '                  ? <button className="live-time live-open" onClick={() => setFocusTask(t.id)}>● {fmtElapsed(Date.now() - t.startedAt)} / {t.minutes} min · plein écran ⤢</button>\n'
        '                  : `${t.cat} · ${t.minutes} min`}',
    )

    focus_render_added = False
    for anchor in ["      {/* tous les rangs */}", "      {/* montée en grade */}", "      {/* montee en grade */}"]:
        if anchor in src and not focus_render_added:
            block = (
                '      {/* mode focus */}\n'
                '      {focusTask && (() => {\n'
                '        const t = data.tasks.find((z) => z.id === focusTask);\n'
                '        if (!t || t.status === "verified" || !t.startedAt) return null;\n'
                '        const el = Date.now() - t.startedAt;\n'
                '        const prog = Math.min(1, el / (t.minutes * 60000));\n'
                '        return (\n'
                '          <div className="focus">\n'
                '            <button className="circle-btn focus-close" onClick={() => setFocusTask(null)} aria-label="Réduire">⌄</button>\n'
                '            <div className="focus-emoji">{t.icon || iconFor(t.title, t.cat)}</div>\n'
                '            <div className="focus-title">{t.title}</div>\n'
                '            <div className="focus-time">{fmtElapsed(el)}</div>\n'
                '            <div className="focus-bar"><div className="focus-fill" style={{ width: Math.round(prog * 100) + "%" }} /></div>\n'
                '            <div className="label center">{Math.round(prog * 100)}% des {t.minutes} min{prog >= 1 ? " — objectif atteint, flag !" : ""}</div>\n'
                '            <div className="focus-actions">\n'
                '              <button className="btn-ghost" onClick={() => { toggleTimer(t.id); setFocusTask(null); }}>Arrêter</button>\n'
                '              <button className="btn-black" onClick={() => { setFocusTask(null); startVerif(t); }}>Flag ✓</button>\n'
                '            </div>\n'
                '            <div className="label center focus-hint">Reste ici. Chaque minute compte pour de vrai.</div>\n'
                '          </div>\n'
                '        );\n'
                '      })()}\n'
                '\n'
            )
            src = src.replace(anchor, block + anchor, 1)
            report.append("OK    Mode Focus - ecran plein ecran ajoute")
            focus_render_added = True
            break
    if not focus_render_added:
        report.append("SKIP  Mode Focus - aucune ancre de rendu trouvee (ecran NON ajoute)")

    css_anchor = '/* pastilles couleur */' if '/* pastilles couleur */' in src else '/* persona */'
    focus_css = (
        '/* mode focus */\n'
        '.focus{\n'
        '  position:fixed; inset:0; z-index:95; display:flex; flex-direction:column;\n'
        '  align-items:center; justify-content:center; gap:16px; padding:24px;\n'
        '  background:\n'
        '    radial-gradient(700px 420px at 50% -10%, color-mix(in srgb, var(--a1) 22%, transparent), transparent 65%),\n'
        '    radial-gradient(600px 400px at 50% 110%, color-mix(in srgb, var(--a3) 18%, transparent), transparent 60%),\n'
        '    var(--bg);\n'
        '  animation:focusIn .3s cubic-bezier(.2,.8,.3,1) both;\n'
        '}\n'
        '@keyframes focusIn{from{opacity:0; transform:scale(1.04);}}\n'
        '@media (prefers-reduced-motion: reduce){ .focus{animation:none;} }\n'
        '.focus-close{position:absolute; top:20px; left:18px; background:var(--fill); color:var(--ink); width:42px; height:42px; font-size:18px;}\n'
        '.focus-emoji{font-size:46px;}\n'
        '.focus-title{font-size:20px; font-weight:800; letter-spacing:-.5px; text-align:center; max-width:88%;}\n'
        '.focus-time{font-size:72px; font-weight:900; letter-spacing:-3px; line-height:1; font-variant-numeric:tabular-nums;}\n'
        '.focus-bar{width:min(320px, 78%); height:5px; background:var(--fill); border-radius:99px; overflow:hidden;}\n'
        '.focus-fill{height:100%; background:linear-gradient(90deg, var(--a1), var(--a2)); border-radius:99px; transition:width 1s linear;}\n'
        '.focus-actions{display:flex; gap:10px; width:min(320px, 78%); margin-top:8px;}\n'
        '.focus-hint{position:absolute; bottom:34px; left:0; right:0; opacity:.7;}\n'
        '.live-open{background:none; border:none; cursor:pointer; font:inherit; padding:0; text-align:left;}\n'
        '\n'
    )
    try_replace("Mode Focus - styles CSS", css_anchor, focus_css + css_anchor)

print("\n".join(report))

if src == original:
    print("\nRien n'a change - fichier non modifie.")
    sys.exit(0)

backup = PATH + ".backup-" + datetime.datetime.now().strftime("%H%M%S")
shutil.copy(PATH, backup)
open(PATH, "w", encoding="utf-8").write(src)
print("\nFichier mis a jour. Sauvegarde de l'ancien : " + backup)
