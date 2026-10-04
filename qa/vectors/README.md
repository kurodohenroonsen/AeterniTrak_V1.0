# `qa/vectors/` — Contrat des Vecteurs de Conformité AeterniTrak V1.0

> **Autorité** : Claude AI (Master Verifier) spécifie et approuve ; le Bushi 16 (QA) propose en `draft` et construit le harnais ; les autres Bushi **ne modifient jamais** un vecteur `approved` (cf. `bushi/bushi-16-qa-testvectors.md` §5 : modification uniquement sur arbitrage de Kudoro).
> **Principe** : *le vecteur précède le code*. Un vecteur rouge est l'état normal d'un chantier avant implémentation.

---

## 1. Arborescence et nommage

```
qa/vectors/
├── README.md                          ce contrat
├── schema/vector-suite.schema.json    schéma JSON (draft 2020-12) de toute suite
├── core/      *.vectors.json          CBOR déterministe, JCS, CID SHA-256, profil mémoriel
├── crypto/    *.vectors.json          Ed25519 (RFC 8032), ES256, COSE_Sign1, enveloppes AES-GCM
├── hardware/  *.vectors.json          séquences APDU ISO 7816-4, plan mémoire ACOSJ 92k / T4T 32k
├── filiere/   *.vectors.json          relevés d'autoclave méthode 1, certificats de lots
└── antiprion/ *.vectors.json          matrice feed-ban + taxonomy-snapshot.json
```

- Un fichier = **une suite** = **un adaptateur** d'implémentation : `<domaine>/<sujet>.vectors.json`.
- Identifiant de cas : `DOMAINE-SOUSTYPE-NNN`, unique dans tout le dépôt, **jamais réattribué** (un cas retiré garde son numéro, marqué dans `notes`).
- `status: approved` = officiel et immuable. `status: draft` = proposé par le Bushi 16, modifiable jusqu'à l'approbation de Claude AI (via un rapport `NNNN-report-qa-*.md`).

## 2. Format d'une suite

Validé par `schema/vector-suite.schema.json`. Champs obligatoires : `suite`, `version`, `issued_by`, `issued_at`, `status`, `spec`, `adapter`, `description`, `cases[]`. Chaque cas : `id`, `title`, `op`, `input`, `expect`, `rule` (+ `tags`, `notes` facultatifs).

| `op`             | `input`                               | `expect`                                  | Domaine        |
| ---------------- | ------------------------------------- | ----------------------------------------- | -------------- |
| `encode`         | élément AVN (§3)                      | `{hex, len, sha256}`                      | core.cbor      |
| `decode`         | `{hex}`                               | `{item}` (élément AVN)                    | core.cbor      |
| `reject-encode`  | élément AVN                           | `{error}`                                 | core.cbor      |
| `reject-decode`  | `{hex}`                               | `{error}`                                 | core.cbor      |
| `canonicalize`   | valeur JSON                           | `{utf8, hex, len, sha256}`                | core.jcs       |
| `evaluate`       | `BatchClaim` v1                       | `{verdict, reasons[], signature_permitted}` | antiprion      |
| `evaluate-with-policy` | `{claim, policy}` (`policy` peut être `null`) | `{verdict, reasons[], signature_permitted}` | antiprion |
| `sign` / `verify` | défini par la suite crypto (à venir) | défini par la suite                       | crypto         |

La comparaison est **exacte et binaire** : octets identiques, listes ordonnées identiques, codes d'erreur identiques. Aucune tolérance, aucune normalisation côté harnais.

## 3. Notation AVN (AeterniTrak Vector Notation) des éléments CBOR

Le JSON ne sait pas représenter nativement tous les éléments CBOR ; l'AVN comble l'écart sans ambiguïté :

