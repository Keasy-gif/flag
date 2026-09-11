# FLAG — Pris en flag de taffer 🏁

Planifie ta journée, prouve chaque bloc en photo (vérifiée par IA), monte en grade.

## Ce qu'il y a dedans
- `src/App.jsx` — toute l'app (design éditorial sombre, coach IA, scan photo, grades, rival, salle commune, bilan, FLAG+ démo)
- `api/claude.js` — fonction serverless qui appelle l'API Anthropic. **La clé reste côté serveur.**
- PWA prête : installable sur l'écran d'accueil (icône FLAG incluse)

## Lancer en 10 minutes

### 0. Prérequis (comptes gratuits)
- [github.com](https://github.com) — héberge le code
- [vercel.com](https://vercel.com) — héberge le site (connecte-toi AVEC ton compte GitHub)
- [console.anthropic.com](https://console.anthropic.com) — clé API pour l'IA (~5 € de crédit)
- Bonus étudiant : [GitHub Student Pack](https://education.github.com/pack) — Codespaces boostés gratuits

### 1. Mettre le code sur GitHub
Sur github.com → **New repository** → nom `flag` → Create.
Puis **Add file → Upload files** → glisse TOUT le contenu de ce dossier → Commit.

### 2. Coder depuis n'importe quel ordi (Codespaces)
Sur ton repo → bouton vert **Code → Codespaces → Create codespace**.
VS Code s'ouvre dans le navigateur. Dans le terminal :
```bash
npm install
npm run dev
```
L'app tourne. Tu peux ouvrir ce même Codespace depuis n'importe quel ordinateur.
(Claude Code marche aussi dedans : `npm install -g @anthropic-ai/claude-code` puis `claude`)

⚠️ En dev local/Codespace, `/api/claude` n'existe pas (c'est une fonction Vercel) —
le coach répondra une erreur réseau. C'est normal : l'IA marche sur le site déployé.
Pour tester l'IA en dev : `npm i -g vercel` puis `vercel dev` (avec la clé dans `.env`).

### 3. Mettre en ligne (Vercel)
1. vercel.com → **Add New → Project** → importe ton repo `flag`
2. Avant de déployer : **Environment Variables** → ajoute
   `ANTHROPIC_API_KEY` = ta clé (commence par `sk-ant-...`)
3. **Deploy** → tu obtiens `https://flag-xxx.vercel.app`

Ensuite : chaque `git push` sur GitHub redéploie le site automatiquement.

### 4. Installer sur téléphone
Ouvre l'URL sur ton tel → menu du navigateur → **Ajouter à l'écran d'accueil**.
Icône FLAG, plein écran, caméra et micro fonctionnels (HTTPS).

## Limites connues de cette v1 web (volontaires)
- **Salle commune** : tu te vois toi-même ; les AUTRES utilisateurs nécessitent un
  backend temps réel → phase 2 avec Supabase (table `live_sessions` + Realtime)
- **Comptes** : pseudo local (par appareil) → phase 2 : Supabase Auth
- **FLAG+** : démo sans paiement → phase 2 : Stripe (web) / RevenueCat (stores)
- **Coût IA** : ~0,01 € par coach/scan → si tu partages le lien large, ajoute une
  limite de requêtes par jour dans `api/claude.js`

## Phase 2 (quand la v1 vit)
Supabase (auth + realtime + photos) → app mobile Expo/React Native → App Store.
