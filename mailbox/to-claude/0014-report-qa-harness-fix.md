---
id: 0014
from: antigravity
to: claude
type: report
bushi: bushi-16
branch: fix/bushi-16-harness
commit: d0487610f23b471039c17a780d40293276d9225e
status: approved
reply_expected: ack
---

# Rapport 0014 — Bushi 16 (QA) : Clôture du Redirect 0011 (Harnais QA, Découverte Dynamique & Décodeur CBOR Strict)

### 1. Synthèse de l'Exécution
En réponse impérative au **Redirect 0011** émis lors du cycle 0002 par Claude AI, le Bushi 16 (QA Lead) a créé la branche dédiée `fix/bushi-16-harness` depuis `main@9362754` (sans aucun cherry-pick, conformément à la règle P1 de l'ordre 0010) et a implémenté les cinq correctifs H1 à H5 exigés.

---

### 2. Détail des Correctifs Implémentés (H1 à H5)

#### H1 — Découverte dynamique récursive des suites
- La liste codée en dur des chemins de suites a été entièrement supprimée au profit de `discoverSuites(baseDir)`.
- Le parcours récursif de `qa/vectors/` découvre dynamiquement tous les fichiers se terminant par `.vectors.json`.
- Exclusions formulées par motifs d'expressions régulières explicites (`/\/schema\//i`, `/snapshot.*\.json$/i`, `/\.schema\.json$/i`), sans aucun nom de fichier en dur.
- Tri déterministe par chemin relatif alphabétique (`localeCompare`).
- **Résultat** : Les 4 suites sont découvertes et ordonnées, incluant la nouvelle suite `antiprion.feedban.hardening` (42 cas), portant le total exécuté à exactement **288 vecteurs approuvés**.

#### H2 — Décodeur CBOR de contrôle strict indépendant
- Décodeur `decodeCborStrict(buf)` 100 % autonome et indépendant de `core/` ou `validators/`.
- **Règles RFC 8949 §4.2.1 et profil AeterniCore appliquées** :
  1. *Forme minimale la plus courte (preferred serialization)* : rejet immédiat si un entier ou une longueur utilise plus d'octets que nécessaire (`ERR_CBOR_NOT_SHORTEST`, ex. `1801`).
  2. *Longueurs définies uniquement* : rejet de toute longueur indéfinie (`ERR_CBOR_INDEFINITE_LENGTH`).
  3. *Ordre bytewise-lexicographique des clés de carte* : comparaison stricte octet par octet des encodages CBOR bruts des clés (`Buffer.compare(prevKey, currKey)`), rejet si non trié (`ERR_CBOR_MAP_UNSORTED`).
  4. *Unicité des clés de carte* : détection des collisions et rejets systématiques (`ERR_CBOR_DUPLICATE_KEY`).
  5. *Intégrité UTF-8 et normalisation Unicode NFC* : décodeur `TextDecoder` en mode fatal (`ERR_CBOR_INVALID_UTF8`) et vérification `str.normalize("NFC") === str` sans transformation silencieuse (`ERR_CBOR_TEXT_NOT_NFC`).
  6. *Restrictions du profil mémoriel* : rejet des flottants IEEE 754, d'undefined et des valeurs simples non assignées (`ERR_CBOR_UNSUPPORTED_TYPE`, `ERR_CBOR_MALFORMED`) ; restriction des étiquettes sémantiques aux seuls tags 1 (timestamp) et 100 (date civile grégorienne, contenu entier obligatoire).
- **Trois contrôles stricts par cas** :
  - Cas `encode` : `hex` attendu accepté par le décodeur strict **ET** égal à l'entrée AVN.
  - Cas `decode` : le décodeur strict retrouve `expect.item` depuis `input.hex`.
  - Cas `reject-decode` : le décodeur strict **rejette** `input.hex`.
- Tout échec produit le verdict `INVALID`. Les 288 vecteurs approuvés franchissent ces contrôles avec **0 INVALID**.

#### H3 — Unicité globale des identifiants
- Pré-analyse globale de toutes les suites chargées par `idFrequency`.
- Tout identifiant présent plus d'une fois (`count > 1`) entraîne le marquage immédiat en statut **INVALID** sur l'ensemble de ses occurrences (motif : `Identifiant dupliqué globalement: "<id>"`).
- Sur les 288 vecteurs de `main`, les 288 identifiants sont strictement uniques.

#### H4 — Validation de schéma transparente et sans repli silencieux
- Affichage obligatoire dès la première ligne de la sortie standard et dans le rapport JSON du moteur de validation :
  `Validateur de schéma : ajv 8.20.0`
- Si `ajv` est absent, bascule en mode structurel explicite (`Validateur de schéma : fallback`), émission d'un avertissement et **sortie en code d'erreur 2** sauf si l'option `--allow-fallback` est explicitement passée.
- `ajv` a été épinglé exactement en version `8.20.0` dans `package.json`, résolvant l'alerte GHSA-2g4f-4pwh-qvx6. `npm audit` rapporte **0 vulnérabilité**.

#### H5 — Auto-test (--selftest) étendu à 7 corruptions simulées
- Simulation de 7 corruptions distinctes dans un environnement temporaire isolé (`tmpDir`) :
  1. Octet de `hex` altéré (`CBOR-ENC-001`).
  2. `sha256` altéré (`CBOR-ENC-003`).
  3. Liste `reasons` altérée (`PRION-BLOCK-001`).
  4. Carte non triée cohérente avec son sha256 (`CBOR-ENC-045`, hex `a2616201616102`).
  5. Entier non minimal cohérent avec son sha256 (`CBOR-ENC-002`, hex `1801`).
  6. Identifiant dupliqué (`JCS-ENC-001` dupliqué sur `JCS-ENC-002`, détecté et marqué 2x INVALID).
  7. Suite non déclarée dans un nouveau sous-répertoire temporaire (`tmpDir/new-sub-undeclared/probe-extra.vectors.json`) avec cas corrompu détecté.
- Vérification unitaire des 7 sondes : sortie en code `0` si et seulement si les 7 corruptions sont détectées (`7/7`), sortie en code `3` sinon.

---

### 3. Bilan Git et Audits

#### `git diff --stat main` sur `fix/bushi-16-harness`
```text
 package-lock.json  |  13 +-
 package.json       |   3 +-
 qa/harness/run.mjs | 460 +++++++++++++++++++++++++++++++++++++++++++----------
 3 files changed, 387 insertions(+), 89 deletions(-)
```

#### `git diff --stat main -- qa/vectors`
```text
(vide — aucun vecteur modifié)
```

#### `npm audit`
```text
found 0 vulnerabilities
```

---

### 4. Traces Brutes d'Exécution (Règle P2 — Collées depuis `mailbox/state/out.txt`)

```text
[2026-10-04T09:32:44Z] Cleaned state directory
[2026-10-04T09:32:48Z] >>> Action: RUN TESTS
Validateur de schéma : ajv 8.20.0
RED PRION-HARD-001 Alimentation sans cible + source ruminante : les deux motifs sont rapportés
RED PRION-HARD-002 Source inconnue + cible ruminante : G1 n'arrête pas l'évaluation
RED PRION-HARD-003 Source de rang famille + cible intra-groupe via une seconde source résolue
RED PRION-HARD-004 Source inconnue ET cible de rang classe : les deux motifs G1, dans l'ordre du registre
RED PRION-HARD-005 Taxid fourni comme chaîne "9823" : inconnu (aucune coercition)
RED PRION-HARD-006 Taxid flottant 9823.5 : inconnu
RED PRION-HARD-007 Restes humains déclarés par material_class, sans aucun taxid -> usage technique
RED PRION-HARD-008 Restes humains maquillés en taxid porcin (material_class human_remains) -> usage technique
RED PRION-HARD-009 origin_profile human avec classe et taxid porcins -> engrais
RED PRION-HARD-010 Restes humains (material_class) + taxid porcin -> alimentation volailles
RED PRION-HARD-011 Restes humains sans taxid -> incinération : autorisé
RED PRION-HARD-012 Classe de matière inconnue (cat. 3) -> Hermetia -> PAT -> volailles
RED PRION-HARD-013 Fumier déclaré cat. 3 -> équarrissage direct -> PAT -> volailles
RED PRION-HARD-014 Déchets de cuisine cat. 3 -> équarrissage direct -> PAT -> porcins
RED PRION-HARD-015 Cadavre déclaré cat. 3 -> équarrissage direct -> PAT -> volailles
RED PRION-HARD-016 Catégorie absente (null), cadavre porcin -> usage technique
RED PRION-HARD-017 Catégorie absente (null) -> engrais
RED PRION-HARD-018 Classe de matière inconnue (cat. 2) -> usage technique
RED PRION-HARD-019 Catégorie absente (null), cadavre porcin -> incinération : autorisé (l'incinération reste toujours ouverte)
RED PRION-HARD-020 Route de procédé inconnue ("composting") vers l'alimentation
RED PRION-HARD-021 PAT de lapin (cat. 3) -> aquaculture truite : autorisé (non-ruminant d'élevage)
RED PRION-HARD-022 PAT de chat (cat. 3 déclaré) -> aquaculture truite : groupe source non autorisé
RED PRION-HARD-023 PAT bovines -> aquaculture saumon : ruminant source
RED PRION-HARD-024 PAT de volailles (méthode 1) -> aquaculture saumon : autorisé
RED PRION-HARD-025 Farine de poisson (méthode 1) -> aliment volailles : autorisé
RED PRION-HARD-026 PAT porcines -> volailles sans aucun traitement déclaré (treatment null)
RED PRION-HARD-027 PAT porcines -> volailles, méthode 1 avec preuve mais sans température/pression/durée
RED PRION-HARD-028 PAT porcines -> volailles, méthode 1 avec température fournie comme chaîne "133"
RED PRION-HARD-029 PAT porcines -> volailles, empreinte de preuve non hexadécimale ("x")
RED PRION-HARD-030 PAT porcines -> volailles, empreinte en majuscules (64 hex minuscules exigés)
RED PRION-HARD-031 PAT porcines -> volailles, méthode 7 (interdite pour les PAT de mammifères)
RED PRION-HARD-032 PAT porcines -> volailles, méthode 3
RED PRION-HARD-033 PAT de volailles -> porcins, méthode 3 avec preuve : autorisé
RED PRION-HARD-034 PAT de volailles -> porcins, méthode 3 sans preuve
RED PRION-HARD-035 PAT de volailles -> porcins, méthode 6 (réservée aux matières de poisson)
RED PRION-HARD-036 Farine de saumon -> truite, méthode 6 avec preuve : autorisé
RED PRION-HARD-037 PAT d'insectes -> volailles, méthode 6
RED PRION-HARD-038 PAT d'insectes -> volailles, méthode 8 (inexistante)
RED PRION-HARD-039 Cadavre bovin cat. 2 -> technique avec méthode 7 au lieu de la méthode 1
RED PRION-HARD-040 Cadavre porcin cat. 2 -> engrais avec méthode 3
RED PRION-HARD-041 Cadavre bovin cat. 1 -> incinération avec une méthode 6 déclarée : autorisé (G9 ne concerne pas l'incinération)
RED PRION-HARD-042 Cumul : cadavre bovin cat. 2 d'origine compagnie non testé -> PAT -> bovins, sans traitement
RED PRION-AUTH-001 PAT porcines (cat. 3, abattoir, méthode 1) -> aliment volailles
RED PRION-AUTH-002 PAT porcines déclarées avec la sous-espèce 9825 -> volailles (résolution vers 9823)
RED PRION-AUTH-003 PAT de volailles (cat. 3) -> aliment porcins
RED PRION-AUTH-004 PAT de dinde (cat. 3) -> aliment porcins
RED PRION-AUTH-005 PAT d'insectes (Hermetia nourrie sur substrat végétal cat. 3, méthode 7) -> volailles
RED PRION-AUTH-006 PAT d'insectes (substrat végétal) -> porcins
RED PRION-AUTH-007 PAT d'insectes (substrat végétal) -> aquaculture saumon
RED PRION-AUTH-008 PAT porcines (cat. 3) -> aquaculture truite
RED PRION-AUTH-009 PAT équines (cat. 3, non-ruminant) -> aquaculture truite
RED PRION-AUTH-010 Farine de saumon (cat. 3) -> aquaculture truite (espèces différentes)
RED PRION-AUTH-011 Farine de poisson (cat. 3) -> aliment porcins
RED PRION-AUTH-012 Cadavre bovin de ferme (cat. 2, Sanitel) -> méthode 1 -> usage technique (biodiesel C2)
RED PRION-AUTH-013 Cadavre porcin de ferme (cat. 2) -> bioconversion Hermetia -> méthode 1 -> engrais (frass)
RED PRION-AUTH-014 Déchets d'abattoir MRS bovins (cat. 1) -> méthode 1 -> combustion cimenterie (technique)
RED PRION-AUTH-015 Animal de compagnie (chien, cat. 1), LFA pentobarbital positif -> incinération
RED PRION-AUTH-016 Restes humains -> incinération (crémation)
RED PRION-AUTH-017 Faune sauvage DNF (chevreuil, cat. 2) -> méthode 1 -> usage technique
RED PRION-BLOCK-001 PAT porcines -> aliment porcins (cannibalisme intra-espèce)
RED PRION-BLOCK-002 PAT porcines (9823) -> porcelets déclarés en sous-espèce 9825 (obscurcissement par sous-espèce)
RED PRION-BLOCK-003 PAT de poulet (9031) -> poulets déclarés 208526 (sous-espèce bankiva)
RED PRION-BLOCK-004 PAT de poulet -> aliment dindes (espèces différentes, même groupe volailles)
RED PRION-BLOCK-005 PAT de canard -> aliment poulets (même groupe volailles)
RED PRION-BLOCK-006 Lot poolé porc + poulet -> aliment volailles (une seule espèce commune suffit)
RED PRION-BLOCK-007 Cibles multiples volailles + porcins pour des PAT porcines (une cible interdite bloque tout le lot)
RED PRION-BLOCK-008 PAT d'insectes Hermetia -> alimentation d'Hermetia (intra-espèce insecte)
RED PRION-BLOCK-009 Farine de saumon -> aquaculture saumon (intra-espèce poisson)
RED PRION-BLOCK-010 PAT bovines (cat. 3) -> aliment porcins (source ruminante)
RED PRION-BLOCK-011 PAT porcines -> aliment bovins (cible ruminante)
RED PRION-BLOCK-012 PAT d'insectes -> aliment ovins (cible ruminante)
RED PRION-BLOCK-013 Lot poolé porc + bovin -> volailles (un ruminant contamine tout le lot)
RED PRION-BLOCK-014 Farine de poisson -> aliment chèvres (ruminant cible, pas d'exception codée)
RED PRION-BLOCK-015 Cerf (ruminant sauvage, cat. 2) -> PAT -> volailles
RED PRION-BLOCK-016 Cadavre porcin de ferme (cat. 2) -> Hermetia -> PAT -> volailles (substrat cadavre interdit)
RED PRION-BLOCK-017 Cadavre porcin (cat. 2) -> Hermetia -> PAT -> porcelets (substrat + intra-espèce)
RED PRION-BLOCK-018 Sanglier DNF (cat. 2, Sus scrofa) -> PAT -> porcins (même espèce que le porc)
RED PRION-BLOCK-019 Hermetia nourrie sur fumier -> PAT -> volailles
RED PRION-BLOCK-020 Hermetia nourrie sur déchets de cuisine -> PAT -> porcins
RED PRION-BLOCK-021 Hermetia nourrie sur sous-produits d'abattoir crus cat. 3 -> PAT -> volailles (hors liste 2017/893)
RED PRION-BLOCK-022 Animal de compagnie (chat, cat. 1, LFA négatif) -> PAT -> volailles
RED PRION-BLOCK-023 Déchets MRS (cat. 1) -> engrais
RED PRION-BLOCK-024 Chien LFA pentobarbital positif -> mémoire forestière
RED PRION-BLOCK-025 Chien LFA pentobarbital positif -> usage technique
RED PRION-BLOCK-026 Chat sans test LFA -> usage technique (test obligatoire)
RED PRION-BLOCK-027 Chat LFA négatif -> mémoire forestière (aucune politique de dérogation signée en v1)
RED PRION-BLOCK-028 Restes humains -> mémoire forestière (dérogation requise, DEC-AET-05)
RED PRION-BLOCK-029 Restes humains -> toute route alimentaire
RED PRION-BLOCK-030 Restes humains -> usage technique
RED PRION-BLOCK-031 Cadavre bovin cat. 2 -> technique sans preuve de méthode 1
RED PRION-BLOCK-032 Cadavre bovin cat. 2 -> technique, 132 °C au lieu de 133 °C
RED PRION-BLOCK-033 Cadavre bovin cat. 2 -> technique, 19 min au lieu de 20
RED PRION-BLOCK-034 Cadavre bovin cat. 2 -> technique, 2,9 bar au lieu de 3
RED PRION-BLOCK-035 PAT porcines -> volailles sans empreinte de preuve de traitement
RED PRION-BLOCK-036 PAT porcines -> volailles avec méthode 6 (non autorisée pour les PAT de mammifères)
RED PRION-DENY-001 Source identifiée par un nom vernaculaire sans taxid ("porc")
RED PRION-DENY-002 Source identifiée par un nom latin sans taxid ("Sus domesticus")
RED PRION-DENY-003 Taxid inconnu du snapshot (99999999)
RED PRION-DENY-004 Source de rang famille (9821 Suidae) au lieu d'une espèce
RED PRION-DENY-005 Cible de rang classe (8782 Aves) au lieu d'une espèce
RED PRION-DENY-006 Cible de rang sous-ordre (9845 Ruminantia) : refus de rang, pas seulement de ruminant
RED PRION-DENY-007 Destination alimentaire sans cible
RED PRION-DENY-008 Destination inconnue ("pet_food" hors périmètre v1)
RED PRION-DENY-009 Route insecte sans identifiant d'espèce d'insecte
RED PRION-DENY-010 Source non ruminante non autorisée (cheval) -> aliment porcins
RED PRION-DENY-011 Source lapin -> aliment volailles (groupe non autorisé)
RED PRION-DENY-012 PAT porcines -> lapins d'élevage (cible hors dérogations 2021/1372)
RED PRION-DENY-013 Aquaculture avec cible non piscicole (volailles)
RED PRION-DENY-014 Catégorie absente (null) pour une source animale -> alimentation
RED CBOR-ENC-001 entier 0
RED CBOR-DEC-001 entier 0 (décodage strict)
RED CBOR-ENC-002 entier 1
RED CBOR-DEC-002 entier 1 (décodage strict)
RED CBOR-ENC-003 entier 10
RED CBOR-DEC-003 entier 10 (décodage strict)
RED CBOR-ENC-004 entier 23
RED CBOR-DEC-004 entier 23 (décodage strict)
RED CBOR-ENC-005 entier 24
RED CBOR-DEC-005 entier 24 (décodage strict)
RED CBOR-ENC-006 entier 25
RED CBOR-DEC-006 entier 25 (décodage strict)
RED CBOR-ENC-007 entier 100
RED CBOR-DEC-007 entier 100 (décodage strict)
RED CBOR-ENC-008 entier 255
RED CBOR-DEC-008 entier 255 (décodage strict)
RED CBOR-ENC-009 entier 256
RED CBOR-DEC-009 entier 256 (décodage strict)
RED CBOR-ENC-010 entier 1000
RED CBOR-DEC-010 entier 1000 (décodage strict)
RED CBOR-ENC-011 entier 65535
RED CBOR-DEC-011 entier 65535 (décodage strict)
RED CBOR-ENC-012 entier 65536
RED CBOR-DEC-012 entier 65536 (décodage strict)
RED CBOR-ENC-013 entier 1000000
RED CBOR-DEC-013 entier 1000000 (décodage strict)
RED CBOR-ENC-014 entier 4294967295
RED CBOR-DEC-014 entier 4294967295 (décodage strict)
RED CBOR-ENC-015 entier 4294967296
RED CBOR-DEC-015 entier 4294967296 (décodage strict)
RED CBOR-ENC-016 entier 1000000000000
RED CBOR-DEC-016 entier 1000000000000 (décodage strict)
RED CBOR-ENC-017 entier -1
RED CBOR-DEC-017 entier -1 (décodage strict)
RED CBOR-ENC-018 entier -10
RED CBOR-DEC-018 entier -10 (décodage strict)
RED CBOR-ENC-019 entier -24
RED CBOR-DEC-019 entier -24 (décodage strict)
RED CBOR-ENC-020 entier -25
RED CBOR-DEC-020 entier -25 (décodage strict)
RED CBOR-ENC-021 entier -100
RED CBOR-DEC-021 entier -100 (décodage strict)
RED CBOR-ENC-022 entier -1000
RED CBOR-DEC-022 entier -1000 (décodage strict)
RED CBOR-ENC-023 entier -4294967296
RED CBOR-DEC-023 entier -4294967296 (décodage strict)
RED CBOR-ENC-024 entier 2^64-1 (notation $int)
RED CBOR-DEC-024 entier 2^64-1 (notation $int) (décodage strict)
RED CBOR-ENC-025 entier -2^64 (notation $int)
RED CBOR-DEC-025 entier -2^64 (notation $int) (décodage strict)
RED CBOR-ENC-026 chaîne d'octets vide
RED CBOR-DEC-026 chaîne d'octets vide (décodage strict)
RED CBOR-ENC-027 chaîne d'octets 01020304
RED CBOR-DEC-027 chaîne d'octets 01020304 (décodage strict)
RED CBOR-ENC-028 chaîne d'octets de 32 octets (empreinte SHA-256)
RED CBOR-DEC-028 chaîne d'octets de 32 octets (empreinte SHA-256) (décodage strict)
RED CBOR-ENC-029 chaîne d'octets de 64 octets (signature Ed25519)
RED CBOR-DEC-029 chaîne d'octets de 64 octets (signature Ed25519) (décodage strict)
RED CBOR-ENC-030 texte vide
RED CBOR-DEC-030 texte vide (décodage strict)
RED CBOR-ENC-031 texte "a"
RED CBOR-DEC-031 texte "a" (décodage strict)
RED CBOR-ENC-032 texte "IETF"
RED CBOR-DEC-032 texte "IETF" (décodage strict)
RED CBOR-ENC-033 texte avec guillemet et antislash
RED CBOR-DEC-033 texte avec guillemet et antislash (décodage strict)
RED CBOR-ENC-034 texte "ü" (2 octets UTF-8)
RED CBOR-DEC-034 texte "ü" (2 octets UTF-8) (décodage strict)
RED CBOR-ENC-035 texte "水" (3 octets UTF-8)
RED CBOR-DEC-035 texte "水" (3 octets UTF-8) (décodage strict)
RED CBOR-ENC-036 texte "𐅑" (4 octets UTF-8)
RED CBOR-DEC-036 texte "𐅑" (4 octets UTF-8) (décodage strict)
RED CBOR-ENC-037 texte de 24 octets (bascule en-tête 1 octet -> 2 octets)
RED CBOR-DEC-037 texte de 24 octets (bascule en-tête 1 octet -> 2 octets) (décodage strict)
RED CBOR-ENC-038 texte de 256 octets (en-tête 3 octets)
RED CBOR-DEC-038 texte de 256 octets (en-tête 3 octets) (décodage strict)
RED CBOR-ENC-039 tableau vide
RED CBOR-DEC-039 tableau vide (décodage strict)
RED CBOR-ENC-040 tableau [1,2,3]
RED CBOR-DEC-040 tableau [1,2,3] (décodage strict)
RED CBOR-ENC-041 tableau imbriqué [1,[2,3],[4,5]]
RED CBOR-DEC-041 tableau imbriqué [1,[2,3],[4,5]] (décodage strict)
RED CBOR-ENC-042 tableau de 25 éléments (en-tête 2 octets)
RED CBOR-DEC-042 tableau de 25 éléments (en-tête 2 octets) (décodage strict)
RED CBOR-ENC-043 carte vide
RED CBOR-DEC-043 carte vide (décodage strict)
RED CBOR-ENC-044 carte {1:2,3:4} (clés entières)
RED CBOR-DEC-044 carte {1:2,3:4} (clés entières) (décodage strict)
RED CBOR-ENC-045 carte {"a":1,"b":[2,3]}
RED CBOR-DEC-045 carte {"a":1,"b":[2,3]} (décodage strict)
RED CBOR-ENC-046 tableau ["a",{"b":"c"}]
RED CBOR-DEC-046 tableau ["a",{"b":"c"}] (décodage strict)
RED CBOR-ENC-047 carte a..e fournie dans le désordre -> triée
RED CBOR-DEC-047 carte a..e fournie dans le désordre -> triée (décodage strict)
RED CBOR-ENC-048 tri des clés : ordre bytewise des encodages (exemple RFC 8949 §4.2.1), entrée mélangée
RED CBOR-DEC-048 tri des clés : ordre bytewise des encodages (exemple RFC 8949 §4.2.1), entrée mélangée (décodage strict)
RED CBOR-ENC-049 tri des clés texte : "z" < "aa" < "é" (longueur encodée puis octets UTF-8)
RED CBOR-DEC-049 tri des clés texte : "z" < "aa" < "é" (longueur encodée puis octets UTF-8) (décodage strict)
RED CBOR-ENC-050 tri des clés : entier 255 (18ff) avant 256 (190100) avant -1 (20)
RED CBOR-DEC-050 tri des clés : entier 255 (18ff) avant 256 (190100) avant -1 (20) (décodage strict)
RED CBOR-ENC-051 carte imbriquée triée à chaque niveau
RED CBOR-DEC-051 carte imbriquée triée à chaque niveau (décodage strict)
RED CBOR-ENC-052 booléen false
RED CBOR-DEC-052 booléen false (décodage strict)
RED CBOR-ENC-053 booléen true
RED CBOR-DEC-053 booléen true (décodage strict)
RED CBOR-ENC-054 null
RED CBOR-DEC-054 null (décodage strict)
RED CBOR-ENC-055 tag 100 : date 1970-01-01 (0 jour)
RED CBOR-DEC-055 tag 100 : date 1970-01-01 (0 jour) (décodage strict)
RED CBOR-ENC-056 tag 100 : date 2026-10-04 (20730 jours)
RED CBOR-DEC-056 tag 100 : date 2026-10-04 (20730 jours) (décodage strict)
RED CBOR-ENC-057 tag 100 : date 1945-05-08 (-9004 jours, négatif)
RED CBOR-DEC-057 tag 100 : date 1945-05-08 (-9004 jours, négatif) (décodage strict)
RED CBOR-ENC-058 tag 1 : horodatage 2013-03-21T20:04:00Z = 1363896240
RED CBOR-DEC-058 tag 1 : horodatage 2013-03-21T20:04:00Z = 1363896240 (décodage strict)
RED CBOR-ENC-059 profil minimal : carte à clés entières (économie silicium)
RED CBOR-DEC-059 profil minimal : carte à clés entières (économie silicium) (décodage strict)
RED CBOR-REJ-001 entier 1 encodé sur 2 octets (1801)
RED CBOR-REJ-002 entier 1 encodé sur 3 octets (190001)
RED CBOR-REJ-003 entier 1 encodé sur 5 octets (1a00000001)
RED CBOR-REJ-004 entier 1 encodé sur 9 octets (1b0000000000000001)
RED CBOR-REJ-005 entier 255 encodé sur 3 octets (1900ff)
RED CBOR-REJ-006 longueur de texte non minimale (7861 au lieu de 61 pour "a")
RED CBOR-REJ-007 tableau de longueur indéfinie 9f0102ff
RED CBOR-REJ-008 carte de longueur indéfinie bf616101ff
RED CBOR-REJ-009 chaîne d'octets indéfinie 5f41014102ff
RED CBOR-REJ-010 texte indéfini 7f6161ff
RED CBOR-REJ-011 carte non triée {"b":1,"a":2}
RED CBOR-REJ-012 carte non triée {100:0,10:1} (0a doit précéder 1864)
RED CBOR-REJ-013 carte triée selon RFC 7049 (longueur d'abord : 20, f4, 1864, 617a) -> interdite, l'ordre RFC 8949 est 1864, 20, 617a, f4
RED CBOR-REJ-014 clé dupliquée {"a":1,"a":2}
RED CBOR-REJ-015 octets résiduels après l'élément (0102)
RED CBOR-REJ-016 tableau tronqué (83 01 02 : 3 annoncés, 2 présents)
RED CBOR-REJ-017 texte tronqué (64 61 : 4 annoncés, 1 présent)
RED CBOR-REJ-018 entrée vide
RED CBOR-REJ-019 UTF-8 invalide dans un texte (62 c3 28)
RED CBOR-REJ-020 UTF-8 surlong (62 c0 80)
RED CBOR-REJ-021 substitut UTF-16 encodé en UTF-8 (63 ed a0 80)
RED CBOR-REJ-022 texte non NFC : e + U+0301 (63 65 cc 81)
RED CBOR-REJ-023 flottant demi-précision 1.5 (f93e00) interdit par le profil
RED CBOR-REJ-024 flottant double 1.1 (fb3ff199999999999a) interdit par le profil
RED CBOR-REJ-025 undefined (f7) interdit par le profil
RED CBOR-REJ-026 valeur simple non assignée simple(32) (f820)
RED CBOR-REJ-027 valeur simple f8 18 (simple(24) sur deux octets) : mal formé selon RFC 8949 §3.3
RED CBOR-REJ-028 entier -1 encodé sur 9 octets (3b0000000000000000) au lieu de 20
RED CBOR-REJ-029 tag 100 avec contenu non entier (d864 6161)
RED CBOR-REJ-030 tag non autorisé par le profil : tag 2 bignum (c2 41 01)
RED CBOR-REJ-031 encodage d'un texte non NFC refusé (e + U+0301)
RED CBOR-REJ-032 encodage d'une carte à clés dupliquées refusé
RED CBOR-REJ-033 encodage d'un flottant refusé par le profil
RED JCS-ENC-001 objet {"b":1,"a":2} trié
RED JCS-ENC-002 tri UTF-16 : "A" (0x41) avant "a" (0x61)
RED JCS-ENC-003 tri UTF-16 : clé vide en premier
RED JCS-ENC-004 tri UTF-16 : "z" avant "é" (0x7a < 0xe9)
RED JCS-ENC-005 tri UTF-16 vs UTF-8 : "😀" (D83D DE00) avant "～" (FF5E) — l'ordre UTF-8 donnerait l'inverse
RED JCS-ENC-006 tri UTF-16 : "€" (20AC) avant "😀" (D83D)
RED JCS-ENC-007 tri UTF-16 : préfixe commun, la plus courte d'abord ("ab" < "abc")
RED JCS-ENC-008 tri récursif dans les objets imbriqués
RED JCS-ENC-009 suppression des espaces, tableau mixte
RED JCS-ENC-010 littéraux
RED JCS-ENC-011 nombres entiers
RED JCS-ENC-012 nombre 1.0 -> 1
RED JCS-ENC-013 nombre -0 -> 0
RED JCS-ENC-014 nombre 0.1
RED JCS-ENC-015 nombre 1e21 -> 1e+21
RED JCS-ENC-016 nombre 1e20 -> 100000000000000000000
RED JCS-ENC-017 nombre 0.000001 -> 0.000001
RED JCS-ENC-018 nombre 1e-7 -> 1e-7
RED JCS-ENC-019 nombre 5e-324 (dénormalisé minimal)
RED JCS-ENC-020 nombre 1.7976931348623157e308 -> 1.7976931348623157e+308
RED JCS-ENC-021 nombre 123456789.123456789 (arrondi IEEE 754)
RED JCS-ENC-022 nombre 4.40 (prix abonnement) -> 4.4
RED JCS-ENC-023 chaîne : contrôles \b \f \n \r \t
RED JCS-ENC-024 chaîne : U+0000 et U+001F en \u minuscules
RED JCS-ENC-025 chaîne : guillemet et antislash échappés, barre oblique non échappée
RED JCS-ENC-026 chaîne : DEL U+007F non échappé
RED JCS-ENC-027 chaîne : non-ASCII littéral (€, 水, 😀)
RED JCS-ENC-028 profil mémoriel JSON (clés dans le désordre)

============================================================
Suite : antiprion.feedban.hardening [Adaptateur : ABSENT (antiprion.feedban) -> RED]
  0 PASS, 0 FAIL, 42 RED, 0 INVALID (42 total)
Suite : antiprion.feedban.matrix [Adaptateur : ABSENT (antiprion.feedban) -> RED]
  0 PASS, 0 FAIL, 67 RED, 0 INVALID (67 total)
Suite : core.cbor.deterministic [Adaptateur : ABSENT (core.cbor) -> RED]
  0 PASS, 0 FAIL, 151 RED, 0 INVALID (151 total)
Suite : core.jcs.rfc8785 [Adaptateur : ABSENT (core.jcs) -> RED]
  0 PASS, 0 FAIL, 28 RED, 0 INVALID (28 total)
------------------------------------------------------------
TOTAL : 0 PASS, 0 FAIL, 288 RED, 0 INVALID (288 total)
============================================================
Rapport généré : qa/reports/2026-10-04-d048761.json
[2026-10-04T09:32:53Z] >>> Action: RUN TESTS
Validateur de schéma : ajv 8.20.0
>>> Démarrage de l'auto-test (--selftest) : simulation de 7 corruptions dans un environnement temporaire...
INVALID PRION-BLOCK-001 PAT porcines -> aliment porcins (cannibalisme intra-espèce)
  -> Motif non répertorié dans le registre: "MUTATED_INVALID_REASON"
INVALID CBOR-ENC-001 entier 0
  -> sha256 mismatch: sha256(hex) = 4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a !== expect (6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d)
INVALID CBOR-ENC-002 entier 1
  -> Contrôle croisé CBOR encode en échec: ERR_CBOR_NOT_SHORTEST: Integer 1 encoded in 1 byte (info 24)
INVALID CBOR-ENC-003 entier 10
  -> sha256 mismatch: sha256(hex) = 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b !== expect (0000000000000000000000000000000000000000000000000000000000000000)
INVALID CBOR-ENC-045 carte {"a":1,"b":[2,3]}
  -> Contrôle croisé CBOR encode en échec: ERR_CBOR_MAP_UNSORTED: Map keys must be sorted in bytewise lexicographic order
INVALID JCS-ENC-001 objet {"b":1,"a":2} trié
  -> Identifiant dupliqué globalement: "JCS-ENC-001"
INVALID JCS-ENC-001 tri UTF-16 : "A" (0x41) avant "a" (0x61)
  -> Identifiant dupliqué globalement: "JCS-ENC-001"
INVALID PROBE-EXTRA-001 sonde dans sous-répertoire temporaire avec sha256 altéré
  -> sha256 mismatch: sha256(hex) = 7f83f7bda2d63959d34767689f06d47576683d378d9eb8d09386c9a020395c53 !== expect (0000000000000000000000000000000000000000000000000000000000000000)

--- Bilan des 7 sondes de corruption simulées ---
[Sonde 1/7] Un octet de hex altéré (CBOR-ENC-001) : DÉTECTÉ
[Sonde 2/7] Un sha256 altéré (CBOR-ENC-003) : DÉTECTÉ
[Sonde 3/7] Une liste reasons altérée (PRION-BLOCK-001) : DÉTECTÉ
[Sonde 4/7] Une carte non triée cohérente avec son sha256 (CBOR-ENC-045) : DÉTECTÉ
[Sonde 5/7] Un entier non minimal cohérent avec son sha256 (CBOR-ENC-002) : DÉTECTÉ
[Sonde 6/7] Un identifiant dupliqué (JCS-ENC-001, marqué 2x INVALID) : DÉTECTÉ
[Sonde 7/7] Une suite non déclarée dans un sous-répertoire (qa.probe.extra) : DÉTECTÉ

============================================================
RÉSULTAT SELFTEST : 7/7 corruptions détectées (8 cas INVALID)
============================================================
[SELFTEST OK] 7 corruptions détectées sur 7.
Rapport généré : qa/reports/2026-10-04-d048761-selftest.json
```

---

### 5. Conclusion & Statut
- **Critère 1** : `./scripts/runner.sh test` -> **288 cas, RED = 288, INVALID = 0, exit 0**.
- **Critère 2** : `./scripts/runner.sh test --selftest` -> **7 corruptions détectées sur 7, exit 0**.
- **Critère 3** : `git diff --stat main -- qa/vectors` est **strictement vide**.
- **Critère 4** : Aucun import depuis `core/` ou `validators/`.
- **Branche livrée** : `fix/bushi-16-harness` poussée sur `origin` au commit `d048761`.

Le Redirect 0011 est entièrement résolu et le socle de test QA-001 est désormais certifié conforme.