| JSON (AVN)                              | Élément CBOR                                             |
| --------------------------------------- | -------------------------------------------------------- |
| nombre entier (\|n\| ≤ 2^53)            | entier (types majeurs 0/1), forme la plus courte          |
| `{"$int": "18446744073709551615"}`      | entier hors plage JSON sûre (jusqu'à ±2^64)               |
| chaîne                                   | texte UTF-8 **NFC** (type majeur 3)                       |
| `{"$bytes": "0a0b"}`                    | chaîne d'octets (type majeur 2), hexadécimal minuscule    |
| tableau                                  | tableau à longueur définie (type majeur 4)                |
| objet                                    | carte à clés texte (type majeur 5), **triée par l'encodeur** |
| `{"$map": [[k, v], ...]}`               | carte à clés quelconques ; l'ordre d'entrée est arbitraire |
| `{"$tag": 100, "$value": -9004}`        | élément étiqueté (type majeur 6)                          |
| `true` / `false` / `null`                | valeurs simples 21 / 20 / 22                              |
| `{"$float": 1.5}`                       | flottant — **interdit par le profil AeterniCore** (rejet) |

Règles d'encodage imposées (RFC 8949 §4.2.1 *Core Deterministic Encoding* + profil AeterniCore v1) :
1. forme la plus courte pour tous les entiers et longueurs ;
2. longueurs définies uniquement ;
3. clés de carte triées par ordre **bytewise** de leur encodage déterministe (⚠️ pas l'ordre « longueur d'abord » de la RFC 7049, cf. `CBOR-REJ-013`) ;
4. pas de clé dupliquée ;
5. profil : pas de flottant, pas d'`undefined`, pas de valeur simple non assignée, tags autorisés dans la charge utile = `1` (epoch secondes) et `100` (RFC 8943, jours depuis 1970-01-01, négatifs admis) ;
6. textes UTF-8 valides et **déjà normalisés NFC** : l'encodeur refuse (il ne normalise pas en silence), le décodeur strict refuse aussi.

## 4. Registres de codes

### 4.1 Erreurs CBOR (suite `core.cbor.deterministic`)
`ERR_CBOR_NOT_SHORTEST` · `ERR_CBOR_INDEFINITE_LENGTH` · `ERR_CBOR_MAP_UNSORTED` · `ERR_CBOR_DUPLICATE_KEY` · `ERR_CBOR_TRAILING_BYTES` · `ERR_CBOR_TRUNCATED` · `ERR_CBOR_MALFORMED` · `ERR_CBOR_INVALID_UTF8` · `ERR_CBOR_TEXT_NOT_NFC` · `ERR_CBOR_UNSUPPORTED_TYPE` · `ERR_CBOR_UNSUPPORTED_TAG` · `ERR_CBOR_TAG_CONTENT`

### 4.2 Motifs du validateur anti-prion (suite `antiprion.feedban.matrix`), dans l'ordre des portes
| Porte | Motif                              | Base                                                     |
| ----- | ---------------------------------- | -------------------------------------------------------- |
| G0    | `DESTINATION_UNSUPPORTED`          | DEFAULT_DENY : `use` hors énumération v1                 |
| G0    | `TARGET_UNSPECIFIED`               | DEFAULT_DENY : route alimentaire sans espèce cible       |
| G1    | `TAXON_UNKNOWN`                    | DEFAULT_DENY : taxid absent du snapshot ou nom sans taxid |
| G1    | `TAXON_RANK_ABOVE_SPECIES`         | DEFAULT_DENY : rang supérieur à l'espèce                 |
| G2    | `HUMAN_REMAINS_ROUTE_PROHIBITED`   | restes humains : aucune route alimentaire ni technique   |
| G3    | `SUBSTRATE_CATEGORY_VIOLATION`     | règl. 1069/2009 art. 12-13 ; règl. 2017/893 (substrats)  |
| G3    | `CATEGORY_DESTINATION_PROHIBITED`  | cat. 1 → engrais interdit                                |
| G3    | `DEROGATION_REQUIRED`              | mémoire forestière : aucune dérogation codée en dur      |
| G4    | `PENTOBARBITAL_POSITIVE` / `PENTOBARBITAL_NOT_TESTED` | PROTOCOL.md §5 profil Compagnie       |
| G5    | `FEED_BAN_RUMINANT_SOURCE`         | règl. 999/2001 annexe IV ch. I                           |
| G6    | `FEED_BAN_RUMINANT_TARGET`         | règl. 999/2001 annexe IV ch. I                           |
| G7    | `FEED_BAN_INTRA_SPECIES_VIOLATION` | règl. 1069/2009 art. 11(1)(a)(b) — **Règle d'Or**        |
| G8    | `FEED_BAN_INTRA_GROUP_VIOLATION`   | règl. 999/2001 annexe IV ch. II (2021/1372) : porcins↔porcins, volailles↔volailles |
| G8    | `SOURCE_GROUP_NOT_AUTHORISED` / `TARGET_GROUP_NOT_AUTHORISED` | dérogations 2021/1372 limitatives |
| G9    | `TREATMENT_NOT_PROVEN`             | règl. 142/2011 annexe IV (méthodes 1-5, 7 ; méthode 1 = 133 °C / 3 bar / 20 min) |

`reasons` est **exhaustif** (toutes les portes sont évaluées, sauf arrêt anticipé G0 `DESTINATION_UNSUPPORTED` et G2 restes humains) et **ordonné** par porte. `signature_permitted = (reasons == [])`. L'oracle de signature Ed25519 ne doit **physiquement** pas pouvoir signer une revendication dont `signature_permitted` est faux.

### 4.3 Précisions v1.1 des portes (suite `antiprion.feedban.hardening`, 42 cas)

Ces précisions ne modifient aucun des 67 vecteurs de la matrice ; elles ferment les chemins que la matrice seule ne discriminait pas (audit du cycle 0002).

- **P1 — Exhaustivité** : seuls `DESTINATION_UNSUPPORTED` (G0) et la porte G2 arrêtent l'évaluation. `TARGET_UNSPECIFIED` et les erreurs G1 **n'arrêtent pas** : les portes suivantes s'évaluent sur les taxons résolus.
- **P2 — G1 cumulatif** : toutes les sources, l'insecte et toutes les cibles sont examinés ; `TAXON_UNKNOWN` puis `TAXON_RANK_ABOVE_SPECIES` sont rapportés chacun au plus une fois.
- **P3 — G2, restes humains** : la protection se déclenche si un taxon source est 9606 **ou** si `material_class = human_remains` **ou** si `origin_profile = human`. Un taxid omis ou falsifié ne la lève pas. Seule l'incinération est autorisée ; la mémoire forestière renvoie `DEROGATION_REQUIRED`.
- **P4 — G3, listes d'autorisation** : jamais de liste d'interdiction. Alimentation : catégorie 3 **et** classe de matière autorisée pour la route (équarrissage direct : `slaughter_byproduct`, `feed_grade_plant` ; bioconversion par insectes : `feed_grade_plant`) **et** route connue. Technique, engrais, mémoire forestière : catégorie ∈ {1, 2, 3} et classe de matière connue. L'incinération reste toujours ouverte, y compris catégorie inconnue.
- **P5 — G8, groupes sources par liste positive** : `feed` : porcins, volailles, insectes, poissons. `aquaculture_feed` : les mêmes plus équidés et lagomorphes (non-ruminants d'élevage). Tout autre groupe, y compris un groupe futur du snapshot : `SOURCE_GROUP_NOT_AUTHORISED`.
- **P6 — G9, méthode selon la nature de la protéine** (règl. (UE) 142/2011, annexe X, ch. II, sect. 1) : la nature est « insecte » dès que la route est la bioconversion, sinon celle des sources. Mammifères (ou nature indéterminée) : **méthode 1 exclusivement**. Volailles et insectes : méthodes 1 à 5 ou 7. Poisson seul : méthodes 1 à 7. Dans tous les cas : `evidence_sha256` de 64 hexadécimaux minuscules ; pour la méthode 1, température, pression et durée numériques et au-dessus des seuils.
- **P7 — G9, périmètre** : G9 ne s'applique qu'aux destinations qui exigent un traitement. Technique et engrais en catégorie 1 ou 2 : méthode 1 prouvée, aucune autre. Incinération et mémoire forestière : G9 ne produit aucun motif.
- **P8 — Typage strict** : un taxid est un entier JSON ; les paramètres de traitement sont des nombres. Une valeur absente ou d'un autre type n'est jamais conforme par défaut (piège JavaScript : `undefined < 133` vaut `false`).

### 4.4 Précisions v1.2 des portes (suite `antiprion.feedban.rules-v12`, cas `PRION-HARD-043` à `062` et `PRION-CELL-*`)

- **P9 — Sources déclarées** : `substrate.sources` doit être un tableau. Absent ou d'un autre type : `TAXON_UNKNOWN` (hors incinération). En alimentation par équarrissage direct, un tableau vide vaut aussi `TAXON_UNKNOWN` : une PAT sans espèce déclarée viderait la Règle d'Or de son objet.
- **P10 — Cohérence de la déclaration** : la classe `feed_grade_plant` exclut toute source animale déclarée ; sinon `SUBSTRATE_CATEGORY_VIOLATION` (hors incinération).
- **P11 — Incinération** : toujours autorisée. Après G0, aucune porte ne produit de motif pour `incineration`, y compris taxon inconnu, catégorie absente ou animal de compagnie non testé. Un cadavre non identifié doit toujours pouvoir être détruit.
- **P12 — Portes indépendantes** : chaque motif s'évalue seul, sans chaîne « sinon » (`SUBSTRATE_CATEGORY_VIOLATION` et `CATEGORY_DESTINATION_PROHIBITED` peuvent coexister ; une catégorie invalide vers technique ou engrais exige aussi la méthode 1). G2 arrête l'évaluation pour toute destination, mémoire forestière comprise.
- **P13 — Natures mêlées** : en équarrissage direct, un lot qui n'est ni entièrement volaille ni entièrement poisson relève de la méthode 1 exclusivement.

### 4.5 Dérogation DEC-AET-05 (cas `PRION-DEROG-*`, opération `evaluate-with-policy`)

Décision de Kudoro du 2026-10-04 : mémoire forestière privée pour les animaux de compagnie de catégorie 1, LFA négatifs. La Porte de Fer ne code aucune dérogation en dur : elle reçoit une **politique** en second argument, et sans politique valide le comportement v1 est inchangé (`DEROGATION_REQUIRED`).

- **Politique valide** : objet dont `policy_id = "DEC-AET-05"`, avec `legal_basis` et `authority_reference` non vides. La vérification de la signature de la politique relève de l'hôte (Bushi 02) ; la Porte ne voit qu'une politique déjà authentifiée.
- **Périmètre** (toutes les conditions) : `origin_profile = "pet"`, catégorie 1, classe `carcass`, route `insect_bioconversion`, au moins une source, aucune erreur G1, aucun ruminant parmi les sources. Hors périmètre : `DEROGATION_REQUIRED`.
- **Dans le périmètre** : G4 s'applique (LFA négatif exigé) ; G9 exige `process.pasteurisation = {core_temp_c ≥ 70, minutes ≥ 60, evidence_sha256}` numériques et prouvés, sinon `TREATMENT_NOT_PROVEN`.
- **Jamais couvert** : les restes humains (G2 passe avant), et toute autre destination. La politique n'ouvre ni l'alimentation ni l'engrais.
- **Limite** : une décision interne au projet n'est pas une autorisation administrative. Le champ `authority_reference` est là pour porter la référence de l'autorisation réelle de l'autorité compétente ; les vecteurs utilisent une référence fictive `TEST-ONLY-…`.

## 5. Harnais (`./scripts/runner.sh test`) — sémantique attendue (chantier QA-001, Bushi 16)

- Charge toutes les suites `qa/vectors/**/*.vectors.json`, les valide contre le schéma (échec = `INVALID`, exit 2).
- Vérifie l'**auto-cohérence** de chaque attente binaire : `sha256(hex) == sha256` et `len(hex)/2 == len` (échec = `INVALID`).
- Pour chaque suite, cherche `qa/harness/adapters/<adapter>.mjs`. **Absent ⇒ tous les cas de la suite sont `RED`** (état normal avant implémentation). Présent ⇒ chaque cas est `PASS` ou `FAIL`.
- Sortie : une ligne par cas `<PASS|FAIL|RED|INVALID> <id> <titre>`, puis un bloc récapitulatif par suite et un total ; copie intégrale dans `mailbox/state/out.txt` et rapport JSON `qa/reports/<AAAA-MM-JJ>-<sha-court>.json`.
- Codes de sortie : `0` = aucun `FAIL` ni `INVALID` (des `RED` sont admis) ; `1` = au moins un `FAIL` ; `2` = au moins un `INVALID`. Un `FAIL` interdit toute fusion sur `main`.
- Le décodeur de contrôle (CBOR) et le canoniseur de contrôle (JCS) utilisés par le harnais sont écrits par le **Bushi 16**, indépendamment du Bushi 01, et ne partagent aucun code avec `core/`.
- Règle 7 bis : le harnais ne s'exécute que par `./scripts/runner.sh test [glob]`, jamais par une commande ad hoc.

## 6. Cycle de vie d'un vecteur

1. Claude AI dépose des vecteurs `approved` (branche `tests/*` → `main`) **ou** le Bushi 16 dépose des vecteurs `draft` sur `ag/bushi-16-qa` et les signale dans `mailbox/to-claude/NNNN-report-qa-*.md`.
2. Claude AI relit, corrige éventuellement par un `redirect`, puis approuve (`status: approved`) et fusionne sur `main`.
3. Un vecteur `approved` ne change plus. Une erreur avérée se traite par un **nouveau** cas (nouveau numéro) et le retrait du cas erroné avec `notes` explicative, sur arbitrage de Kudoro consigné dans `DECISIONS-KUDORO.md`.
