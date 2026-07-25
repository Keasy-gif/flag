import { useState, useEffect, useRef } from "react";

/* ===== stockage web =====
   Perso -> localStorage. Partagé (salle commune) -> mémoire locale en attendant
   le backend Supabase (phase 2) : tu te vois toi-même, les autres arrivent avec le temps réel. */
const _sharedMem = {};
const _storage = {
  async get(key, shared) {
    if (shared) {
      if (!(key in _sharedMem)) throw new Error("not_found");
      return { key, value: _sharedMem[key], shared: true };
    }
    const v = localStorage.getItem(key);
    if (v === null) throw new Error("not_found");
    return { key, value: v, shared: false };
  },
  async set(key, value, shared) {
    if (shared) { _sharedMem[key] = value; return { key, value, shared: true }; }
    localStorage.setItem(key, value);
    return { key, value, shared: false };
  },
  async delete(key, shared) {
    if (shared) { delete _sharedMem[key]; return { key, deleted: true, shared: true }; }
    localStorage.removeItem(key);
    return { key, deleted: true, shared: false };
  },
  async list(prefix, shared) {
    const keys = shared
      ? Object.keys(_sharedMem)
      : Object.keys(localStorage);
    return { keys: keys.filter((k) => k.startsWith(prefix || "")), prefix, shared: !!shared };
  },
};
if (typeof window !== "undefined") window.storage = _storage;


/* ================= helpers ================= */

const todayKey = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
const yesterdayKey = () => {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
const fmtDate = () => {
  const s = new Date().toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });
  return s.charAt(0).toUpperCase() + s.slice(1);
};
const nowHM = () => new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
const uid = () => Math.random().toString(36).slice(2, 9);
const dayKeyOf = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const greet = () => {
  const h = new Date().getHours();
  return h < 6 ? "Encore debout" : h < 12 ? "Bonjour" : h < 18 ? "Bon aprem" : "Bonsoir";
};
const fmtElapsed = (ms) => {
  const s = Math.floor(ms / 1000);
  const m = Math.floor(s / 60);
  const h = Math.floor(m / 60);
  return h > 0 ? `${h}:${String(m % 60).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}` : `${m}:${String(s % 60).padStart(2, "0")}`;
};

const GRADES = [
  { min: 0, name: "Fer", icon: "🔩", color: "#8A93A6" },
  { min: 1, name: "Bronze", icon: "🥉", color: "#CD7F32" },
  { min: 3, name: "Argent", icon: "🥈", color: "#9AA6B5" },
  { min: 7, name: "Or", icon: "🥇", color: "#E8B33A" },
  { min: 14, name: "Platine", icon: "💠", color: "#23C4A9" },
  { min: 30, name: "Diamant", icon: "💎", color: "#2FA6E8" },
  { min: 90, name: "Ascendant", icon: "🔮", color: "#8B4CE8" },
  { min: 180, name: "Immortel", icon: "⚡", color: "#E83A5C" },
  { min: 365, name: "Radiant", icon: "👑", color: "#E8A13A" },
];
const gradeFor = (streak) => {
  let g = GRADES[0];
  for (const x of GRADES) if (streak >= x.min) g = x;
  const next = GRADES[GRADES.indexOf(g) + 1] || null;
  const prog = next ? Math.min(1, (streak - g.min) / (next.min - g.min)) : 1;
  return { current: g, next, prog };
};

const ICON_MAP = [
  [/math|alg[eè]bre|analyse|int[eé]grale|proba|g[eé]om/i, "📐"],
  [/physique|m[eé]ca|quantique/i, "⚛️"],
  [/chimie/i, "🧪"],
  [/anglais|espagnol|allemand|langue|toefl|toeic/i, "🗣️"],
  [/lecture|lire|livre|bouquin/i, "📖"],
  [/code|dev|app|python|projet|site|github/i, "💻"],
  [/salle|muscu|gym|fitness|pompes|force/i, "🏋️"],
  [/course|courir|running|cardio|footing/i, "🏃"],
  [/foot(?!ing)|match/i, "⚽"],
  [/natation|piscine|nager/i, "🏊"],
  [/v[eé]lo|cyclisme/i, "🚴"],
  [/logement|appart|maison|immo|bail|caution/i, "🏠"],
  [/contact|appel|t[eé]l[eé]phone|rdv|rendez/i, "📞"],
  [/mail|email|courrier|lettre|candidature|cv/i, "✉️"],
  [/admin|dossier|papier|formulaire|inscription/i, "📋"],
  [/cuisine|repas|manger|meal/i, "🍳"],
  [/m[eé]nage|rangement|nettoyer|lessive/i, "🧹"],
  [/courses|achat|shopping/i, "🛒"],
  [/finance|budget|banque|trading|bourse|invest/i, "📈"],
  [/r[eé]vision|annale|exam|fiche|partiel|concours|qcm/i, "📝"],
  [/cours|amphi|td|tp/i, "🎓"],
  [/musique|guitare|piano|chant/i, "🎸"],
  [/m[eé]ditation|yoga|respiration/i, "🧘"],
  [/dessin|peinture|art/i, "🎨"],
];
const iconFor = (title, cat) => {
  for (const [re, ic] of ICON_MAP) if (re.test(title)) return ic;
  return cat === "Études" ? "📘" : cat === "Sport" ? "🏋️" : "⚡";
};

const PERSONAS = [
  { id: "cash", name: "Cash", emoji: "😤", style: "direct, tutoiement, un peu cash, vanne légère autorisée" },
  { id: "sergent", name: "Sergent", emoji: "🪖", style: "sergent instructeur : sec, exigeant, phrases courtes, quelques MAJUSCULES, zéro excuse tolérée, mais jamais insultant ni humiliant" },
  { id: "zen", name: "Zen", emoji: "🧘", style: "calme, posé, bienveillant, encourageant sans mollesse, tutoiement" },
  { id: "frero", name: "Fréro", emoji: "🤝", style: "grand frère : chaleureux, argot léger, taquin, motivant, tutoiement" },
];
const personaOf = (id) => PERSONAS.find((p) => p.id === id) || PERSONAS[0];

const TEMPLATES = [
  { id: "revisions", icon: "📐", name: "Révisions intensives", prompt: "Programme du jour : révisions intensives type prépa/exam. Je veux 4 à 5 blocs d'études sérieux (annales, exos, fiches, relecture) avec des durées réalistes et de la variété." },
  { id: "equilibre", icon: "☀️", name: "Journée équilibrée", prompt: "Programme du jour : journée équilibrée. 2-3 blocs d'études, 1 bloc de sport, et 1 bloc perso (lecture, projet, admin)." },
  { id: "deepwork", icon: "🧠", name: "Deep work", prompt: "Programme du jour : deep work. 2 ou 3 blocs longs (90-180 min) de travail profond sur un seul sujet chacun, avec une vraie coupure entre les deux." },
  { id: "sport", icon: "🏋️", name: "Remise en forme", prompt: "Programme du jour : priorité au sport. 1 vraie séance de sport + 1 bloc mobilité, et 2 blocs d'études ou de travail autour." },
  { id: "veille", icon: "📝", name: "Veille d'exam", prompt: "Programme du jour : veille d'examen. Blocs de révision courts et ciblés, en finissant tôt pour dormir." },
  { id: "code", icon: "💻", name: "Projet perso", prompt: "Programme du jour : avancer sur un projet perso de code/app. 2-3 blocs de dev avec des objectifs concrets par bloc." },
];

function processPhoto(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        const make = (maxSide, q) => {
          const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
          const c = document.createElement("canvas");
          c.width = Math.round(img.width * scale);
          c.height = Math.round(img.height * scale);
          c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
          return c.toDataURL("image/jpeg", q);
        };
        resolve({ b64: make(1000, 0.7).split(",")[1], preview: make(1000, 0.7), thumb: make(140, 0.6), mid: make(480, 0.6) });
      };
      img.onerror = () => reject(new Error("image"));
      img.src = reader.result;
    };
    reader.onerror = () => reject(new Error("read"));
    reader.readAsDataURL(file);
  });
}

async function callClaude(content) {
  const response = await fetch("/api/claude", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: [{ role: "user", content }] }),
  });
  const data = await response.json();
  const text = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
  return JSON.parse(text.replace(/```json|```/g, "").trim());
}

const verifyWithAI = (task, b64, style) =>
  callClaude([
    { type: "image", source: { type: "base64", media_type: "image/jpeg", data: b64 } },
    {
      type: "text",
      text: `Tu es le vérificateur impitoyable mais juste de FLAG, une app d'accountability.
Tâche déclarée : "${task.title}" (${task.cat}, ${task.minutes} min).
Juge si la photo est une preuve plausible que la personne fait cette activité MAINTENANT. Hors sujet, illisible ou sans rapport = refus.
Réponds UNIQUEMENT en JSON : {"valide": true|false, "confiance": 0-100, "motif": "une phrase courte en français, ton : ${style}"}`,
    },
  ]);

const planWithAI = (message, existing, style) =>
  callClaude(`Tu es le coach de FLAG, une app d'accountability où chaque bloc planifié doit être prouvé par une photo.
L'utilisateur te décrit sa journée, ses objectifs ou ses contraintes. Tu construis un planning de blocs concrets et réalistes.

Message de l'utilisateur : "${message}"
Blocs déjà planifiés aujourd'hui (ne les duplique pas) : ${existing.length ? existing.map((t) => `${t.title} (${t.minutes} min)`).join(", ") : "aucun"}

Règles : 2 à 6 blocs, 15 à 180 min chacun, titres précis et actionnables, catégorie parmi Études / Sport / Autre. Prévois des pauses implicites. Ton : ${style}.

Réponds UNIQUEMENT en JSON, sans markdown :
{"message": "1 ou 2 phrases de coach", "blocs": [{"titre": "...", "cat": "Études", "minutes": 90, "emoji": "un seul emoji représentant ce bloc"}]}`);

const bilanWithAI = (tasks, streak, grade, style) =>
  callClaude(`Tu es le coach de FLAG. Fais le bilan de la journée.

Blocs du jour :
${tasks.map((t) => `- ${t.title} (${t.cat}, ${t.minutes} min) : ${t.status === "verified" ? "PROUVÉ à " + t.at : "NON PROUVÉ"}`).join("\n")}
Streak : ${streak} jour(s). Grade : ${grade}.

Ton : ${style}. Honnête : félicite ce qui est prouvé, pointe ce qui a été esquivé. Finis par un encouragement concret pour demain, pas de motivation creuse.

Réponds UNIQUEMENT en JSON, sans markdown :
{"resume": "2 phrases max", "encouragement": "1 ou 2 phrases concrètes pour demain"}`);

/* ================= composant ================= */

const CATS = ["Études", "Sport", "Autre"];

