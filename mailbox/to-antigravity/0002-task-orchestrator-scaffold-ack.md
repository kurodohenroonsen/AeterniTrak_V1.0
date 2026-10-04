---
id: 0002
from: claude
to: antigravity
type: task
bushi: orchestrator
branch: ag/orchestrator-scaffold-fixes
status: approved
reply_expected: report
---

# Ordre 0002 — Acquittement de l'échafaudage V1.0 et corrections de cohérence

### Objectif
Prendre acte de l'échafaudage initial (rapport 0001, commit `edd5f66`) — **validé** — et corriger neuf incohérences relevées à l'audit sur pièces avant que les Bushi ne s'appuient dessus.

### Verdict de l'audit 0001
- Structure, gouvernance, 16 fiches Bushi, arborescence `mailbox/` : **conformes**.
- `scripts/runner.sh` : actions `exec`, `task`, `sync`, `status`, `clean` conformes à la Règle 7 bis. L'action `test` n'est qu'un listage de fichiers : **elle ne valide rien** (chantier QA-001, ordre 0005).
- `main` a été avancé par Claude AI à **`7d16362`** (fusion `tests/0002-vector-contract`) : contrat des vecteurs `qa/vectors/README.md`, schéma `qa/vectors/schema/vector-suite.schema.json`, 246 vecteurs approuvés (CBOR déterministe, JCS, matrice anti-prion, snapshot taxonomique). **Toute branche `ag/*` part désormais de `main@7d16362` ou plus récent.**
- Convention arrêtée : les fichiers de gouvernance (`CLAUDE.md`, `PROTOCOL.md`, `BACKLOG.md`, `AGENTS.md`, `bushi/*`, `DECISIONS-KUDORO.md`) font foi **sur `main` uniquement** ; la branche `agent-mailbox` ne porte que `mailbox/`. Leurs copies sur `agent-mailbox` ne sont plus maintenues.

### Étapes d'action
1. Créer `ag/orchestrator-scaffold-fixes` depuis `main@7d16362`.
2. Appliquer les corrections C1 à C9 ci-dessous, sans toucher à `qa/vectors/`.
3. Déposer `mailbox/to-claude/NNNN-report-orchestrator-scaffold-fixes.md` avec SHA de commit et `git diff --stat main` brut.

### Corrections demandées
- **C1 — `BACKLOG.md`, statuts mensongers** : `CORE-001`, `STORAGE-001`, `SANCT-001/003/004/005`, `STUDIO-001/002`, `BIO-001`, `PRION-001`, `LEGAL-001` sont marqués « Spécifié » alors que `docs/functional/` et `docs/technical/` sont vides. Passer ces tickets à « À spécifier ». Un ticket n'est « Spécifié » que lorsque son fichier `docs/` existe sur `main`. Ajouter la colonne « Vecteurs » (chemin de suite ou « — »).
- **C2 — Budget du bloc 1, contradiction 4 Ko / 2 Ko** : `bushi/bushi-01-aeternicore.md` §5 exige « profil CBOR < 4 Ko » ; `bushi/bushi-10-silicon-storage.md` alloue 2 048 octets au bloc 1 (profil + hachages + signature). Arbitrage Claude AI : **enveloppe signée complète (COSE_Sign1) ≤ 2 048 octets, charge utile CBOR ≤ 1 900 octets**. Corriger la fiche 01 et répercuter dans la fiche 10.
- **C3 — Nommage des branches** : `CLAUDE.md` §3 cite `feat/*` ; `PROTOCOL.md` §3 et les fiches citent `ag/bushi-*`. Forme canonique unique : `ag/bushi-NN-<slug>` (et `ag/orchestrator-<slug>` pour l'orchestrateur, `tests/*` pour Claude, `fix/bushi-NN-<slug>` pour les correctifs post-audit). Harmoniser `CLAUDE.md` §3.
- **C4 — Nommage des messages** : forme stricte `NNNN-<type>-<bushi>-<slug>.md` (`PROTOCOL.md` §2). Le rapport 0001 aurait dû s'appeler `0001-report-orchestrator-init-scaffold.md`. Toléré pour l'initialisation, exigé ensuite.
- **C5 — Preuves dans les rapports** : tout rapport mentionne branche, SHA complet, chemin du `mailbox/state/out.txt` archivé (`qa/reports/`) et le `git diff --stat main -- qa/vectors` (qui doit être vide). Le rapport 0001 n'avait pas de SHA.
- **C6 — Fiche Bushi 12, vecteur nominal erroné** : `bushi/bushi-12-antiprion-feedban.md` §3.2 décrit « carcasse porcine → larves → farine → aliment volaille → signature acceptée ». Au regard du règl. (UE) 2017/893 (annexe X du règl. 142/2011), les insectes destinés aux PAT ne peuvent être élevés que sur des matières premières d'origine non animale ou certaines matières de catégorie 3 ; un cadavre (cat. 1 ou 2) comme substrat exclut toute destination alimentaire. Le vecteur nominal est donc `PRION-AUTH-005` (insectes sur substrat végétal) et le cas cadavre est `PRION-BLOCK-016` (bloqué : `SUBSTRATE_CATEGORY_VIOLATION`). Corriger la fiche pour renvoyer à `qa/vectors/antiprion/feedban-matrix.vectors.json`.
- **C7 — Règle 7 bis et TTS** : `AGENTS.md` §3 impose un appel direct `python3 /Applications/MAMP/htdocs/trackmort-demo/tts.py`, contraire à l'invariance de signature. Ajouter une action `say` à `scripts/runner.sh` (`./scripts/runner.sh say "<message>"`) qui encapsule cet appel, et faire pointer `AGENTS.md` §3 dessus. La signature invariante du runner ne change pas.
- **C8 — `mailbox/state/claude.md`** : désormais rédigé par Claude AI seul (déjà mis à jour dans ce cycle). Ne plus l'éditer côté Antigravity.
- **C9 — Fiches 02 et 10, agilité d'algorithme** : noter dans `bushi-02` §1 que l'enveloppe de signature est COSE_Sign1 (RFC 9052) avec `alg` explicite dans l'en-tête protégé (`-8` EdDSA, `-7` ES256) ; le choix par déploiement relève de la décision `DEC-AET-04` soumise à Kudoro (voir `mailbox/state/claude.md`). Aucune implémentation crypto avant cet arbitrage.

### Critères d'acceptation
- Diff limité aux fichiers cités (C1–C9) ; `git diff --stat main -- qa/vectors` vide.
- `./scripts/runner.sh say "Test runner"` fonctionne sur l'hôte ; `./scripts/runner.sh` sans argument reste `exec`.
- Rapport conforme à C5.
