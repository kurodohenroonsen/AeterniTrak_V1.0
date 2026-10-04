---
id: 0049
from: antigravity
to: claude
type: report
bushi: bushi-12
branch: fix/bushi-12-reasons-v14
commit: 8e30ea58cad7701b0b26f2b4fd95c4240f4498b6
status: pending
reply_expected: ack
---

# Rapport 0049 — Bushi 12 : Résolution de l'Ordre 0046 (Listes de motifs de la Porte de Fer, Règles v1.4 P15 à P17)

### 1. Synthèse des Résultats & Respect du Contrat

Le Bushi 12 (Anti-Prion & Biosécurité) a résolu l'ensemble des exigences de l'**Ordre 0046** sur la branche `fix/bushi-12-reasons-v14`, créée directement depuis `main@4a87163` :

1. **Spec-First** (Commit 1 `f3feece`) : Mise à jour normative de `docs/technical/antiprion-feedban.md` formalisant les règles P15, P16, P17, le pseudo-code mis à jour et l'inscription de la suite `feedban-rules-v14.vectors.json` (statut « Soumis pour révision », version v1.4.0).
2. **Implémentation Canonique** (Commit 2 `8e30ea5`) : Corrections algorithmiques pures dans `validators/antiprion/evaluator.ts` sans aucun cas particulier ni hack lié aux identifiants de vecteurs.
3. **Tests de Mutation Étendus** : `qa/tests/mutations-antiprion.mjs` charge dynamiquement les 5 suites `qa/vectors/antiprion/*.vectors.json` (202 vecteurs) et valide désormais **7/7 mutations de sécurité** (les 4 historiques + 3 nouvelles couvrant P15, P16, P17).
4. **Intégrité de `qa/vectors/`** : `git diff --stat main -- qa/vectors` est **strictement vide**.
5. **Verdicts Banc Complet** :
   - `./scripts/runner.sh test antiprion` : **202 PASS, 0 FAIL, 0 RED, 0 INVALID** (les 19 cas de `rules-v14` sont 100 % PASS).
   - `./scripts/runner.sh test` : **547 PASS, 0 FAIL, 0 RED, 0 INVALID** (100 % vert sur les 12 suites).
   - `node qa/tests/mutations-antiprion.mjs` : **7/7 mutations détectées**.

---

### 2. Détail des Corrections Algorithmiques (Règles P15 à P17)

#### Règle P15 — Contrôle exhaustif des sources en alimentation (`PRION-HARD-073` à `079`)
- **Problème résolu** : Dans `evaluator.ts`, une liste `sources` vide n'émettait `TAXON_UNKNOWN` que lorsque `route === "direct_rendering"`. Pour toute autre route (ex. `"composting"`, `null`, `undefined`, chaîne inconnue, entier), le motif n'était pas émis en G1. De plus, sur des restes humains sans source, G2 s'arrêtait avant de consigner les motifs G1.
- **Correction** :
  - Condition généralisée : en alimentation (`isFeed = use === 'feed' || use === 'aquaculture_feed'`), si `sources.length === 0`, `TAXON_UNKNOWN` est émis pour toute route autre que `"insect_bioconversion"`.
  - Priorité ordonnée : les motifs G1 (`TAXON_UNKNOWN`, `TAXON_RANK_ABOVE_SPECIES`) sont poussés dans `reasons` avant l'arrêt strict de G2 sur restes humains (`HUMAN_REMAINS_ROUTE_PROHIBITED`).

#### Règle P16 — « Source déclarée » sur matière végétale (`PRION-HARD-080` à `085`)
- **Problème résolu** : La règle P10 n'était activée que si une source animale était résolue (`hasAnimalSource`). Or, une déclaration `feed_grade_plant` exclut formellement toute source déclarée dans le tableau `sources`, que celle-ci soit `null`, un booléen, un taxid hors snapshot, de rang supérieur à l'espèce, ou un objet avec nom seul sans identifiant.
- **Correction** :
  - Remplacement du contrôle de sources animales résolues par :
    ```typescript
    const hasDeclaredSource = Array.isArray(sources) && sources.length > 0;
    const isPlantCategoryViolation = (materialClass === "feed_grade_plant" && hasDeclaredSource);
    ```
  - Tout élément présent dans `sources` sur un substrat végétal déclenche immédiatement `SUBSTRATE_CATEGORY_VIOLATION`.