const Bot = () => (
  <svg viewBox="0 0 40 40" className="bot" aria-label="Coach">
    <line x1="20" y1="5" x2="20" y2="10" className="bot-ant" />
    <circle cx="20" cy="4" r="2" className="bot-tip" />
    <rect x="8" y="10" width="24" height="20" rx="7" className="bot-head" />
    <rect x="14" y="17" width="4" height="6" rx="2" className="bot-eye" />
    <rect x="22" y="17" width="4" height="6" rx="2" className="bot-eye" />
  </svg>
);

export default function Flag() {
  const [data, setData] = useState({ tasks: [], streak: 0, lastDay: null, totalVerified: 0, bilans: {} });
  const [loaded, setLoaded] = useState(false);
  const [adding, setAdding] = useState(false);
  const [nTitle, setNTitle] = useState("");
  const [nCat, setNCat] = useState("Études");
  const [nMin, setNMin] = useState(60);
  const [verif, setVerif] = useState(null);
  const [coachMsg, setCoachMsg] = useState("");
  const [coachBusy, setCoachBusy] = useState(false);
  const [proposal, setProposal] = useState(null);
  const [bilanBusy, setBilanBusy] = useState(false);
  const [obStep, setObStep] = useState(0);
  const [pseudo, setPseudo] = useState("");
  const [obAvatar, setObAvatar] = useState(null);
  const [dispPct, setDispPct] = useState(0);
  const [viewProof, setViewProof] = useState(null);
  const [shareImg, setShareImg] = useState(null);
  const [shareBusy, setShareBusy] = useState(false);
  const [settings, setSettings] = useState(false);
  const [subView, setSubView] = useState(false);
  const [editPseudo, setEditPseudo] = useState("");
  const [confirmClear, setConfirmClear] = useState(false);
  const [gradeUp, setGradeUp] = useState(null);
  const [wall, setWall] = useState(false);
  const [liveUsers, setLiveUsers] = useState([]);
  const [listening, setListening] = useState(false);
  const [voiceErr, setVoiceErr] = useState(null);
  const [, setTick] = useState(0);
  const fileRef = useRef(null);
  const avatarRef = useRef(null);
  const recRef = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await window.storage.get("flag:data");
        if (res && res.value) setData({ bilans: {}, ...JSON.parse(res.value) });
      } catch (e) {}
      setLoaded(true);
    })();
  }, []);

  const persist = async (next) => {
    setData(next);
    try {
      await window.storage.set("flag:data", JSON.stringify(next));
    } catch (e) {
      console.error("storage", e);
    }
  };

  const today = todayKey();
  const tasks = data.tasks.filter((t) => t.date === today);

  /* tic-tac pour chrono de bloc + fenêtre de preuve */
  useEffect(() => {
    const running = data.tasks.some((t) => t.startedAt && t.status !== "verified") || (verif && verif.photoAt && !verif.verdict) || liveUsers.length > 0;
    if (!running) return;
    const iv = setInterval(() => setTick((x) => x + 1), 1000);
    return () => clearInterval(iv);
  }, [data.tasks, verif, liveUsers]);
  const pending = tasks.filter((t) => t.status !== "verified");
  const done = tasks.filter((t) => t.status === "verified");
  const minutesDone = done.reduce((s, t) => s + (t.minutes || 0), 0);
  const pct = tasks.length ? Math.round((done.length / tasks.length) * 100) : 0;
  const grade = gradeFor(data.streak);
  const bilan = (data.bilans || {})[today];
  const persona = personaOf(data.persona);

  /* le Rival — ton double déterministe */
  const rivalResults = tasks.map((t) => {
    let h = 0;
    const s = t.id + today;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return { done: h % 100 < 82, min: t.minutes || 0 };
  });
  const rivalDone = rivalResults.filter((r) => r.done).length;
  const rivalMin = rivalResults.filter((r) => r.done).reduce((s, r) => s + r.min, 0);
  const rivalLead = done.length - rivalDone;

  const allProofs = data.tasks
    .filter((t) => t.status === "verified" && t.thumb)
    .sort((a, b) => (a.date < b.date ? 1 : -1));
  const theme = data.theme || "dark";
  const appCls = "app" + (theme === "dark" ? " dark" : "");
  const toggleTheme = () => persist({ ...data, theme: theme === "dark" ? "light" : "dark" });

  /* heatmap de régularité (84 derniers jours) */
  const heatMap = {};
  data.tasks.forEach((t) => {
    if (t.status === "verified") heatMap[t.date] = (heatMap[t.date] || 0) + (t.minutes || 0);
  });
  const heatCells = [];
  for (let i = 83; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const k = dayKeyOf(d);
    heatCells.push({ k, min: heatMap[k] || 0 });
  }
  const weekMin = heatCells.slice(-7).reduce((s, c) => s + c.min, 0);
  const heatLevel = (min) => (min === 0 ? 0 : min < 30 ? 1 : min < 60 ? 2 : min < 120 ? 3 : 4);

  /* % animé */
  useEffect(() => {
    let raf;
    const from = dispPct;
    const to = pct;
    if (from === to) return;
    const start = performance.now();
    const dur = 700;
    const step = (t) => {
      const p = Math.min(1, (t - start) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      setDispPct(Math.round(from + (to - from) * e));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [pct]); // eslint-disable-line

  /* carte récap partageable */
  const makeShareCard = async () => {
    if (shareBusy) return;
    setShareBusy(true);
    try {
      const W = 1080, H = 1920;
      const c = document.createElement("canvas");
      c.width = W; c.height = H;
      const x = c.getContext("2d");
      const rr = (x0, y0, w, h, r) => {
        x.beginPath();
        x.moveTo(x0 + r, y0);
        x.arcTo(x0 + w, y0, x0 + w, y0 + h, r);
        x.arcTo(x0 + w, y0 + h, x0, y0 + h, r);
        x.arcTo(x0, y0 + h, x0, y0, r);
        x.arcTo(x0, y0, x0 + w, y0, r);
        x.closePath();
      };
      x.fillStyle = "#0D0B0E"; x.fillRect(0, 0, W, H);
      /* header */
      x.fillStyle = "#F5F3F4"; x.font = "900 88px Inter, sans-serif"; x.fillText("FLAG.", 60, 118);
      x.fillStyle = "#8A8590"; x.font = "600 40px Inter, sans-serif";
      x.textAlign = "right"; x.fillText(data.user.pseudo, W - 60, 112); x.textAlign = "left";
      /* carte art */
      x.save(); rr(60, 170, W - 120, 640, 52); x.clip();
      const g = x.createLinearGradient(60, 170, W - 60, 810);
      g.addColorStop(0, "#FF5A2E"); g.addColorStop(0.55, "#FF2E63"); g.addColorStop(1, "#B02AFF");
      x.fillStyle = g; x.fillRect(60, 170, W - 120, 640);
      x.fillStyle = "rgba(255,255,255,.12)";
      for (let i = 60; i < W - 60; i += 9) x.fillRect(i, 170, 2, 640);
      x.fillStyle = "rgba(0,0,0,.10)";
      for (let i = 64; i < W - 60; i += 21) x.fillRect(i, 170, 2, 640);
      x.fillStyle = "#fff";
      x.font = "600 44px Inter, sans-serif"; x.fillText(fmtDate(), 116, 280);
      x.font = "900 230px Inter, sans-serif"; x.fillText(pct + "%", 108, 540);
      x.font = "700 52px Inter, sans-serif";
      x.fillText(`${done.length}/${tasks.length} blocs prouvés · ${minutesDone} min`, 116, 660);
      /* jauge crantée */
      for (let i = 0; i < 20; i++) {
        x.fillStyle = pct >= ((i + 1) / 20) * 100 ? "#fff" : "rgba(255,255,255,.3)";
        x.save(); x.translate(116 + i * 26, 700); x.transform(1, 0, -0.25, 1, 0, 0); x.fillRect(0, 0, 12, 44); x.restore();
      }
      x.restore();
      /* grade */
      x.fillStyle = grade.current.color; x.font = "800 58px Inter, sans-serif";
      x.fillText(`${grade.current.icon} ${grade.current.name} · 🔥 ${data.streak} j`, 60, 930);
      /* blocs */
      let y = 1030;
      x.font = "600 46px Inter, sans-serif";
      tasks.slice(0, 7).forEach((t) => {
        const ok = t.status === "verified";
        x.fillStyle = ok ? "#18A15C" : "#8A8590";
        x.fillText(ok ? "✓" : "○", 60, y);
        x.fillStyle = ok ? "#F5F3F4" : "#8A8590";
        x.fillText(t.title.length > 32 ? t.title.slice(0, 32) + "…" : t.title, 132, y);
        y += 82;
      });
      /* mosaïque des preuves */
      const thumbs = done.filter((t) => t.thumb).slice(0, 6);
      let tx = 60; const ty = H - 440;
      for (const t of thumbs) {
        const im = await new Promise((res) => {
          const i2 = new Image();
          i2.onload = () => res(i2);
          i2.onerror = () => res(null);
          i2.src = t.thumb;
        });
        if (im) { x.save(); rr(tx, ty, 152, 152, 30); x.clip(); x.drawImage(im, tx, ty, 152, 152); x.restore(); }
        tx += 168;
      }
      /* footer */
      x.fillStyle = "#8A8590"; x.font = "600 38px Inter, sans-serif";
      x.fillText("Pris en flag de taffer — pas de photo, pas de validation.", 60, H - 110);
      setShareImg(c.toDataURL("image/png"));
    } catch (e) {
      console.error("share", e);
    }
    setShareBusy(false);
  };

  const askCoach = async () => {
    const msg = coachMsg.trim();
    if (!msg || coachBusy) return;
    setCoachBusy(true);
    setProposal(null);
    try {
      const res = await planWithAI(msg, tasks, persona.style);
      setProposal({ message: res.message, blocs: (res.blocs || []).map((b) => ({ ...b, keep: true })) });
      setCoachMsg("");
    } catch {
      setProposal({ message: "Le coach n'a pas répondu. Réessaie.", blocs: [], erreur: true });
    }
    setCoachBusy(false);
  };

  const askTemplate = async (tpl) => {
    if (coachBusy) return;
    setCoachBusy(true);
    setProposal(null);
    try {
      const res = await planWithAI(tpl.prompt, tasks, persona.style);
      setProposal({ message: res.message, blocs: (res.blocs || []).map((b) => ({ ...b, keep: true })), tpl: tpl.name });
    } catch {
      setProposal({ message: "Le coach n'a pas répondu. Réessaie.", blocs: [], erreur: true });
    }
    setCoachBusy(false);
  };

  const toggleBloc = (i) =>
    setProposal((p) => ({ ...p, blocs: p.blocs.map((b, j) => (j === i ? { ...b, keep: !b.keep } : b)) }));

  const acceptProposal = () => {
    const kept = proposal.blocs.filter((b) => b.keep);
    if (!kept.length) return setProposal(null);
    const room = data.plan === "plus" ? kept.length : Math.max(0, 3 - tasks.length);
    const toAdd = kept.slice(0, room);
    if (toAdd.length < kept.length) setSubView(true);
    if (!toAdd.length) return;
    persist({
      ...data,
      tasks: [
        ...data.tasks,
        ...toAdd.map((b) => ({
          id: uid(),
          date: today,
          title: b.titre,
          cat: CATS.includes(b.cat) ? b.cat : "Autre",
          minutes: Math.min(180, Math.max(15, Number(b.minutes) || 30)),
          icon: b.emoji && b.emoji.length <= 4 ? b.emoji : iconFor(b.titre, b.cat),
          status: "pending",
          coach: true,
        })),
      ],
    });
    setProposal(null);
  };

  const makeBilan = async () => {
    if (bilanBusy || !tasks.length) return;
    setBilanBusy(true);
    try {
      const res = await bilanWithAI(tasks, data.streak, grade.current.name, persona.style);
      persist({ ...data, bilans: { ...(data.bilans || {}), [today]: res } });
    } catch {
      persist({ ...data, bilans: { ...(data.bilans || {}), [today]: { resume: "Bilan indisponible (réseau).", encouragement: "Réessaie dans un instant." } } });
    }
    setBilanBusy(false);
  };

  const addTask = () => {
    const title = nTitle.trim();
    if (!title) return;
    persist({
      ...data,
      tasks: [...data.tasks, { id: uid(), date: today, title, cat: nCat, minutes: Number(nMin) || 30, icon: iconFor(title, nCat), status: "pending" }],
    });
    setNTitle("");
    setAdding(false);
  };

  const removeTask = (id) => persist({ ...data, tasks: data.tasks.filter((t) => t.id !== id) });

  const freeLimitHit = data.plan !== "plus" && tasks.length >= 3;
  const tryAdd = () => {
    if (freeLimitHit) return setSubView(true);
    setAdding(true);
  };
  const toggleTimer = (id) => {
    const t = data.tasks.find((z) => z.id === id);
    if (!t) return;
    const starting = !t.startedAt;
    const myId = data.uid || uid();
    persist({ ...data, uid: myId, tasks: data.tasks.map((z) => (z.id === id ? { ...z, startedAt: starting ? Date.now() : null } : z)) });
    if (starting) {
      const payload = {
        p: data.user.pseudo,
        e: t.icon || iconFor(t.title, t.cat),
        c: t.cat,
        s: Date.now(),
        x: Date.now() + (Number(t.minutes) + 20) * 60000,
      };
      window.storage.set("live:" + myId, JSON.stringify(payload), true).catch(() => {});
    } else {
      window.storage.delete("live:" + myId, true).catch(() => {});
    }
  };

  const refreshRoom = async () => {
    try {
      const res = await window.storage.list("live:", true);
      const keys = ((res && res.keys) || []).slice(0, 12);
      const now = Date.now();
      const out = [];
      for (const k of keys) {
        if (data.uid && k === "live:" + data.uid) continue;
        try {
          const r = await window.storage.get(k, true);
          if (r && r.value) {
            const v = JSON.parse(r.value);
            if (v.x > now && now - v.s < 4 * 3600000) out.push(v);
          }
        } catch {}
      }
      setLiveUsers(out);
    } catch {}
  };

  useEffect(() => {
    if (!loaded || !data.user) return;
    refreshRoom();
    const iv = setInterval(refreshRoom, 25000);
    return () => clearInterval(iv);
  }, [loaded, data.user]); // eslint-disable-line

  const startVoice = () => {
    setVoiceErr(null);
    if (listening) {
      try { recRef.current && recRef.current.stop(); } catch {}
      setListening(false);
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setVoiceErr("Dictée non supportée par ce navigateur — écris ta journée à la place.");
      return;
    }
    const rec = new SR();
    rec.lang = "fr-FR";
    rec.interimResults = true;
    rec.continuous = false;
    rec.maxAlternatives = 1;
    rec.onstart = () => setListening(true);
    rec.onresult = (e) => {
      const txt = Array.from(e.results).map((r) => r[0].transcript).join(" ").trim();
      if (txt) setCoachMsg(txt);
    };
    rec.onend = () => { setListening(false); recRef.current = null; };
    rec.onerror = (e) => {
      setListening(false);
      recRef.current = null;
      if (e.error === "not-allowed" || e.error === "service-not-allowed")
        setVoiceErr("Micro non autorisé dans cet aperçu — dans la vraie app ce sera natif. Écris ta journée en attendant.");
      else if (e.error === "no-speech")
        setVoiceErr("J'ai rien entendu — réessaie en parlant plus fort.");
      else if (e.error !== "aborted")
        setVoiceErr("Micro indisponible ici. Écris ta journée à la place.");
    };
    recRef.current = rec;
    try { rec.start(); } catch {
      recRef.current = null;
      setVoiceErr("Impossible de lancer le micro dans cet environnement.");
    }
  };

  const onAvatarFile = async (e) => {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file) return;
    try {
      const { thumb } = await processPhoto(file);
      if (!data.user) setObAvatar(thumb);
      else persist({ ...data, user: { ...data.user, avatar: thumb } });
    } catch {}
  };

  const startVerif = (task) => {
    setVerif({ taskId: task.id, preview: null, b64: null, checking: false, verdict: null });
    setTimeout(() => fileRef.current && fileRef.current.click(), 50);
  };

  const onFile = async (e) => {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file || !verif) return;
    try {
      const { b64, preview, thumb, mid } = await processPhoto(file);
      setVerif((v) => ({ ...v, preview, b64, thumb, mid, photoAt: Date.now() }));
    } catch {
      setVerif((v) => ({ ...v, verdict: { valide: false, motif: "Photo illisible, réessaie." } }));
    }
  };

  const submitProof = async () => {
    if (!verif || !verif.b64) return;
    if (verif.photoAt && Date.now() - verif.photoAt > 60000) {
      setVerif((v) => ({ ...v, verdict: { valide: false, motif: "Preuve expirée — plus de 60 s. Reprends une photo direct, sur le vif." } }));
      return;
    }
    const task = data.tasks.find((t) => t.id === verif.taskId);
    setVerif((v) => ({ ...v, checking: true, verdict: null }));
    let verdict;
    try {
      verdict = await verifyWithAI(task, verif.b64, persona.style);
    } catch {
      setVerif((v) => ({ ...v, checking: false, verdict: { valide: false, motif: "Vérification impossible (réseau). Réessaie." } }));
      return;
    }
    if (verdict.valide) {
      const before = gradeFor(data.streak).current;
      let { streak, lastDay } = data;
      if (lastDay !== today) {
        streak = lastDay === yesterdayKey() ? streak + 1 : 1;
        lastDay = today;
      }
      const after = gradeFor(streak).current;
      persist({
        ...data,
        streak,
        lastDay,
        totalVerified: (data.totalVerified || 0) + 1,
        tasks: data.tasks.map((t) =>
          t.id === verif.taskId ? { ...t, status: "verified", at: nowHM(), motif: verdict.motif, thumb: verif.thumb, proof: verif.mid, startedAt: null } : t
        ),
      });
      if (after.name !== before.name) setTimeout(() => setGradeUp(after), 600);
      if (data.uid) window.storage.delete("live:" + data.uid, true).catch(() => {});
    } else {
      persist({ ...data, tasks: data.tasks.map((t) => (t.id === verif.taskId ? { ...t, lastRefus: verdict.motif } : t)) });
    }
    setVerif((v) => ({ ...v, checking: false, verdict }));
  };

  if (!loaded)
    return (
      <div className={appCls}>
        <style>{css}</style>
        <div className="label center pad">Chargement…</div>
      </div>
    );

  /* ===== accueil / connexion ===== */
  if (!data.user)
    return (
      <div className={appCls}>
        <style>{css}</style>
        <div className="aurora" aria-hidden="true"><span /><span /><span /></div>
        {obStep === 0 ? (
          <div className="landing">
            <h1 className="land-title">FLAG.</h1>
            <div className="art art-blue land-art">
              <div className="land-art-txt">Pris en flag<br />de taffer</div>
              <div className="pill-progress"><span className="pill-dot" />preuve par photo</div>
            </div>
            <div className="land-feats">
              <div className="feat"><b>Planifie.</b> Décris ta journée, le coach IA crée tes blocs.</div>
              <div className="feat"><b>Prouve.</b> Chaque bloc se valide par une photo scannée par l'IA.</div>
              <div className="feat"><b>Monte en grade.</b> De Fer à Radiant, un jour à la fois.</div>
            </div>
            <button className="btn-black big" onClick={() => setObStep(1)}>Commencer</button>
          </div>
        ) : (
          <div className="landing">
            <input ref={avatarRef} type="file" accept="image/*" style={{ display: "none" }} onChange={onAvatarFile} />
            <button className="circle-btn land-close" onClick={() => setObStep(0)} aria-label="Retour">×</button>
            <button className="ob-avatar" onClick={() => avatarRef.current && avatarRef.current.click()} aria-label="Choisir une photo de profil">
              {obAvatar ? <img src={obAvatar} alt="" className="avatar-img" /> : <Bot />}
              <span className="ob-plus">＋</span>
            </button>
            <h1 className="land-title2">Ton blaze</h1>
            <div className="label center">Photo et pseudo — ils apparaîtront sur tes preuves et ton grade.</div>
            <input
              className="field land-field"
              placeholder="Pseudo"
              value={pseudo}
              maxLength={20}
              onChange={(e) => setPseudo(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && pseudo.trim() && persist({ ...data, user: { pseudo: pseudo.trim(), avatar: obAvatar } })}
              autoFocus
            />
            <button className="btn-black big" disabled={!pseudo.trim()} onClick={() => persist({ ...data, user: { pseudo: pseudo.trim(), avatar: obAvatar } })}>
              Créer
            </button>
          </div>
        )}
      </div>
    );

  /* ===== app ===== */
  return (
    <div className={appCls}>
      <style>{css}</style>
      <div className="aurora" aria-hidden="true"><span /><span /><span /></div>
      <input ref={fileRef} type="file" accept="image/*" capture="environment" style={{ display: "none" }} onChange={onFile} />
      <input ref={avatarRef} type="file" accept="image/*" style={{ display: "none" }} onChange={onAvatarFile} />

      {/* header */}
      <header className="head rise">
        <div>
          <div className="label">{greet()}, {data.user.pseudo}</div>
          <h1 className="h1">Ta journée <span className="h1-count">({tasks.length})</span></h1>
        </div>
        <div className="head-right">
          <button className="circle-btn theme" onClick={toggleTheme} aria-label="Changer de thème">{theme === "dark" ? "☀" : "☾"}</button>
          <button className="avatar" onClick={() => { setEditPseudo(data.user.pseudo); setConfirmClear(false); setSubView(false); setSettings(true); }} aria-label="Paramètres">
            {data.user.avatar ? <img src={data.user.avatar} alt="" className="avatar-img" /> : <Bot />}
          </button>
        </div>
      </header>

      {/* carte du jour — art */}
      <section className="art art-blue day-card rise" style={{ animationDelay: ".05s" }}>
        <div className="day-title">{fmtDate().split(" ")[0]}<br />{fmtDate().split(" ").slice(1).join(" ")}</div>
        <div className="pill-progress">
          <span className="pill-dot" />
          <b>{done.length}/{tasks.length}</b>&nbsp;blocs · {minutesDone} min
        </div>
        <div className="day-bottom">
          <div className="pwr">
            <div className="pwr-num">{dispPct}<span className="pwr-sign">%</span></div>
            <div className="pwr-bar">
              {[...Array(20)].map((_, i) => (
                <div key={i} className={"notch" + (pct >= ((i + 1) / 20) * 100 ? " notch-on" : "")} />
              ))}
            </div>
          </div>
          <div className="day-btns">
            <button className="circle-btn light" onClick={makeShareCard} disabled={shareBusy || !tasks.length} aria-label="Partager ma journée">{shareBusy ? "…" : "↗"}</button>
            <button className="circle-btn light" onClick={tryAdd} aria-label="Ajouter un bloc">＋</button>
          </div>
        </div>
      </section>

      {/* carte grade — art teintée */}
      <section
        className="art grade-card rise"
        style={{ animationDelay: ".1s", backgroundImage: `repeating-linear-gradient(90deg, rgba(255,255,255,.14) 0 1px, transparent 1px 3px), radial-gradient(circle at 30% 25%, ${grade.current.color}, transparent 60%), linear-gradient(140deg, ${grade.current.color} 0%, #1c1c1e 130%)` }}
      >
        <div className="grade-top">
          <div className="grade-name">{grade.current.icon} {grade.current.name}</div>
          <div className="grade-streak">🔥 {data.streak} j</div>
        </div>
        <div className="grade-bar"><div className="grade-fill" style={{ width: Math.round(grade.prog * 100) + "%" }} /></div>
        <div className="grade-hint">
          {grade.next ? `${grade.next.icon} ${grade.next.name} dans ${grade.next.min - data.streak} jour${grade.next.min - data.streak > 1 ? "s" : ""}` : "Grade maximum. Respect."}
        </div>
      </section>

      {/* le rival */}
      <section className="card rival rise" style={{ animationDelay: ".13s" }}>
        <div className="rival-head">
          <span className="rival-title">⚔️ Le Rival</span>
          <span className="label">l'autre toi — celui qui lâche jamais</span>
        </div>
        {tasks.length === 0 ? (
          <div className="rival-verdict">Il attend ton planning. Dès que tu poses des blocs, il attaque les mêmes que toi.</div>
        ) : (
          <>
            <div className="rival-vs">
              <div className="rv-col">
                <div className="label">Toi</div>
                <div className="rv-num">{done.length}</div>
                <div className="label">{minutesDone} min</div>
              </div>
              <div className="rv-x">VS</div>
              <div className="rv-col">
                <div className="label">Lui</div>
                <div className="rv-num rv-ghost">{rivalDone}</div>
                <div className="label">{rivalMin} min</div>
              </div>
            </div>
            <div className={"rival-verdict" + (rivalLead > 0 ? " rv-ok" : rivalLead < 0 ? " rv-bad" : "")}>
              {rivalLead > 0
                ? `Tu le domines de ${rivalLead} bloc${rivalLead > 1 ? "s" : ""}. Garde l'avance.`
                : rivalLead < 0
                ? `Il te met ${-rivalLead} bloc${rivalLead < -1 ? "s" : ""} dans la vue. Rattrape-le avant ce soir.`
                : "Égalité parfaite. Le prochain bloc départage."}
            </div>
          </>
        )}
      </section>

      {/* salle commune */}
      {(() => {
        const myLive = tasks.find((t) => t.startedAt && t.status !== "verified");
        const roomCount = liveUsers.length + (myLive ? 1 : 0);
        return (
          <section className="card room rise" style={{ animationDelay: ".16s" }}>
            <div className="rival-head">
              <span className="rival-title"><span className="live-dot" /> Salle commune</span>
              <span className="label">{roomCount} en session</span>
            </div>
            {roomCount === 0 ? (
              <div className="rival-verdict">Personne en session là. Lance un chrono ▶ sur un bloc et ouvre le bal.</div>
            ) : (
              <div className="room-list">
                {myLive && (
                  <div className="room-row room-me">
                    <span className="task-emoji big-emoji">{myLive.icon || iconFor(myLive.title, myLive.cat)}</span>
                    <span className="task-body">
                      <span className="task-title">Toi</span>
                      <span className="label">{myLive.cat} · en bloc</span>
                    </span>
                    <span className="live-time">● {fmtElapsed(Date.now() - myLive.startedAt)}</span>
                  </div>
                )}
                {liveUsers.map((u, i) => (
                  <div key={i} className="room-row">
                    <span className="task-emoji big-emoji">{u.e}</span>
                    <span className="task-body">
                      <span className="task-title">{u.p}</span>
                      <span className="label">{u.c} · en bloc</span>
                    </span>
                    <span className="live-time">● {fmtElapsed(Date.now() - u.s)}</span>
                  </div>
                ))}
              </div>
            )}
            <div className="label room-note">Chrono lancé = ton pseudo et ton activité sont visibles par les autres utilisateurs.</div>
          </section>
        );
      })()}

      {/* régularité — heatmap */}
      <div className="label sect">Régularité</div>
      <section className="card heat rise" style={{ animationDelay: ".15s" }}>
        <div className="heat-head">
          <span className="heat-stat"><b>{weekMin} min</b> prouvées sur 7 jours</span>
          <button className="label link" onClick={() => setWall(true)} disabled={!allProofs.length}>Voir le mur ›</button>
        </div>
        <div className="heat-grid">
          {heatCells.map((c) => (
            <span key={c.k} className={"hc hc-" + heatLevel(c.min)} title={`${c.k} · ${c.min} min`} />
          ))}
        </div>
      </section>

      {/* coach */}
      <div className="label sect">Coach</div>
      <section className="card coach">
        <div className="coach-row">
          <div className={"coach-bot" + (coachBusy || listening ? " bot-busy" : "")}><Bot /></div>
          <input
            className="field grow"
            placeholder={listening ? "Je t'écoute…" : "Décris ta journée, je planifie"}
            value={coachMsg}
            onChange={(e) => setCoachMsg(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askCoach()}
            disabled={coachBusy}
          />
          <button className={"circle-btn mic" + (listening ? " mic-on" : "")} onClick={startVoice} disabled={coachBusy} aria-label={listening ? "Arrêter la dictée" : "Dicter ma journée"}>🎙</button>
          <button className="circle-btn black" onClick={askCoach} disabled={coachBusy || !coachMsg.trim()} aria-label="Envoyer">↑</button>
        </div>

        {voiceErr && <div className="label refus voice-err">{voiceErr}</div>}

        {coachBusy && <div className="label thinking">Le coach réfléchit…</div>}

        {!proposal && !coachBusy && (
          <div className="tpl-row">
            {TEMPLATES.map((t) => (
              <button key={t.id} className="chip" onClick={() => askTemplate(t)}>{t.icon} {t.name}</button>
            ))}
          </div>
        )}

        {proposal && (
          <div className="proposal">
            {proposal.tpl && <div className="label ptag">Programme · {proposal.tpl}</div>}
            <div className="pmsg">{proposal.message}</div>
            {proposal.blocs.map((b, i) => (
              <button key={i} className="task pbloc" onClick={() => toggleBloc(i)}>
                <span className={"check" + (b.keep ? " check-on" : "")}>{b.keep ? "✓" : ""}</span>
                <span className="task-emoji">{b.emoji && b.emoji.length <= 4 ? b.emoji : iconFor(b.titre, b.cat)}</span>
                <span className="task-body">
                  <span className={"task-title" + (b.keep ? "" : " strike")}>{b.titre}</span>
                  <span className="label">{b.cat} · {b.minutes} min</span>
                </span>
              </button>
            ))}
            {proposal.blocs.length > 0 && (
              <div className="row-btns">
                <button className="btn-ghost" onClick={() => setProposal(null)}>Refuser</button>
                <button className="btn-black" onClick={acceptProposal}>Ajouter {proposal.blocs.filter((b) => b.keep).length}</button>
              </div>
            )}
          </div>
        )}
      </section>

      {/* blocs à prouver */}
      <div className="label sect">À prouver ({pending.length})</div>
      <section className="card">
        {pending.length === 0 && tasks.length === 0 && (
          <div className="task"><span className="task-body"><span className="task-title">Journée vide</span><span className="label">Lance un template ou décris ta journée au coach.</span></span></div>
        )}
        {pending.length === 0 && tasks.length > 0 && (
          <div className="task"><span className="task-body"><span className="task-title">Tout est prouvé 🎯</span><span className="label">Génère ton bilan en bas.</span></span></div>
        )}
        {pending.map((t) => (
          <div key={t.id} className={"task" + (t.startedAt ? " task-live" : "")}>
            <span className="task-emoji big-emoji">{t.icon || iconFor(t.title, t.cat)}</span>
            <span className="task-body">
              <span className="task-title">{t.title}{t.coach && <span className="coach-star"> ✦</span>}</span>
              <span className="label">
                {t.startedAt
                  ? <span className="live-time">● {fmtElapsed(Date.now() - t.startedAt)} / {t.minutes} min</span>
                  : `${t.cat} · ${t.minutes} min`}
              </span>
              {t.lastRefus && <span className="label refus">Refusé : {t.lastRefus}</span>}
            </span>
            <button className={"circle-btn timer-btn" + (t.startedAt ? " timer-on" : "")} onClick={() => toggleTimer(t.id)} aria-label={t.startedAt ? "Arrêter le chrono" : "Démarrer le chrono"}>
              {t.startedAt ? "■" : "▶"}
            </button>
            <button className="btn-black small" onClick={() => startVerif(t)}>Flag</button>
            <button className="x" onClick={() => removeTask(t.id)} aria-label="Supprimer">×</button>
          </div>
        ))}

        {adding && (
          <div className="task add-form">
            <div className="task-body add-body">
              <input
                className="field"
                placeholder="Ex : 2h de maths — intégrales"
                value={nTitle}
                onChange={(e) => setNTitle(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addTask()}
                autoFocus
              />
              <div className="chip-row">
                {CATS.map((c) => (
                  <button key={c} className={"chip" + (nCat === c ? " chip-on" : "")} onClick={() => setNCat(c)}>{c}</button>
                ))}
                <select className="field sel" value={nMin} onChange={(e) => setNMin(e.target.value)}>
                  {[15, 30, 45, 60, 90, 120, 180].map((m) => <option key={m} value={m}>{m} min</option>)}
                </select>
              </div>
              <div className="row-btns">
                <button className="btn-ghost" onClick={() => setAdding(false)}>Annuler</button>
                <button className="btn-black" onClick={addTask}>Créer</button>
              </div>
            </div>
          </div>
        )}
        {!adding && (
          <button className="task task-add" onClick={tryAdd}>
            <span className="check add-plus">＋</span>
            <span className="task-body">
              <span className="task-title">Nouveau bloc</span>
              {freeLimitHit && <span className="label">Limite gratuite atteinte (3/jour) — FLAG+ pour l'illimité</span>}
            </span>
          </button>
        )}
      </section>

      {/* complétés */}
      {done.length > 0 && (
        <>
          <div className="label sect">Prouvés ({done.length})</div>
          <section className="card">
            {done.map((t) => (
              <button key={t.id} className="task task-add" onClick={() => setViewProof(t.id)}>
                <span className="check check-on">✓</span>
                <span className="task-body">
                  <span className="task-title strike">{t.title}</span>
                  <span className="label">{t.at} — {t.motif}</span>
                </span>
                {t.thumb && <img src={t.thumb} alt="" className="thumb" />}
              </button>
            ))}
          </section>
        </>
      )}

      {/* bilan */}
      {tasks.length > 0 && (
        <>
          <div className="label sect">Bilan</div>
          <section className="card">
            {bilan ? (
              <div className="bilan">
                <div className="bilan-txt">{bilan.resume}</div>
                <div className="bilan-enc">{grade.current.icon} {bilan.encouragement}</div>
                <button className="label link" onClick={makeBilan} disabled={bilanBusy}>{bilanBusy ? "Génération…" : "Régénérer"}</button>
              </div>
            ) : (
              <button className="task task-add" onClick={makeBilan} disabled={bilanBusy}>
                <span className="check add-plus">✦</span>
                <span className="task-body">
                  <span className="task-title">{bilanBusy ? "Le coach analyse…" : "Générer le bilan du jour"}</span>
                  <span className="label">Résumé honnête + encouragement</span>
                </span>
              </button>
            )}
          </section>
        </>
      )}

      {/* sheet vérification */}
      {verif && (
        <div className="overlay" onClick={() => !verif.checking && setVerif(null)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <button className="circle-btn sheet-close" onClick={() => !verif.checking && setVerif(null)} aria-label="Fermer">×</button>
            <div className="sheet-title">{(data.tasks.find((t) => t.id === verif.taskId) || {}).title}</div>

            {!verif.preview && !verif.verdict && (
              <div className="sheet-body">
                <div className="label center">Prends-toi en flag. L'IA tranche.</div>
                <button className="btn-black big" onClick={() => fileRef.current && fileRef.current.click()}>Prendre la photo</button>
              </div>
            )}

            {verif.preview && !verif.verdict && (
              <div className="sheet-body">
                <img src={verif.preview} alt="preuve" className="proof-img" />
                {verif.checking ? (
                  <div className="label center thinking">Analyse en cours…</div>
                ) : (
                  <>
                    <div className="row-btns">
                      <button className="btn-ghost" onClick={() => fileRef.current && fileRef.current.click()}>Reprendre</button>
                      <button className="btn-black" onClick={submitProof}>Envoyer</button>
                    </div>
                    {verif.photoAt && (
                      <div className={"label center" + (60 - Math.floor((Date.now() - verif.photoAt) / 1000) <= 15 ? " refus" : "")}>
                        ⏱ {Math.max(0, 60 - Math.floor((Date.now() - verif.photoAt) / 1000))} s pour envoyer — après, la preuve expire
                      </div>
                    )}
                  </>
                )}
              </div>
            )}

            {verif.verdict && (
              <div className="sheet-body">
                {verif.verdict.valide && (
                  <div className="confetti" aria-hidden="true">
                    {[...Array(18)].map((_, i) => (
                      <span
                        key={i}
                        style={{
                          left: (i * 5.5 + 3) + "%",
                          animationDelay: (i % 6) * 0.12 + "s",
                          background: ["#FF5A2E", "#FF2E63", "#B02AFF", "#FFC24A", "#18A15C"][i % 5],
                        }}
                      />
                    ))}
                  </div>
                )}
                <div className={"badge" + (verif.verdict.valide ? " badge-ok" : " badge-ko")}>{verif.verdict.valide ? "✓" : "✕"}</div>
                <div className="verdict-t">{verif.verdict.valide ? "Prouvé" : "Refusé"}</div>
                <div className="label center">{verif.verdict.motif}</div>
                {verif.verdict.valide ? (
                  <button className="btn-black big" onClick={() => setVerif(null)}>OK</button>
                ) : (
                  <div className="row-btns">
                    <button className="btn-ghost" onClick={() => setVerif(null)}>Abandonner</button>
                    <button className="btn-black" onClick={() => { setVerif((v) => ({ ...v, preview: null, b64: null, verdict: null })); setTimeout(() => fileRef.current && fileRef.current.click(), 50); }}>Réessayer</button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* paramètres */}
      {settings && !subView && (
        <div className="overlay" onClick={() => setSettings(false)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <button className="circle-btn sheet-close" onClick={() => setSettings(false)} aria-label="Fermer">×</button>
            <div className="sheet-title">Paramètres</div>
            <div className="sheet-body set-body">

              <button className="ob-avatar set-avatar" onClick={() => avatarRef.current && avatarRef.current.click()} aria-label="Changer la photo de profil">
                {data.user.avatar ? <img src={data.user.avatar} alt="" className="avatar-img" /> : <Bot />}
                <span className="ob-plus">＋</span>
              </button>

              <div className="set-field-row">
                <input
                  className="field grow"
                  value={editPseudo}
                  maxLength={20}
                  onChange={(e) => setEditPseudo(e.target.value)}
                  placeholder="Pseudo"
                />
                {editPseudo.trim() && editPseudo.trim() !== data.user.pseudo && (
                  <button className="btn-black small" onClick={() => persist({ ...data, user: { ...data.user, pseudo: editPseudo.trim() } })}>OK</button>
                )}
              </div>

              <div className="set-persona">
                <div className="label">Personnalité du coach</div>
                <div className="chip-row">
                  {PERSONAS.map((p) => (
                    <button key={p.id} className={"chip" + (persona.id === p.id ? " chip-on" : "")} onClick={() => persist({ ...data, persona: p.id })}>
                      {p.emoji} {p.name}
                    </button>
                  ))}
                </div>
              </div>

              <div className="set-list">
                <button className="task task-add" onClick={() => setSubView(true)}>
                  <span className="set-ic">✦</span>
                  <span className="task-body">
                    <span className="task-title">Abonnement</span>
                    <span className="label">{data.plan === "plus" ? "FLAG+ actif" : "FLAG Gratuit"}</span>
                  </span>
                  <span className="chev">›</span>
                </button>
                <div className="task">
                  <span className="set-ic">{theme === "dark" ? "☾" : "☀"}</span>
                  <span className="task-body">
                    <span className="task-title">Mode sombre</span>
                  </span>
                  <button className={"sw" + (theme === "dark" ? " sw-on" : "")} onClick={toggleTheme} aria-label="Basculer le mode sombre">
                    <span className="sw-knob" />
                  </button>
                </div>
                <button className="task task-add" onClick={() => {
                  if (!confirmClear) return setConfirmClear(true);
                  persist({ tasks: [], streak: 0, lastDay: null, totalVerified: 0, bilans: {}, user: data.user, theme: data.theme, plan: data.plan });
                  setConfirmClear(false);
                }}>
                  <span className="set-ic danger">🗑</span>
                  <span className="task-body">
                    <span className={"task-title" + (confirmClear ? " danger" : "")}>{confirmClear ? "Sûr ? Touche encore pour tout effacer" : "Effacer mes données"}</span>
                    <span className="label">Blocs, preuves, streak et grades — le compte reste</span>
                  </span>
                </button>
                <button className="task task-add" onClick={() => { setSettings(false); persist({ ...data, user: null }); }}>
                  <span className="set-ic danger">⏻</span>
                  <span className="task-body">
                    <span className="task-title danger">Déconnexion</span>
                  </span>
                </button>
              </div>

              <div className="label center">FLAG · prototype v1</div>
            </div>
          </div>
        </div>
      )}

      {/* abonnement */}
      {subView && (
        <div className="overlay" onClick={() => setSubView(false)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <button className="circle-btn sheet-close" onClick={() => setSubView(false)} aria-label="Retour">‹</button>
            <div className="sheet-title">Abonnement</div>
            <div className="sheet-body">
              <div className="art art-blue sub-card">
                <div className="sub-name">FLAG+</div>
                <div className="sub-price">3,99 € <span className="sub-per">/ mois</span></div>
              </div>
              <div className="sub-feats">
                <div className="sub-feat"><b>Blocs illimités</b> — gratuit : 3 par jour</div>
                <div className="sub-feat"><b>Coach à mémoire</b> — il apprend tes patterns et planifie tout seul</div>
                <div className="sub-feat"><b>Joker de streak</b> — 1 journée protégée tous les 14 jours</div>
                <div className="sub-feat"><b>Stats avancées</b> — heatmap complète, récaps hebdo</div>
              </div>
              {data.plan === "plus" ? (
                <button className="btn-ghost" onClick={() => persist({ ...data, plan: null })}>Résilier FLAG+ (démo)</button>
              ) : (
                <button className="btn-black big" onClick={() => persist({ ...data, plan: "plus" })}>Passer à FLAG+ (démo)</button>
              )}
              <div className="label center">Prototype — aucun paiement réel. Dans la vraie app : achat in-app Apple/Google.</div>
            </div>
          </div>
        </div>
      )}

      {/* le mur des preuves */}
      {wall && (
        <div className="overlay" onClick={() => setWall(false)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <button className="circle-btn sheet-close" onClick={() => setWall(false)} aria-label="Fermer">×</button>
            <div className="sheet-title">Le Mur — {allProofs.length} preuve{allProofs.length > 1 ? "s" : ""}</div>
            <div className="sheet-body">
              <div className="wall-grid">
                {allProofs.map((t) => (
                  <button key={t.id} className="wall-cell" onClick={() => { setWall(false); setViewProof(t.id); }}>
                    <img src={t.thumb} alt="" />
                  </button>
                ))}
              </div>
              <div className="label center">Chaque photo est un moment où t'as tenu parole.</div>
            </div>
          </div>
        </div>
      )}

      {/* montée en grade */}
      {gradeUp && (
        <div className="overlay" onClick={() => setGradeUp(null)}>
          <div className="gradeup" onClick={(e) => e.stopPropagation()} style={{ borderColor: gradeUp.color + "66" }}>
            <div className="confetti" aria-hidden="true">
              {[...Array(22)].map((_, i) => (
                <span key={i} style={{ left: (i * 4.5 + 2) + "%", animationDelay: (i % 7) * 0.1 + "s", background: [gradeUp.color, "#FF5A2E", "#FF2E63", "#B02AFF", "#FFC24A"][i % 5] }} />
              ))}
            </div>
            <div className="gu-icon" style={{ background: gradeUp.color + "26", borderColor: gradeUp.color }}>{gradeUp.icon}</div>
            <div className="label center gu-label">Nouveau grade</div>
            <div className="gu-name" style={{ color: gradeUp.color }}>{gradeUp.name}</div>
            <div className="label center">{data.streak} jour{data.streak > 1 ? "s" : ""} de régularité prouvée. Continue.</div>
            <button className="btn-black big" onClick={() => setGradeUp(null)}>Continuer</button>
          </div>
        </div>
      )}

      {/* vue preuve */}
      {viewProof && (() => {
        const t = data.tasks.find((z) => z.id === viewProof);
        if (!t) return null;
        return (
          <div className="overlay" onClick={() => setViewProof(null)}>
            <div className="sheet" onClick={(e) => e.stopPropagation()}>
              <button className="circle-btn sheet-close" onClick={() => setViewProof(null)} aria-label="Fermer">×</button>
              <div className="sheet-title">{t.icon || "✓"} {t.title}</div>
              <div className="sheet-body">
                {(t.proof || t.thumb) && <img src={t.proof || t.thumb} alt="preuve" className="proof-img" />}
                <div className="label center">Prouvé à {t.at} · {t.minutes} min · {t.cat}</div>
                <div className="bilan-enc center">"{t.motif}"</div>
              </div>
            </div>
          </div>
        );
      })()}

      {/* carte de partage */}
      {shareImg && (
        <div className="overlay" onClick={() => setShareImg(null)}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <button className="circle-btn sheet-close" onClick={() => setShareImg(null)} aria-label="Fermer">×</button>
            <div className="sheet-title">Ton récap du jour</div>
            <div className="sheet-body">
              <img src={shareImg} alt="récap" className="share-img" />
              <a className="btn-black big share-dl" href={shareImg} download="flag-recap.png">Télécharger l'image</a>
              <div className="label center">Format story — balance-la où tu veux.</div>
            </div>
          </div>
        </div>
      )}

      <footer className="label center foot">
        Pas de photo, pas de validation.
      </footer>
    </div>
  );
}

/* ================= styles — éditorial ================= */

const css = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
  --bg:#E9EAEC; --card:#FFFFFF; --ink:#0B0B0C; --label:#8B8F94;
  --sep:rgba(11,11,12,.07); --fill:rgba(11,11,12,.05);
  --glass:rgba(255,255,255,.66); --glass-b:rgba(255,255,255,.85);
  --ok:#18A15C; --ko:#E23A3A;
}
*{box-sizing:border-box; margin:0; -webkit-tap-highlight-color:transparent;}
.app{
  min-height:100vh; color:var(--ink);
  background:
    radial-gradient(620px 320px at 85% -90px, rgba(255,90,46,.16), transparent 60%),
    radial-gradient(520px 320px at -5% 32%, rgba(158,42,255,.12), transparent 55%),
    radial-gradient(480px 300px at 100% 78%, rgba(255,46,99,.09), transparent 55%),
    var(--bg);
  font-family:'Inter',-apple-system,system-ui,sans-serif;
  padding:0 16px 44px; max-width:480px; margin:0 auto;
  font-size:16px; letter-spacing:-.3px;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
.label{color:var(--label); font-size:13px; font-weight:500; letter-spacing:-.1px; line-height:1.45;}
.center{text-align:center;} .pad{padding:70px 0;} .grow{flex:1;}

/* ===== aurora vivante ===== */
.app > *{position:relative; z-index:1;}
.aurora{position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden;}
.aurora span{position:absolute; border-radius:50%; filter:blur(90px); opacity:.32; will-change:transform;}
.aurora span:nth-child(1){width:360px; height:360px; background:#FF5A2E; top:-140px; right:-90px; animation:aur1 24s ease-in-out infinite alternate;}
.aurora span:nth-child(2){width:320px; height:320px; background:#B02AFF; left:-140px; top:28%; animation:aur2 30s ease-in-out infinite alternate;}
.aurora span:nth-child(3){width:280px; height:280px; background:#FF2E63; bottom:4%; right:6%; animation:aur3 27s ease-in-out infinite alternate;}
@keyframes aur1{to{transform:translate(-90px,140px) scale(1.25);}}
@keyframes aur2{to{transform:translate(120px,-90px) scale(1.15);}}
@keyframes aur3{to{transform:translate(-110px,-130px) scale(1.3);}}
.dark .aurora span{opacity:.42;}
@media (prefers-reduced-motion: reduce){ .aurora span{animation:none;} }

/* ===== grain de pellicule ===== */
.app::after{
  content:""; position:fixed; inset:0; z-index:80; pointer-events:none; opacity:.05;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E");
}
.dark .app::after, .app.dark::after{opacity:.07;}

/* header sticky façon nav bar iOS */
.head{
  display:flex; align-items:flex-start; justify-content:space-between;
  position:sticky; top:0; z-index:30;
  margin:0 -16px 14px; padding:20px 20px 12px;
  background:rgba(233,234,236,.72);
  backdrop-filter:blur(18px) saturate(1.6); -webkit-backdrop-filter:blur(18px) saturate(1.6);
  border-bottom:.5px solid var(--sep);
}
.dark .head{background:rgba(13,11,14,.72);}
.h1{font-size:34px; font-weight:800; letter-spacing:-1.5px; line-height:1.05; margin-top:2px;}
.h1-count{color:var(--label); font-weight:700;}
.avatar{
  width:52px; height:52px; border-radius:50%; background:var(--glass); flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  border:1px solid var(--glass-b); box-shadow:0 4px 14px rgba(11,11,12,.08);
  cursor:pointer; padding:0; overflow:hidden; font-family:inherit; transition:transform .12s;
}
.avatar:active{transform:scale(.94);}
.avatar-img{width:100%; height:100%; object-fit:cover; border-radius:50%; display:block;}
.ob-avatar{
  width:88px; height:88px; border-radius:50%; background:var(--glass); align-self:center;
  display:flex; align-items:center; justify-content:center; position:relative;
  border:1px solid var(--glass-b); cursor:pointer; padding:0; overflow:visible;
  backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  box-shadow:0 6px 18px rgba(11,11,12,.1); font-family:inherit;
}
.ob-avatar .bot{width:48px; height:48px;}
.ob-avatar .avatar-img{border-radius:50%;}
.ob-plus{
  position:absolute; bottom:-2px; right:-2px; width:28px; height:28px; border-radius:50%;
  background:#FF5A2E; color:#fff; font-size:16px; font-weight:700;
  display:flex; align-items:center; justify-content:center; box-shadow:0 2px 8px rgba(255,90,46,.4);
}
.bot{width:34px; height:34px;}
.bot-head{fill:#F0F1F3; stroke:#0B0B0C; stroke-width:1.6;}
.bot-ant{stroke:#0B0B0C; stroke-width:1.6;}
.bot-tip{fill:#FF5A2E;}
.bot-eye{fill:#0B0B0C;}

/* art génératif */
.art{
  border-radius:26px; padding:22px; color:#fff; position:relative; overflow:hidden;
  margin-bottom:12px;
  box-shadow:0 14px 34px rgba(11,11,12,.18), inset 0 1px 0 rgba(255,255,255,.25);
}
.art > *{position:relative; z-index:2;}
.art::after{
  content:""; position:absolute; width:75%; aspect-ratio:1; border-radius:50%; z-index:1;
  background:radial-gradient(circle, rgba(255,255,255,.38), rgba(255,255,255,0) 68%);
  top:-24%; right:-16%; filter:blur(26px); mix-blend-mode:overlay;
  animation:blobDrift 15s ease-in-out infinite alternate; will-change:transform;
}
@keyframes blobDrift{to{transform:translate(-45%,50%) scale(1.3);}}
.art::before{
  content:""; position:absolute; inset:-40%; z-index:3; pointer-events:none;
  background:linear-gradient(115deg, transparent 43%, rgba(255,255,255,.20) 50%, transparent 57%);
  transform:translateX(-85%); animation:shine 8s ease-in-out infinite;
}
@keyframes shine{0%,58%{transform:translateX(-85%);} 80%,100%{transform:translateX(85%);}}
@media (prefers-reduced-motion: reduce){ .art::after, .art::before{animation:none;} }
.art-blue{
  background-image:
    repeating-linear-gradient(90deg, rgba(255,255,255,.13) 0 1px, transparent 1px 3px),
    repeating-linear-gradient(90deg, rgba(0,0,0,.08) 0 1px, transparent 1px 7px),
    radial-gradient(circle at 55% 40%, #6A14E8 0%, #9E2AFF 24%, rgba(158,42,255,.35) 48%, transparent 66%),
    linear-gradient(165deg, #FF5A2E 0%, #FF2E63 55%, #B02AFF 100%);
}
.day-card{min-height:230px; display:flex; flex-direction:column;}
.day-title{font-size:38px; font-weight:800; letter-spacing:-1.5px; line-height:1.02; text-shadow:0 2px 18px rgba(0,0,0,.18);}
.pill-progress{
  display:inline-flex; align-items:center; gap:8px; margin-top:14px; align-self:flex-start;
  background:rgba(255,255,255,.2); backdrop-filter:blur(6px); border-radius:99px; padding:7px 13px;
  font-size:13px; font-weight:500;
}
.pill-dot{width:14px; height:20px; background:#fff; border-radius:8px; box-shadow:0 1px 4px rgba(0,0,0,.2);}
.day-bottom{display:flex; align-items:center; justify-content:space-between; margin-top:auto; padding-top:20px;}
.pwr{display:flex; flex-direction:column; gap:8px;}
.pwr-num{font-size:36px; font-weight:900; letter-spacing:-1.5px; line-height:1; text-shadow:0 2px 14px rgba(0,0,0,.22);}
.pwr-sign{font-size:17px; font-weight:700; opacity:.85;}
.pwr-bar{display:flex; gap:2.5px;}
.notch{width:4px; height:13px; background:rgba(255,255,255,.28); border-radius:1px; transform:skewX(-14deg); transition:all .3s;}
.notch-on{background:#fff; box-shadow:0 0 7px rgba(255,255,255,.65);}

/* boutons ronds */
.circle-btn{
  width:46px; height:46px; border-radius:50%; border:none; cursor:pointer;
  font-size:20px; font-weight:600; display:flex; align-items:center; justify-content:center;
  font-family:inherit; transition:transform .12s;
}
.circle-btn:active{transform:scale(.94);}
.circle-btn.light{background:rgba(255,255,255,.85); color:var(--ink); backdrop-filter:blur(6px);}
.circle-btn.black{background:var(--ink); color:#fff; width:44px; height:44px; flex-shrink:0;}
.circle-btn.black:disabled{opacity:.25;}

/* carte grade */
.grade-card{padding:18px 20px;}
.grade-top{display:flex; align-items:baseline; justify-content:space-between; margin-bottom:12px;}
.grade-name{font-size:22px; font-weight:800; letter-spacing:-.8px; text-shadow:0 1px 10px rgba(0,0,0,.25);}
.grade-streak{font-size:14px; font-weight:700; background:rgba(255,255,255,.2); border-radius:99px; padding:5px 11px; backdrop-filter:blur(6px);}
.grade-streak, .streak-flame{display:inline-flex; align-items:center; gap:4px;}
@keyframes flame{0%,100%{transform:scale(1);} 50%{transform:scale(1.18);}}
.grade-bar{height:6px; background:rgba(255,255,255,.25); border-radius:99px; overflow:hidden;}
.grade-fill{height:100%; background:#fff; border-radius:99px; transition:width .5s ease;}
.grade-hint{font-size:12px; font-weight:600; margin-top:9px; opacity:.95;}

/* cartes blanches → verre */
.card{
  background:var(--glass); border-radius:22px; margin-bottom:12px; overflow:hidden;
  backdrop-filter:blur(20px) saturate(1.4); -webkit-backdrop-filter:blur(20px) saturate(1.4);
  border:1px solid var(--glass-b);
  box-shadow:0 10px 30px rgba(11,11,12,.08), inset 0 1px 0 rgba(255,255,255,.6);
}
.sect{padding:12px 8px 8px; text-transform:uppercase; font-size:11px; letter-spacing:.8px; font-weight:700;}

/* coach */
.coach{padding:14px;}
.coach-bot{width:44px; height:44px; flex-shrink:0; display:flex; align-items:center; justify-content:center;}
.coach-bot .bot{width:40px; height:40px;}
.coach-bot .bot-eye{transform-box:fill-box; transform-origin:center; animation:botblink 4.5s infinite;}
@keyframes botblink{0%,91%,100%{transform:scaleY(1);} 94%{transform:scaleY(.12);}}
.bot-busy .bot-eye{animation:botpulse .65s infinite;}
@keyframes botpulse{50%{opacity:.25;}}
@media (prefers-reduced-motion: reduce){ .coach-bot .bot-eye{animation:none;} }
.circle-btn.mic{width:44px; height:44px; background:var(--fill); color:var(--ink); font-size:17px; flex-shrink:0;}
.circle-btn.mic:disabled{opacity:.35;}
.mic-on{background:#FF5A2E !important; color:#fff !important; animation:micpulse 1.1s infinite;}
@keyframes micpulse{50%{box-shadow:0 0 0 9px rgba(255,90,46,.18);}}
@media (prefers-reduced-motion: reduce){ .mic-on{animation:none;} }
.coach-row{display:flex; gap:9px; align-items:center;}
.field{
  padding:13px 16px; border:1.5px solid var(--sep); border-radius:99px; font-size:15px;
  font-family:inherit; background:var(--fill); color:var(--ink); letter-spacing:-.2px; width:100%;
}
.field::placeholder{color:var(--label);}
.field:focus{outline:none; border-color:var(--ink);}
.thinking{padding:12px 6px 0; animation:blink 1.2s infinite;}
@keyframes blink{50%{opacity:.4;}}
@media (prefers-reduced-motion: reduce){ .thinking{animation:none;} }

.tpl-row{display:flex; gap:8px; margin-top:12px; overflow-x:auto; padding-bottom:2px; scrollbar-width:none; -webkit-overflow-scrolling:touch;}
.tpl-row::-webkit-scrollbar{display:none;}
.chip{
  flex-shrink:0; border:1.5px solid var(--sep); background:var(--fill); border-radius:99px;
  padding:9px 15px; font-size:13px; font-weight:600; cursor:pointer; font-family:inherit; color:var(--ink);
  letter-spacing:-.2px; transition:all .15s;
}
.chip:hover{border-color:var(--ink);}
.chip-on{background:var(--ink); color:#fff; border-color:var(--ink);}
.chip-row{display:flex; gap:8px; flex-wrap:wrap; align-items:center;}

.proposal{margin-top:12px;}
.ptag{text-transform:uppercase; font-size:10px; letter-spacing:1px; font-weight:700; padding:0 4px 6px;}
.pmsg{font-size:14px; line-height:1.5; padding:0 4px 10px; font-weight:500;}
.row-btns{display:flex; gap:8px; padding-top:10px;}

/* tâches */
.task{
  display:flex; align-items:center; gap:13px; padding:14px 16px; width:100%;
  background:none; border:none; text-align:left; font-family:inherit; color:var(--ink);
  position:relative; letter-spacing:-.3px;
}
.task + .task::before, .task + .add-form::before{
  content:""; position:absolute; top:0; left:60px; right:0; height:.5px; background:var(--sep);
}
.task-add{cursor:pointer; transition:transform .12s, background .12s;}
.task-add:active{background:var(--fill); transform:scale(.99);}
.task-add:disabled{opacity:.5;}
.task-emoji{font-size:18px; flex-shrink:0; width:24px; text-align:center;}
.big-emoji{
  width:40px; height:40px; border-radius:50%; background:var(--fill);
  display:flex; align-items:center; justify-content:center; font-size:18px;
}
.task-body{flex:1; min-width:0; display:flex; flex-direction:column; gap:2px;}
.task-title{font-size:15px; font-weight:600;}
.strike{text-decoration:line-through; color:var(--label);}
.coach-star{color:#FF5A2E; font-size:12px;}
.refus{color:var(--ko);}
.check{
  width:26px; height:26px; border-radius:50%; border:1.5px solid rgba(11,11,12,.18);
  display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700;
  color:#fff; flex-shrink:0; transition:all .15s; background:var(--card);
}
.check-on{background:var(--ink); border-color:var(--ink);}
.add-plus{border-style:dashed; color:var(--ink); font-weight:600;}
.thumb{width:40px; height:40px; object-fit:cover; border-radius:12px; flex-shrink:0;}
.x{background:none; border:none; color:var(--label); font-size:19px; cursor:pointer; padding:2px 4px; flex-shrink:0;}
.pbloc{cursor:pointer;}
.pbloc + .pbloc::before{left:48px;}

/* boutons */
.btn-black{
  font-family:inherit; font-size:15px; font-weight:700; color:#fff; letter-spacing:-.2px;
  background:var(--ink); border:none; border-radius:99px; padding:13px 22px; cursor:pointer; flex:1;
  transition:transform .12s, opacity .12s;
}
.btn-black:active{transform:scale(.98); opacity:.85;}
.btn-black:disabled{opacity:.3;}
.btn-black.big{flex:none; width:100%; padding:16px;}
.btn-black.small{flex:none; padding:9px 18px; font-size:13px;}
.btn-ghost{
  font-family:inherit; font-size:15px; font-weight:600; color:var(--ink); letter-spacing:-.2px;
  background:var(--card); border:1.5px solid var(--sep); border-radius:99px; padding:13px 20px; cursor:pointer; flex:1;
}
button:focus-visible, input:focus-visible, select:focus-visible{outline:2px solid var(--ink); outline-offset:2px;}
.sel{width:auto; font-size:13px; padding:9px 13px;}
.add-form{padding:14px 16px;}
.add-body{gap:10px;}
.link{background:none; border:none; cursor:pointer; text-align:left; padding:0; text-decoration:underline; font-family:inherit;}
.link:disabled{opacity:.5;}

/* bilan */
.bilan{padding:16px; display:flex; flex-direction:column; gap:11px;}

/* heatmap */
.heat{padding:16px;}
.heat-head{display:flex; align-items:baseline; justify-content:space-between; margin-bottom:12px;}
.heat-stat{font-size:14px; font-weight:500; color:var(--label);}
.heat-stat b{color:var(--ink); font-weight:800;}
.heat-grid{
  display:grid; grid-template-rows:repeat(7, 1fr); grid-auto-flow:column;
  gap:3.5px; justify-content:space-between;
}
.hc{width:100%; aspect-ratio:1; min-width:8px; border-radius:3px; background:var(--fill);}
.hc-1{background:rgba(255,90,46,.28);}
.hc-2{background:rgba(255,90,46,.5);}
.hc-3{background:rgba(255,90,46,.75);}
.hc-4{background:#FF5A2E; box-shadow:0 0 6px rgba(255,90,46,.4);}

/* confettis */
.confetti{position:absolute; inset:0; overflow:hidden; pointer-events:none; border-radius:26px 26px 0 0;}
.confetti span{
  position:absolute; top:-12px; width:8px; height:12px; border-radius:2px;
  animation:fall 1.6s ease-in forwards;
}
@keyframes fall{
  0%{transform:translateY(0) rotate(0deg); opacity:1;}
  100%{transform:translateY(420px) rotate(560deg); opacity:0;}
}
@media (prefers-reduced-motion: reduce){ .confetti{display:none;} }

/* entrée animée */
.rise{animation:rise .5s cubic-bezier(.2,.7,.3,1) both;}
@keyframes rise{from{opacity:0; transform:translateY(16px);}}
@media (prefers-reduced-motion: reduce){ .rise{animation:none;} }

/* boutons carte du jour */
.day-btns{display:flex; gap:9px;}
.circle-btn.light:disabled{opacity:.4;}

/* partage */
.share-img{width:62%; align-self:center; border-radius:18px; box-shadow:0 10px 30px rgba(0,0,0,.25);}
.share-dl{text-align:center; text-decoration:none; display:block;}
.bilan-enc.center{text-align:center;}

/* paramètres */
.set-body{gap:16px;}
.set-avatar{align-self:center;}
.set-field-row{display:flex; gap:8px; align-items:center;}
.set-list{
  border:1px solid var(--sep); border-radius:18px; overflow:hidden;
  display:flex; flex-direction:column; background:var(--fill);
}
.set-ic{width:28px; text-align:center; font-size:16px; flex-shrink:0;}
.chev{color:var(--label); font-size:20px; font-weight:600; flex-shrink:0;}
.danger{color:var(--ko);}
.set-list .task + .task::before{left:58px;}
.voice-err{padding:10px 6px 0;}

/* switch iOS */
.sw{
  width:51px; height:31px; border-radius:99px; border:none; cursor:pointer; flex-shrink:0;
  background:var(--fill); padding:2px; display:flex; justify-content:flex-start;
  transition:background .2s;
}
.sw-on{background:#34C759; justify-content:flex-end;}
.sw-knob{
  width:27px; height:27px; border-radius:50%; background:#fff; display:block;
  box-shadow:0 2px 6px rgba(0,0,0,.25); transition:transform .2s;
}

/* le rival */
.rival{padding:16px;}
.rival-head{display:flex; align-items:baseline; justify-content:space-between; margin-bottom:12px; gap:10px;}
.rival-title{font-size:15px; font-weight:800; letter-spacing:-.3px;}
.rival-vs{display:flex; align-items:center; justify-content:space-around; margin-bottom:12px;}
.rv-col{display:flex; flex-direction:column; align-items:center; gap:2px;}
.rv-num{font-size:34px; font-weight:900; letter-spacing:-1.5px; line-height:1.1;}
.rv-ghost{opacity:.55; position:relative;}
.rv-x{font-size:12px; font-weight:800; color:var(--label); letter-spacing:1px;}
.rival-verdict{
  font-size:13px; font-weight:600; text-align:center; border-radius:14px; padding:10px 12px;
  background:var(--fill); color:var(--label);
}
.rv-ok{background:rgba(24,161,92,.12); color:var(--ok);}
.rv-bad{background:rgba(226,58,58,.1); color:var(--ko);}

/* le mur */
.wall-grid{display:grid; grid-template-columns:repeat(4, 1fr); gap:6px; max-height:52vh; overflow-y:auto;}
.wall-cell{border:none; padding:0; background:none; cursor:pointer; border-radius:12px; overflow:hidden; aspect-ratio:1;}
.wall-cell img{width:100%; height:100%; object-fit:cover; display:block; transition:transform .15s;}
.wall-cell:active img{transform:scale(.94);}

/* salle commune */
.room{padding:16px;}
.live-dot{
  display:inline-block; width:9px; height:9px; border-radius:50%; background:#34C759;
  margin-right:7px; box-shadow:0 0 8px rgba(52,199,89,.6); animation:livepulse 1.6s infinite;
}
@keyframes livepulse{50%{opacity:.45;}}
@media (prefers-reduced-motion: reduce){ .live-dot{animation:none;} }
.room-list{display:flex; flex-direction:column; gap:2px; margin-bottom:10px;}
.room-row{display:flex; align-items:center; gap:12px; padding:9px 0;}
.room-row + .room-row{border-top:.5px solid var(--sep);}
.room-me .task-title{color:#FF5A2E;}
.room-note{margin-top:10px; font-size:11px;}

/* persona */
.set-persona{display:flex; flex-direction:column; gap:9px;}

/* abonnement */
.sub-card{min-height:150px; display:flex; flex-direction:column; justify-content:flex-end; margin-bottom:0;}
.sub-name{font-size:30px; font-weight:900; letter-spacing:-1px; text-shadow:0 2px 12px rgba(0,0,0,.2);}
.sub-price{font-size:20px; font-weight:800; margin-top:2px;}
.sub-per{font-size:13px; font-weight:600; opacity:.85;}
.sub-feats{display:flex; flex-direction:column; gap:9px;}
.sub-feat{font-size:14px; line-height:1.5; color:var(--label); font-weight:500;}
.sub-feat b{color:var(--ink); font-weight:700;}

/* chrono de bloc */
.task-live{background:rgba(255,90,46,.06);}
.live-time{color:#FF5A2E; font-weight:700;}
.timer-btn{width:38px; height:38px; font-size:13px; background:var(--fill); color:var(--ink); flex-shrink:0;}
.timer-on{background:#FF5A2E; color:#fff; box-shadow:0 0 12px rgba(255,90,46,.4);}

/* montée en grade */
.gradeup{
  background:var(--glass); backdrop-filter:blur(28px) saturate(1.5); -webkit-backdrop-filter:blur(28px) saturate(1.5);
  border:1.5px solid var(--glass-b); border-radius:28px; margin:0 20px 30vh;
  padding:30px 24px; width:calc(100% - 40px); max-width:380px; position:relative; overflow:hidden;
  display:flex; flex-direction:column; gap:10px; align-items:center; align-self:center;
  animation:guPop .35s cubic-bezier(.2,.8,.3,1.2) both;
}
@keyframes guPop{from{opacity:0; transform:scale(.8);}}
@media (prefers-reduced-motion: reduce){ .gradeup{animation:none;} }
.gu-icon{
  width:84px; height:84px; border-radius:50%; border:2px solid; font-size:40px;
  display:flex; align-items:center; justify-content:center;
}
.gu-label{text-transform:uppercase; letter-spacing:1.5px; font-size:11px; font-weight:700;}
.gu-name{font-size:36px; font-weight:900; letter-spacing:-1px;}
.gradeup .btn-black{margin-top:8px;}
.gradeup .confetti{border-radius:28px;}
.bilan-txt{font-size:14px; line-height:1.55; font-weight:500;}
.bilan-enc{
  font-size:14px; line-height:1.55; font-weight:600;
  background:var(--fill); border-radius:16px; padding:13px 15px;
}

/* sheet */
.overlay{position:fixed; inset:0; background:rgba(11,11,12,.4); display:flex; align-items:flex-end; justify-content:center; z-index:50;}
.overlay:has(.gradeup){align-items:center;}
.sheet{
  background:var(--glass); backdrop-filter:blur(28px) saturate(1.5); -webkit-backdrop-filter:blur(28px) saturate(1.5);
  border:1px solid var(--glass-b); border-bottom:none;
  width:100%; max-width:480px; border-radius:26px 26px 0 0; position:relative;
  animation:sheetUp .32s cubic-bezier(.2,.8,.3,1) both;
}
.sheet::before{
  content:""; display:block; width:36px; height:5px; border-radius:99px;
  background:var(--sep); margin:9px auto 0;
}
@keyframes sheetUp{from{transform:translateY(46px); opacity:0;}}
@media (prefers-reduced-motion: reduce){ .sheet{animation:none;} }
.sheet-close{position:absolute; top:14px; left:14px; background:var(--fill); color:var(--ink); width:38px; height:38px; font-size:17px;}
.sheet-title{font-size:17px; font-weight:800; letter-spacing:-.5px; text-align:center; padding:22px 60px 6px;}
.sheet-body{padding:12px 20px 34px; display:flex; flex-direction:column; gap:14px;}
.proof-img{width:100%; max-height:300px; object-fit:contain; border-radius:18px; background:var(--fill);}
.badge{
  width:64px; height:64px; border-radius:50%; align-self:center;
  display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:800; color:#fff;
}
.badge-ok{background:var(--ok);}
.badge-ko{background:var(--ko);}
.verdict-t{font-size:22px; font-weight:800; letter-spacing:-.8px; text-align:center;}

/* landing */
.landing{min-height:90vh; display:flex; flex-direction:column; justify-content:center; gap:16px; padding:8px 4px; position:relative;}
.land-title{font-size:46px; font-weight:900; letter-spacing:-2px; padding-left:4px;}
.land-title2{font-size:34px; font-weight:900; letter-spacing:-1.5px;}
.land-art{min-height:250px; display:flex; flex-direction:column; justify-content:flex-end;}
.land-art-txt{font-size:34px; font-weight:800; letter-spacing:-1.2px; line-height:1.05; text-shadow:0 2px 18px rgba(0,0,0,.2);}
.land-feats{display:flex; flex-direction:column; gap:11px; padding:4px;}
.feat{font-size:14.5px; line-height:1.5; color:var(--label); font-weight:500;}
.feat b{color:var(--ink); font-weight:700;}
.land-field{text-align:center; font-size:17px; padding:15px; border-radius:18px;}
.land-close{position:absolute; top:18px; left:4px; background:var(--card); box-shadow:0 2px 10px rgba(0,0,0,.06);}

.foot{margin-top:24px; display:flex; flex-direction:column; gap:8px; align-items:center; font-size:12px;}
.logout{opacity:.7;}

/* ===== mode sombre ===== */
.head-right{display:flex; align-items:center; gap:10px; flex-shrink:0;}
.circle-btn.theme{width:40px; height:40px; background:var(--card); color:var(--ink); font-size:15px; box-shadow:0 2px 10px rgba(0,0,0,.06);}
.app.dark{
  --bg:#0D0B0E; --card:#19161B; --ink:#F5F3F4; --label:#8A8590;
  --sep:rgba(255,255,255,.09); --fill:rgba(255,255,255,.07);
  --glass:rgba(255,255,255,.055); --glass-b:rgba(255,255,255,.13);
  background:
    radial-gradient(620px 320px at 85% -90px, rgba(255,90,46,.20), transparent 60%),
    radial-gradient(520px 320px at -5% 32%, rgba(158,42,255,.15), transparent 55%),
    radial-gradient(480px 300px at 100% 78%, rgba(255,46,99,.12), transparent 55%),
    var(--bg);
}
.dark .card{
  box-shadow:0 14px 36px rgba(0,0,0,.42), inset 0 1px 0 rgba(255,255,255,.09);
}
.dark .avatar{box-shadow:0 6px 18px rgba(0,0,0,.35);}
.dark .sheet{background:rgba(25,22,27,.78);}
.dark .circle-btn.theme{background:var(--glass); border:1px solid var(--glass-b); box-shadow:none;}
.dark .btn-black, .dark .circle-btn.black{background:#F4F4F6; color:#0B0B0C;}
.dark .check-on{background:#F4F4F6; border-color:#F4F4F6; color:#0B0B0C;}
.dark .check{border-color:rgba(255,255,255,.22); background:var(--card);}
.dark .chip-on{background:#F4F4F6; color:#0B0B0C; border-color:#F4F4F6;}
.dark .field:focus{border-color:#F4F4F6;}
.dark .btn-ghost{background:transparent;}
.dark .sel option{background:#17171A; color:var(--ink);}
.dark .bot-head{fill:#232327; stroke:#F4F4F6;}
.dark .bot-ant{stroke:#F4F4F6;}
.dark .bot-eye{fill:#F4F4F6;}
.dark .bot-tip{fill:#FF5A2E;}
.dark .coach-star{color:#FF7A52;}
.dark .overlay{background:rgba(0,0,0,.6);}
.dark .land-close{box-shadow:none;}
.dark button:focus-visible, .dark input:focus-visible, .dark select:focus-visible{outline-color:#F4F4F6;}
`;
