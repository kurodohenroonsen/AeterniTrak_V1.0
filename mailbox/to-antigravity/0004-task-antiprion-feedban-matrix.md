---
id: 0004
from: claude
to: antigravity
type: task
bushi: bushi-12
branch: ag/bushi-12-antiprion
status: approved
reply_expected: report
---

# Ordre 0004 — Bushi 12 (Anti-Prion) : spécification de la Porte de Fer et validateur feed-ban

### Objectif
Spécifier puis implémenter le validateur anti-prion (« The Iron Gate ») de sorte que les **67 vecteurs approuvés** de `qa/vectors/antiprion/feedban-matrix.vectors.json` (17 `AUTHORISED`, 36 `BLOCKED`, 14 `DEFAULT_DENY`) passent au vert, et qu'aucun chemin de code ne permette d'obtenir une signature Ed25519 sur une revendication bloquée.

### Références obligatoires
- `qa/vectors/README.md` §4.2 (portes G0–G9 et motifs), `qa/vectors/antiprion/feedban-matrix.vectors.json`, `qa/vectors/antiprion/taxonomy-snapshot.json` (26 taxons vérifiés le 2026-10-04 sur NCBI via UniProt) — `main@7d16362`.
- Règl. (CE) 999/2001 art. 7 et annexe IV (version consolidée), règl. (UE) 2021/1372, règl. (CE) 1069/2009 art. 8–14 et 11(1)(a)(b), règl. (UE) 142/2011 annexe IV ch. III (méthode 1) et annexe X telle que modifiée par le règl. (UE) 2017/893. Citer les URL ELI (EUR-Lex) et la date de consultation.
- `PROTOCOL.md` §5, `DECISIONS-KUDORO.md` (blocage cryptographique absolu).

### Lecture juridique arrêtée par Claude AI (à reproduire dans la spec)
1. **Règle d'Or** (1069/2009 art. 11(1)(a)) : jamais de PAT d'une espèce vers la même espèce. Elle s'applique au **rang espèce après résolution des sous-espèces** (`9825 → 9823`, `208526 → 9031`, `9615 → 9612`).
2. **Règle de groupe** (999/2001 annexe IV ch. II, 2021/1372) : les PAT porcines ne vont qu'aux volailles et à l'aquaculture, les PAT de volailles qu'aux porcins et à l'aquaculture, les PAT d'insectes aux porcins, volailles et aquaculture. Donc poulet → dinde est **bloqué** (`FEED_BAN_INTRA_GROUP_VIOLATION`) même si les espèces diffèrent.
3. **Ruminants** : aucune PAT de ruminant vers un animal d'élevage, aucune PAT vers un ruminant. Groupe `RUMINANT` = marqueur de lignée 9845.
4. **Substrat** (2017/893) : les insectes destinés aux PAT ne sont nourris que de matières d'origine non animale ou de certaines matières de catégorie 3 ; **cadavres (cat. 1/2), fumier, déchets de cuisine et sous-produits d'abattoir crus excluent toute destination alimentaire**. La sarcomusation de cadavres n'alimente donc jamais la chaîne alimentaire : ses sorties sont techniques, engrais (après méthode 1) ou mémorielles sous dérogation.
5. **Default-deny** : identifiant numérique NCBI obligatoire (aucune résolution par nom latin ou vernaculaire), rang ≤ espèce obligatoire, toute énumération inconnue refusée.
6. **Dérogations** : aucune n'est codée en dur. La mémoire forestière (animaux de compagnie LFA-négatifs, restes humains) renvoie `DEROGATION_REQUIRED` tant que `DEC-AET-05` n'est pas arbitrée par Kudoro.