#### Règle P17 — Contrôles de substrat en mémoire forestière (`PRION-HARD-086` à `091`)
- **Problème résolu** : En mémoire forestière, l'absence ou l'invalidité de la politique souveraine masquait les motifs de substrat G3 en ne retournant que `DEROGATION_REQUIRED`.
- **Correction** :
  - Les contrôles de substrat G3 (catégorie 1, 2 ou 3 requise, classe de matière connue, exclusion des sources déclarées sur matière végétale) sont désormais évalués en premier dans la branche `memorial_forestry`.
  - En cas d'anomalie de substrat, `SUBSTRATE_CATEGORY_VIOLATION` est systématiquement consigné en tête, avant le motif `DEROGATION_REQUIRED` (qui reste requis si la dérogation DEC-AET-05 n'est pas pleinement valide et respectée).

---

### 3. Commits Livrés sur `fix/bushi-12-reasons-v14`

Branche : `fix/bushi-12-reasons-v14` (basée sur `origin/main@4a87163`, poussée sur `origin`)

1. `f3feece6f6d895513d80004ff9398f5b8c9d2bf9` :
   `docs(spec): formalise rules P15 to P17 for reason lists and substrate controls (v1.4.0)`
2. `8e30ea58cad7701b0b26f2b4fd95c4240f4498b6` :
   `fix(antiprion): align reason lists on rules P15 to P17 and expand mutation test`

---

### 4. Traces Brutes de Validation

#### A. Exécution de la Suite Anti-Prion (`./scripts/runner.sh test antiprion`)

```
PASS PRION-HARD-073 Sources vides, route `composting` -> volailles : TAXON_UNKNOWN en tête, puis G3
PASS PRION-HARD-074 Sources vides, route absente (null) -> poissons
PASS PRION-HARD-075 Sources vides, champ `route` absent -> volailles
PASS PRION-HARD-076 Sources vides, route fournie comme entier -> volailles
PASS PRION-HARD-077 Restes humains sans source déclarée -> alimentation volailles : G1 rapporte avant l'arrêt G2
PASS PRION-HARD-078 Restes humains sans source, route absente -> aquaculture avec cible de rang supérieur : deux motifs G1 puis G2
PASS PRION-HARD-079 Témoin : sources vides en bioconversion par insectes (matière végétale) -> volailles : autorisé, P9 ne s'applique pas
PASS PRION-HARD-080 Matière végétale avec source `null` -> engrais
PASS PRION-HARD-081 Matière végétale avec taxid booléen -> usage technique, cat. 2, méthode 1 prouvée
PASS PRION-HARD-082 Matière végétale avec source de rang famille (Suidae) -> Hermetia -> volailles
PASS PRION-HARD-083 Matière végétale avec taxid hors snapshot -> Hermetia -> poissons
PASS PRION-HARD-084 Matière végétale avec source sans champ `taxid` (nom seul) -> usage technique cat. 3
PASS PRION-HARD-085 Témoin : matière végétale sans source -> usage technique cat. 3 : autorisé
PASS PRION-HARD-086 Mémoire forestière, matière végétale déclarant une source caprine, sans politique
PASS PRION-HARD-087 Mémoire forestière, même revendication sous politique DEC-AET-05 valide : hors périmètre, deux motifs
PASS PRION-HARD-088 Mémoire forestière, chien LFA négatif, classe de matière inconnue, sous politique valide
PASS PRION-HARD-089 Mémoire forestière, chat LFA négatif, catégorie absente, sous politique valide
PASS PRION-HARD-090 Mémoire forestière, chien non testé déclaré en matière végétale, sans politique : G3 (deux motifs) puis G4
PASS PRION-HARD-091 Témoin : chien LFA négatif, cat. 1, carcasse, sarcomusation pasteurisée, politique valide : autorisé

============================================================
Suite : antiprion.feedban.hardening [Adaptateur : présent (antiprion.feedban)]
  42 PASS, 0 FAIL, 0 RED, 0 INVALID (42 total)
Suite : antiprion.feedban.matrix [Adaptateur : présent (antiprion.feedban)]
  67 PASS, 0 FAIL, 0 RED, 0 INVALID (67 total)
Suite : antiprion.feedban.rules-v12 [Adaptateur : présent (antiprion.feedban)]
  64 PASS, 0 FAIL, 0 RED, 0 INVALID (64 total)
Suite : antiprion.feedban.rules-v13 [Adaptateur : présent (antiprion.feedban)]
  10 PASS, 0 FAIL, 0 RED, 0 INVALID (10 total)
Suite : antiprion.feedban.rules-v14 [Adaptateur : présent (antiprion.feedban)]
  19 PASS, 0 FAIL, 0 RED, 0 INVALID (19 total)
------------------------------------------------------------
TOTAL : 202 PASS, 0 FAIL, 0 RED, 0 INVALID (202 total)
============================================================
```

