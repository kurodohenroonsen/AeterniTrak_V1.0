---
id: 0005
from: claude
to: antigravity
type: task
bushi: bushi-16
branch: ag/bushi-16-qa
status: approved
reply_expected: report
---

# Ordre 0005 — Bushi 16 (QA) : harnais de validation des vecteurs (`QA-001`, P0)

### Objectif
Remplacer l'action `test` factice de `scripts/runner.sh` par un harnais réel qui exécute toutes les suites `qa/vectors/**/*.vectors.json` selon la sémantique de `qa/vectors/README.md` §5, sans changer la signature invariante du runner (Règle 7 bis). Ce harnais est le **prérequis** des ordres 0003 et 0004 : il doit être livré en premier.

### Références
- `qa/vectors/README.md` §2 (format), §3 (notation AVN), §4 (registres), §5 (sémantique du harnais) — `main@7d16362`.
- `qa/vectors/schema/vector-suite.schema.json`.

### Étapes d'action
1. Créer `ag/bushi-16-qa` depuis `main@7d16362`.
2. Implémenter `qa/harness/run.mjs` (Node 22 LTS, ESM) :
   - **Chargement** : découverte des suites, validation contre le schéma. Dépendance de développement tolérée : `ajv` **épinglé en version exacte** avec `package-lock.json` et empreintes d'intégrité ; aucune autre dépendance.
   - **Auto-cohérence des attentes** : pour tout `expect` binaire, `sha256(hex) == sha256` et `len(hex)/2 == len`, sinon `INVALID`.
   - **Décodeur CBOR de contrôle et canoniseur JCS de contrôle écrits par le Bushi 16**, indépendants de `core/` (aucun import partagé) : pour chaque cas `encode`, le décodeur de contrôle doit retrouver l'élément AVN d'entrée depuis `hex` ; pour chaque `canonicalize`, le canoniseur de contrôle doit reproduire `utf8`. Un écart est rapporté `INVALID` avec le détail : c'est le contrôle croisé des vecteurs eux-mêmes.
   - **Adaptateurs** : chargement dynamique de `qa/harness/adapters/<adapter>.mjs` exportant `run(op, input) → résultat` ; absent ⇒ tous les cas de la suite `RED`.
   - **Comparaison exacte** (octets, chaînes, listes ordonnées, codes d'erreur) ; `PASS` / `FAIL` avec diff lisible (attendu / obtenu) sur `FAIL`.
   - **Sorties** : une ligne par cas `<PASS|FAIL|RED|INVALID> <id> <titre>`, récapitulatif par suite et total ; rapport JSON `qa/reports/<AAAA-MM-JJ>-<sha-court>.json` ; copie intégrale dans `mailbox/state/out.txt`.
   - **Codes de sortie** : `0` si aucun `FAIL` ni `INVALID` (les `RED` sont admis), `1` si au moins un `FAIL`, `2` si au moins un `INVALID`.
   - **Filtre** : `./scripts/runner.sh test <glob>` restreint aux suites dont le chemin ou le nom contient `<glob>` (`core`, `antiprion`, …).
   - **Auto-test** : `./scripts/runner.sh test --selftest` copie une suite dans un répertoire temporaire, corrompt un octet d'un `hex`, un `sha256` et une liste `reasons`, et doit rapporter exactement trois `INVALID`/`FAIL` puis sortir en `2`.
3. Modifier **uniquement** le corps du `case "test")` de `scripts/runner.sh` pour appeler `node qa/harness/run.mjs "$@"` ; signature d'appel inchangée.
4. Exécuter et archiver :
```bash
./scripts/runner.sh test
./scripts/runner.sh test --selftest
```
5. Déposer `mailbox/to-claude/NNNN-report-qa-harness.md` : branche, SHA, sorties brutes non tronquées, `git diff --stat main -- qa/vectors` (vide).

### Critères d'acceptation
- Sur `main@7d16362` + branche : `RED = 246`, `PASS = 0`, `FAIL = 0`, `INVALID = 0`, exit `0`.
- Le contrôle croisé (décodeur/canoniseur de contrôle) valide les 246 attentes sans `INVALID`. Si un vecteur approuvé est mis en défaut par le contrôle, **ne pas le modifier** : déposer `NNNN-question-qa-*.md` avec la preuve ; l'arbitrage appartient à Claude AI puis Kudoro.
- `--selftest` détecte les trois corruptions.
- `package.json` : `dependencies: {}` ; `devDependencies` limitées à `ajv` épinglé.

### Interdits
- Toute tolérance de comparaison (normalisation, trim, tri côté harnais).
- Tout code partagé entre le harnais de contrôle et `core/`.
- Toute modification sous `qa/vectors/`.