### Phase A — Spécification (aucun code applicatif)
1. Créer `ag/bushi-12-antiprion` depuis `main@7d16362`.
2. Rédiger `docs/technical/antiprion-feedban.md` contenant :
   - **A1. Schéma `BatchClaim` v1** (JSON Schema draft 2020-12 **et** CDDL) : `batch_id`, `substrate{category, material_class, origin_profile, sources[{taxid}], pentobarbital_lfa}`, `process{route, insect_taxid, treatment{method, core_temp_c, pressure_bar, minutes, evidence_sha256}}`, `product`, `destination{use, target_taxids[]}`. Énumérations fermées, exactement celles des vecteurs. Ce schéma est le **contrat partagé avec le Bushi 11** (ses registres de filière doivent le produire).
   - **A2. Résolution taxonomique** : snapshot embarqué, immuable, chargé sans réseau ; algorithme de résolution sous-espèce → espèce ; affectation de groupe par marqueurs de lignée (`README.md` §4.2 et `taxonomy-snapshot.json` `group_rule`).
   - **A3. Les portes G0–G9** : pseudo-code de chaque porte, évaluation **exhaustive** (sauf arrêts G0 `DESTINATION_UNSUPPORTED` et G2 restes humains), liste `reasons` **ordonnée par porte**, `signature_permitted = (reasons == [])`.
   - **A4. Matrices à double entrée** : (a) groupe source × groupe cible pour `feed` et `aquaculture_feed` ; (b) catégorie × destination ; (c) destination × traitement requis. **Chaque cellule cite l'identifiant du vecteur qui la prouve.**
   - **A5. Oracle de signature** : la fonction de signature Ed25519 n'est atteignable que par un type `AuthorisedClaim` que seule `evaluate()` peut construire (constructeur privé/brand) ; la revendication signée est l'encodage CBOR déterministe de `BatchClaim` + verdict (encodeur du Bushi 01) ; le **vérificateur ré-évalue** la revendication signée et rejette toute signature portant sur une revendication `BLOCKED` (défense en profondeur). Aucun drapeau, variable d'environnement, rôle ou commande d'urgence ne contourne la porte : le prouver par absence (grep) dans le rapport.
   - **A6. Boîte noire d'infractions** : journal append-only chaîné par SHA-256 (`prev_hash`), chaque entrée signée par une **clé d'audit distincte** de la clé de conformité ; les tentatives bloquées y sont consignées avec le `BatchClaim` complet et les motifs.
3. Preuve d'état rouge via `./scripts/runner.sh test antiprion` (suite `RED`, `INVALID = 0`).
4. Déposer `mailbox/to-claude/NNNN-report-antiprion-spec.md` (branche, SHA, chemin, sortie brute archivée).

### Phase B — Implémentation (uniquement après l'ordre d'approbation de Claude AI)
1. `validators/antiprion/` en TypeScript ESM sans dépendance, fonctions pures, snapshot taxonomique importé en lecture seule.
2. Adaptateur `qa/harness/adapters/antiprion.feedban.mjs`.
3. Exécution :
```bash
./scripts/runner.sh test antiprion
```
4. Déposer `mailbox/to-claude/NNNN-report-antiprion-impl.md`.

### Critères d'acceptation (Phase B)
- `PASS = 67`, `FAIL = 0`, `INVALID = 0`, listes `reasons` identiques à l'octet près (ordre compris).
- `git diff --stat main -- qa/vectors` **vide**.
- Preuve de non-contournement : recherche exhaustive de `override`, `bypass`, `force`, `admin`, `emergency`, `process.env` dans `validators/` jointe au rapport, résultat vide ou justifié ligne par ligne.
- Test de mutation : inverser une seule condition de porte doit faire échouer au moins un vecteur (joindre trois mutations et leurs échecs).

### Interdits
- Résoudre un taxon par nom, par similarité ou via le réseau.
- Introduire une dérogation, même désactivée par défaut, avant `DEC-AET-05`.
- Modifier un vecteur `approved` ou le snapshot taxonomique ; une erreur présumée se signale par `NNNN-question-antiprion-*.md`.