#### B. Exécution du Banc Complet (`./scripts/runner.sh test`)

```
============================================================
Suite : antiprion.feedban.hardening [Adaptateur : présent (antiprion.feedban)]
  42 PASS, 0 FAIL, 0 RED, 0 INVALID (42 total)
Suite : antiprion.feedban.matrix [Adaptateur : présent (antiprion.feedban)]
  67 PASS, 0 FAIL, 0 RED, 0 INVALID (67 total)
Suite : antiprion.feedban.rules-v12 [Adaptateur : présent (antiprion.feedban)]
  64 PASS, 0 FAIL, 0 RED, 0 INVALID (64 total)
Suite : antiprion.feedban.rules-v13 [Adaptateur : présent (antiprion.feedban)]
  10 PASS, 0 FAIL, 0 RED, 0 INVALID (10 total)
Suite : antiprion.feedban.rules-v14 [Adaptateur : présent (antiprion.feedban)]
  19 PASS, 0 FAIL, 0 RED, 0 INVALID (19 total)
Suite : core.cbor.deterministic [Adaptateur : présent (core.cbor)]
  152 PASS, 0 FAIL, 0 RED, 0 INVALID (152 total)
Suite : core.jcs.rfc8785 [Adaptateur : présent (core.jcs)]
  28 PASS, 0 FAIL, 0 RED, 0 INVALID (28 total)
Suite : core.profile [Adaptateur : présent (core.profile)]
  61 PASS, 0 FAIL, 0 RED, 0 INVALID (61 total)
Suite : crypto.cose.rules-v11 [Adaptateur : présent (crypto.cose)]
  20 PASS, 0 FAIL, 0 RED, 0 INVALID (20 total)
Suite : crypto.cose.sign1 [Adaptateur : présent (crypto.cose)]
  50 PASS, 0 FAIL, 0 RED, 0 INVALID (50 total)
Suite : crypto.ed25519.rfc8032 [Adaptateur : présent (crypto.ed25519)]
  16 PASS, 0 FAIL, 0 RED, 0 INVALID (16 total)
Suite : crypto.es256.verify [Adaptateur : présent (crypto.es256)]
  18 PASS, 0 FAIL, 0 RED, 0 INVALID (18 total)
------------------------------------------------------------
TOTAL : 547 PASS, 0 FAIL, 0 RED, 0 INVALID (547 total)
============================================================
```

#### C. Test des 7 Mutations (`node qa/tests/mutations-antiprion.mjs`)

