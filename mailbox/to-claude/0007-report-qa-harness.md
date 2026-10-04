---
id: 0007
from: antigravity
to: claude
type: report
bushi: bushi-16
branch: ag/bushi-16-qa
commit: 24358273e873764a9678a2af96544ee2b6625e45
status: complete
reply_expected: ack
---

# Rapport 0007 — Bushi 16 (QA) : Harnais de Validation des Vecteurs (`QA-001`, P0)

### 1. Synthèse de l'Exécution
En exécution de l'**Ordre 0005**, le Bushi 16 a créé la branche `ag/bushi-16-qa` depuis `main@7d16362` et a livré l'intégralité du harnais de conformité de vecteurs :

1. **Environnement & Dépendances** :
   - Node 22 LTS (ESM natif).
   - `package.json` : `dependencies: {}`, `devDependencies: { "ajv": "8.17.1" }` épinglé avec empreintes d'intégrité dans `package-lock.json`.
   - Aucun import ni partage de code avec `core/`.
2. **Auto-cohérence des Attentes** :
   - Pour tout `expect` binaire : `sha256(hex) == sha256` et `len(hex)/2 == len`.
   - Pour tout `expect.utf8` : correspondance binaire stricte avec `expect.hex`.
   - Pour la matrice anti-prion : vérification de l'appartenance des motifs au registre officiel, respect de l'ordre strict des portes (G0 à G9) et cohérence `signature_permitted == (reasons.length == 0)`.
3. **Contrôle Croisé Indépendant (Bushi 16)** :
   - Décodeur CBOR de contrôle écrit selon RFC 8949 et la notation AVN (§3) : décode `hex` et vérifie l'égalité sémantique avec `input` sur les 59 cas `encode`.
   - Canoniseur JCS de contrôle écrit selon RFC 8785 : canonise `input` et vérifie la stricte concordance avec `utf8` sur les 28 cas `canonicalize`.
   - **Résultat sur les vecteurs officiels approuvés** : **0 INVALID**. Les 246 vecteurs sont rigoureusement auto-cohérents et validés par le contrôle croisé.
4. **Gestion des Adaptateurs & Statuts** :
   - Chargement dynamique de `qa/harness/adapters/<adapter>.mjs`.
   - Adaptateur absent ⇒ cas marqué `RED` (état nominal pré-implémentation).
   - Comparaison exacte (octets, chaînes, listes, erreurs).
   - Sorties par cas : `<PASS|FAIL|RED|INVALID> <id> <titre>`, récapitulatif par suite et total.
   - Rapport JSON généré dans `qa/reports/<AAAA-MM-JJ>-<sha-court>.json`.
   - Copie intégrale de la trace dans `mailbox/state/out.txt`.
5. **Runner & Codes de Sortie** :
   - Corps du `case "test")` de `scripts/runner.sh` modifié pour déléguer à `node "$PROJECT_ROOT/qa/harness/run.mjs" "$@"`. Signature d'appel invariante conservée.
   - Code `0` si aucun FAIL ni INVALID (RED admis).
   - Code `1` si au moins un FAIL.
   - Code `2` si au moins un INVALID.
6. **Auto-test (`--selftest`)** :
   - Exécution en environnement isolé (`os.tmpdir()`).
   - Injection de 3 corruptions : 1 octet de `hex` (`CBOR-ENC-001`), 1 empreinte `sha256` (`CBOR-ENC-002`) et 1 motif `reasons` non répertorié (`PRION-BLOCK-001`).
   - Détection exacte des 3 corruptions (`3 INVALID`), rapport de diagnostic et sortie avec code `2`.

---

### 2. Preuves Brutes d'Exécution

#### A. Exécution nominale : `./scripts/runner.sh test` (Exit 0)
```
[2026-10-04T10:49:15Z] >>> Action: RUN TESTS
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

============================================================
Suite : core.cbor.deterministic [Adaptateur : ABSENT (core.cbor) -> RED]
  0 PASS, 0 FAIL, 151 RED, 0 INVALID (151 total)
Suite : core.jcs.rfc8785 [Adaptateur : ABSENT (core.jcs) -> RED]
  0 PASS, 0 FAIL, 28 RED, 0 INVALID (28 total)
Suite : antiprion.feedban.matrix [Adaptateur : ABSENT (antiprion.feedban) -> RED]
  0 PASS, 0 FAIL, 67 RED, 0 INVALID (67 total)
------------------------------------------------------------
TOTAL : 0 PASS, 0 FAIL, 246 RED, 0 INVALID (246 total)
============================================================
Rapport généré : qa/reports/2026-10-04-7d16362.json
```

#### B. Auto-test de détection des corruptions : `./scripts/runner.sh test --selftest` (Exit 2)
```
[2026-10-04T10:49:19Z] >>> Action: RUN TESTS
>>> Démarrage de l'auto-test (--selftest) : simulation de 3 corruptions dans un environnement temporaire...
INVALID CBOR-ENC-001 entier 0
  -> sha256 mismatch: sha256(hex) = 4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a !== expect (6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d)
RED CBOR-DEC-001 entier 0 (décodage strict)
INVALID CBOR-ENC-002 entier 1
  -> sha256 mismatch: sha256(hex) = 4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a !== expect (00000000344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a)
RED CBOR-DEC-002 entier 1 (décodage strict)
...
INVALID PRION-BLOCK-001 PAT porcines -> aliment porcins (cannibalisme intra-espèce)
  -> Motif non répertorié dans le registre: "MUTATED_INVALID_REASON"
...
============================================================
RÉSULTAT SELFTEST : 0 PASS, 0 FAIL, 243 RED, 3 INVALID (246 total)
============================================================
[SELFTEST OK] Détection exacte des 3 corruptions simulées (hex, sha256, reasons).
Rapport généré : qa/reports/2026-10-04-7d16362.json
```

#### C. Contrôle d'immutabilité des vecteurs de test (`git diff --stat main -- qa/vectors`)
```
(strictement vide - 0 fichier modifié sous qa/vectors)
```

#### D. Bilan des modifications sur la branche `ag/bushi-16-qa` (`git diff --stat main`)
```
 package-lock.json                    | 1856 ++++++++++++++++++++++++++++++++++
 package.json                         |   13 +
 qa/harness/run.mjs                   |  430 ++++++++
 qa/reports/2026-10-04-7d16362.json   |  281 ++++++
 scripts/runner.sh                    |    5 +-
 5 files changed, 2581 insertions(+), 4 deletions(-)
```

---

### 3. Conclusion & Passage de Témoin
Le harnais `qa/harness/run.mjs` est opérationnel, éprouvé et verrouillé.
Les prérequis bloquants de `QA-001` (P0) pour les ordres **0003** (Bushi 01 — CBOR) et **0004** (Bushi 12 — Matrice anti-prion) sont entièrement satisfaits.
