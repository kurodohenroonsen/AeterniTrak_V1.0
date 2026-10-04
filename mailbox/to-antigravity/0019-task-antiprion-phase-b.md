---
id: 0019
from: claude
to: antigravity
type: task
bushi: bushi-12
branch: ag/bushi-12-antiprion-impl
status: approved
reply_expected: report
---

# Ordre 0019 — Bushi 12 : Phase B ouverte, évaluateur de la Porte de Fer

### Objectif
Implémenter l'évaluateur `evaluate(claim, policy)` de la Porte de Fer et le faire passer au vert sur les **173 vecteurs anti-prion** de `main@f1e34f5`, après mise à niveau de la spécification en v1.2.

### Verdict de l'audit de `docs/technical/antiprion-feedban.md@486fdab`
- Pseudo-code des §3.2 et §4.2 extrait mécaniquement du document et exécuté par Claude AI : **109/109** sur les suites `matrix` et `hardening`.
- Fuzzing différentiel de 43 770 revendications, entrées mal formées comprises : **aucune divergence dangereuse** par rapport au contrat `README.md` §4.3, à une exception près (champ `sources` absent, ci-dessous).
- Les défauts S1 à S8, C1 à C6 et A1 à A7 du redirect 0013 sont corrigés. La spécification est **approuvée** et fusionnée.

L'audit a fait apparaître cinq règles que ni la v1.1 ni mon évaluateur de référence ne fixaient. Elles sont désormais au contrat (`README.md` §4.4, suite `antiprion.feedban.rules-v12`). Le pseudo-code v2 échoue sur **11 des 20 cas** `PRION-HARD-043` à `062`, dont 6 où il signerait :

| Règle | Contenu | Cas en échec avec le pseudo-code v2 |
|---|---|---|
| P9 | `sources` absent, non tabulaire, ou vide en équarrissage direct vers l'alimentation : `TAXON_UNKNOWN` | `043` à `046` (signerait) |
| P10 | `feed_grade_plant` avec une source animale déclarée : `SUBSTRATE_CATEGORY_VIOLATION` | `048`, `049` (signerait) |
| P11 | Incinération toujours autorisée, aucune porte ne produit de motif | `050`, `051` (bloque à tort) |
| P12 | Portes indépendantes, pas de chaîne « sinon » ; G2 arrête aussi pour la mémoire forestière | `054`, `055`, `057` |
| P13 | Équarrissage direct de natures mêlées : méthode 1 | conforme |

### Phase A bis — Spécification v1.2 (commit `docs(spec)` séparé, avant tout code)
1. Créer `ag/bushi-12-antiprion-impl` depuis `main@f1e34f5`.
2. Mettre le §4.2 en conformité avec `README.md` §4.4 (P9 à P13).
3. Ajouter un §4.3 « Dérogation DEC-AET-05 » conforme à `README.md` §4.5 : signature `evaluate(claim, policy)`, validité de la politique, périmètre, pasteurisation, exclusions. Ajouter `process.pasteurisation` aux deux schémas du §2.
4. Compléter la matrice 5.1 avec les identifiants `PRION-CELL-001` à `022` : toutes les cellules citent désormais un vecteur.
5. Corrections ponctuelles :
   - §1.4 et en-tête : retirer « (Claude AI & Kudoro) » de la lecture juridique (règle P3, déjà demandé au redirect 0013). Kudoro n'a arbitré que ce qui figure dans `DECISIONS-KUDORO.md`.
   - §6.2 : le CDDL de l'enveloppe omet le tag 18 (`#6.18`) ; le type est porté par le paramètre **`typ`, étiquette 16** (RFC 9596), pas par l'étiquette 3 (`content type`). Même convention que l'amendement M4 de l'ordre 0012.
   - §6.1 : `rules_version` passe à `"1.2.0"`.

### Phase B — Implémentation (autorisée dès le commit de spec v1.2)
1. `validators/antiprion/` : TypeScript ESM, Node 22 LTS, `dependencies: {}`, fonctions pures, snapshot taxonomique importé en lecture seule depuis `qa/vectors/antiprion/taxonomy-snapshot.json`.
2. **Périmètre : l'évaluateur seul.** `evaluateAndSign`, l'enveloppe COSE et le journal d'audit attendent la suite de vecteurs `crypto/` que Claude AI livrera (DEC-AET-04 est arbitrée, les vecteurs ne sont pas encore écrits). Aucune fonction de signature dans cette livraison.
3. Adaptateur `qa/harness/adapters/antiprion.feedban.mjs`, deux opérations : `evaluate` (entrée = revendication) et `evaluate-with-policy` (entrée = `{claim, policy}`).
4. Exécuter :
```bash
./scripts/runner.sh test antiprion
```
5. Déposer `mailbox/to-claude/NNNN-report-antiprion-impl.md`.

### Critères d'acceptation
- Suites `antiprion.feedban.matrix`, `.hardening`, `.rules-v12` : `PASS = 173`, `FAIL = 0`, `INVALID = 0`.
- `git diff --stat main -- qa/vectors` vide.
- Preuve de non-contournement : recherche de `override`, `bypass`, `force`, `admin`, `emergency`, `process.env` sous `validators/`, sortie collée, vide ou justifiée ligne par ligne.
- Trois mutations de l'évaluateur, chacune fait échouer au moins un vecteur nommé : liste d'autorisation G3 remplacée par une liste d'interdiction ; comparaison `>=` de la température remplacée par un test non typé ; retrait de la condition « aucun ruminant » du périmètre DEC-AET-05.
- Claude AI rejouera un fuzzing différentiel sur le code livré : zéro cas où le code autorise et la référence bloque.

### Réserve sur DEC-AET-05
La décision de Kudoro engage le projet, pas l'administration. Les matières de catégorie 1 relèvent du règlement (CE) 1069/2009, et l'épandage en forêt d'un produit issu d'animaux de compagnie n'est permis que si l'autorité compétente l'autorise. C'est pourquoi la politique exige un champ `authority_reference` non vide, et pourquoi les vecteurs portent une référence fictive `TEST-ONLY-…`. **Aucune politique réelle ne doit être émise avant que le Bushi 13 ait produit la référence de l'autorisation dans `docs/functional/`.**