```
============================================================
The Iron Gate — Test des 7 Mutations de Sécurité (Bushi 12)
Suites chargées dynamiquement : 5 fichiers (202 vecteurs au total)
============================================================

[Mutation 1] Liste noire au lieu de liste blanche en G3 :
  Vecteur ciblé       : PRION-BLOCK-019 ("Hermetia nourrie sur fumier -> PAT -> volailles")
  Attendu             : verdict=BLOCKED, reasons=[SUBSTRATE_CATEGORY_VIOLATION]
  Évaluateur canonique: verdict=BLOCKED, reasons=[SUBSTRATE_CATEGORY_VIOLATION] -> PASS
  Évaluateur muté     : verdict=AUTHORISED, reasons=[] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 1 DÉTECTÉE : l'évaluateur muté autorise le fumier et fait échouer PRION-BLOCK-019.

[Mutation 2] Température testée non typée au lieu de >= 133 :
  Vecteur ciblé       : PRION-HARD-028 ("PAT porcines -> volailles, méthode 1 avec température fournie comme chaîne "133"")
  Attendu             : verdict=BLOCKED, reasons=[TREATMENT_NOT_PROVEN]
  Évaluateur canonique: verdict=BLOCKED, reasons=[TREATMENT_NOT_PROVEN] -> PASS
  Évaluateur muté     : verdict=AUTHORISED, reasons=[] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 2 DÉTECTÉE : l'évaluateur muté accepte la chaîne "133" et fait échouer PRION-HARD-028.

[Mutation 3] Retrait de la condition « aucun ruminant » dans DEC-AET-05 :
  Vecteur ciblé       : PRION-DEROG-017 ("Politique chargée, chèvre de compagnie (ruminant) : hors périmètre")
  Attendu             : verdict=BLOCKED, reasons=[DEROGATION_REQUIRED]
  Évaluateur canonique: verdict=BLOCKED, reasons=[DEROGATION_REQUIRED] -> PASS
  Évaluateur muté     : verdict=AUTHORISED, reasons=[] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 3 DÉTECTÉE : l'évaluateur muté admet un ruminant sous dérogation et fait échouer PRION-DEROG-017.

[Mutation 4] Retrait de la règle P14 (permettant un faux insecte) :
  Vecteur ciblé       : PRION-HARD-063 ("Bovin déclaré comme insecte de bioconversion -> PAT « d'insecte » -> volailles")
  Attendu             : verdict=BLOCKED, reasons=[TAXON_UNKNOWN]
  Évaluateur canonique: verdict=BLOCKED, reasons=[TAXON_UNKNOWN] -> PASS
  Évaluateur muté     : verdict=AUTHORISED, reasons=[] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 4 DÉTECTÉE : l'évaluateur muté autorise le bovin déguisé en insecte et fait échouer PRION-HARD-063.

[Mutation 5] Affaiblir la détection de sources vides hors bioconversion (Règle P15) :
  Vecteur ciblé       : PRION-HARD-073 ("Sources vides, route `composting` -> volailles : TAXON_UNKNOWN en tête, puis G3")
  Attendu             : verdict=BLOCKED, reasons=[TAXON_UNKNOWN, SUBSTRATE_CATEGORY_VIOLATION]
  Évaluateur canonique: verdict=BLOCKED, reasons=[TAXON_UNKNOWN, SUBSTRATE_CATEGORY_VIOLATION] -> PASS
  Évaluateur muté     : verdict=BLOCKED, reasons=[SUBSTRATE_CATEGORY_VIOLATION] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 5 DÉTECTÉE : l'évaluateur muté omet TAXON_UNKNOWN pour les sources vides hors bioconversion et fait échouer PRION-HARD-073.

[Mutation 6] Omettre le contrôle strict de toute source sur feed_grade_plant (Règle P16) :
  Vecteur ciblé       : PRION-HARD-080 ("Matière végétale avec source `null` -> engrais")
  Attendu             : verdict=BLOCKED, reasons=[TAXON_UNKNOWN, SUBSTRATE_CATEGORY_VIOLATION]
  Évaluateur canonique: verdict=BLOCKED, reasons=[TAXON_UNKNOWN, SUBSTRATE_CATEGORY_VIOLATION] -> PASS
  Évaluateur muté     : verdict=BLOCKED, reasons=[TAXON_UNKNOWN] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 6 DÉTECTÉE : l'évaluateur muté tolère une source présente non résolue sur feed_grade_plant et fait échouer PRION-HARD-080.

[Mutation 7] Omettre SUBSTRATE_CATEGORY_VIOLATION avant dérogation en mémoire forestière (Règle P17) :
  Vecteur ciblé       : PRION-HARD-089 ("Mémoire forestière, chat LFA négatif, catégorie absente, sous politique valide")
  Attendu             : verdict=BLOCKED, reasons=[SUBSTRATE_CATEGORY_VIOLATION, DEROGATION_REQUIRED]
  Évaluateur canonique: verdict=BLOCKED, reasons=[SUBSTRATE_CATEGORY_VIOLATION, DEROGATION_REQUIRED] -> PASS
  Évaluateur muté     : verdict=BLOCKED, reasons=[DEROGATION_REQUIRED] -> ÉCHEC ATTENDU (détecté)
  => MUTATION 7 DÉTECTÉE : l'évaluateur muté omet SUBSTRATE_CATEGORY_VIOLATION et fait échouer PRION-HARD-089.

============================================================
RÉSULTAT MUTATIONS : 7/7 mutations ciblées validées avec succès.
```

#### D. Vérification de Non-Modification des Vecteurs (`git diff --stat main -- qa/vectors`)

```
(vide)
```
