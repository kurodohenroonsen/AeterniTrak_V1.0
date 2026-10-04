# Spécification Technique AeterniCore V1.0 — Sérialisation CBOR Déterministe & Profil Mémoriel

> **Bushi 01 — AeterniCore Architect**  
> **Devise** : *"Un seul cœur, toutes les plateformes. L'état pur ne ment jamais."*  
> **Date de rédaction** : 4 octobre 2026  
> **Statut** : Approuvé pour Phase B avec amendements M1-M10 (Ordres 0012 & 0020)  
> **Conformité normative** : RFC 8949 (§4.2.1), RFC 8785 (JCS), RFC 8943 (Tag 100), RFC 8610 (CDDL), RFC 9052 / RFC 9053 (COSE), RFC 9596 (COSE typ), FIPS 180-4 (SHA-256), `DEC-AET-01`, `DEC-AET-04`.

---

## 0. Recherches Documentaires Normatives Obligatoires

Conformément à la section 2 de la fiche de poste du Bushi 01, les recherches normatives suivantes ont été exécutées et intégrées aux fondations de cette spécification :

1. **RFC 8949 — Concise Binary Object Representation (CBOR)**
   - *URL consultée* : `https://www.rfc-editor.org/rfc/rfc8949.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Section 4.2.1 (*Core Deterministic Encoding Requirements*), sérialisation préférée la plus courte pour entiers et longueurs, interdiction stricte des longueurs indéfinies, tri bytewise-lexicographique des encodages de clés de cartes.
2. **RFC 8785 — JSON Canonicalization Scheme (JCS)**
   - *URL consultée* : `https://www.rfc-editor.org/rfc/rfc8785.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Tri lexicographique strict des propriétés d'objets selon les unités de code UTF-16 (code units), suppression intégrale des espaces blancs superflus, formatage des nombres IEEE 754 conforme à ECMAScript `Number::toString()`, politique d'échappement minimale (`"`, `\`, et caractères de contrôle `\u0000` à `\u001f` en minuscules).
3. **FIPS 180-4 — Secure Hash Standard (SHA-256)**
   - *URL consultée* : `https://csrc.nist.gov/pubs/fips/180-4/upd1/final`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Calcul déterministe d'empreintes numériques 256 bits (32 octets) pour les CIDs de blocs de données (WebP, audio selon DEC-AET-01) et les condensats de signature COSE.
4. **WebAssembly Core Specification 2.0 — SIMD & Memory Footprint**
   - *URL consultée* : `https://www.w3.org/TR/wasm-core-2/`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Intégration portable SIMD 128 bits (`v128`) pour l'accélération vectorielle du calcul SHA-256 et du tri des clés en mémoire linéaire sans overhead d'allocation dynamique.
5. **Deterministic CBOR Encoding Rules for Cryptographic Applications (dCBOR / CDE)**
   - *URL consultée* : `https://datatracker.ietf.org/doc/draft-ietf-cbor-cde/`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Rejet obligatoire de tout flottant, toute valeur indéfinie (`undefined`), toute valeur simple non assignée, et obligation d'une validation Unicode NFC stricte sans transformation silencieuse.

---

## A1. Règles d'Encodage Normatives

AeterniCore implémente le profil d'encodage binaire déterministe le plus strict de l'écosystème, assurant qu'une structure logique unique produise **exactement la même suite d'octets sur toute machine** (x86_64, ARM64, WASM, JavaCard).

### 1. Forme la plus courte (Preferred Serialization)
Conformément à la RFC 8949 §4.2.1 règle (1) :
- Tout entier positif (type majeur 0) ou négatif (type majeur 1) doit être encodé sur le nombre minimal d'octets suffisant pour contenir sa valeur :
  - $[0, 23]$ : encodé directement dans l'octet initial (`0x00`..`0x17`).
  - $[24, 255]$ : encodé sur 2 octets (`0x18xx`).
  - $[256, 65535]$ : encodé sur 3 octets (`0x19xxxx`).
  - $[65536, 4294967295]$ : encodé sur 5 octets (`0x1axxxxxxxx`).
  - $[4294967296, 2^{64}-1]$ : encodé sur 9 octets (`0x1bxxxxxxxxxxxxxxxx`).
- Les entiers négatifs $n \in [-2^{64}, -1]$ utilisent l'argument $-1 - n$ encodé selon la même règle de compacité minimale dans le type majeur 1.
- Toute tentative d'encoder ou de décoder un entier sur une largeur supérieure à son minimum requis est formellement rejetée avec le code `ERR_CBOR_NOT_SHORTEST` (ex. cas `CBOR-REJ-001` à `CBOR-REJ-005`, `CBOR-REJ-028`).
- Les longueurs de chaînes d'octets (type majeur 2), de textes (type majeur 3), de tableaux (type majeur 4) et de cartes (type majeur 5) suivent rigoureusement cette même règle de compacité (ex. `CBOR-REJ-006`).

### 2. Longueurs définies obligatoires
- Toute sérialisation en longueur indéfinie (*indefinite-length / streaming*, utilisant les octets `0x9f`, `0xbf`, `0x5f`, `0x7f` avec l'octet de fin `0xff`) est **strictement proscrite**.
- Le décodeur strict rejette immédiatement ces formats avec l'erreur `ERR_CBOR_INDEFINITE_LENGTH` (cas `CBOR-REJ-007` à `CBOR-REJ-010`).

### 3. Tri Bytewise-Lexicographique des Clés de Carte
- Conformément à la RFC 8949 §4.2.1 règle (3), les paires clé/valeur d'une carte (type majeur 5) doivent être ordonnées selon l'ordre **bytewise-lexicographique des encodages déterministes complets des clés**.
- **Avertissement normatif crucial** : La règle obsolète de la RFC 7049 (qui ordonnait d'abord par la longueur de la clé encodée, puis par la valeur) est **strictement caduque et interdite**. Tout encodage respectant l'ordre RFC 7049 au lieu de la RFC 8949 est rejeté (`ERR_CBOR_MAP_UNSORTED`, cas `CBOR-REJ-013`).
- Règle de comparaison : pour deux clés encodées $K_A$ et $K_B$, l'ordre est déterminé par le premier octet différent $K_A[i] \neq K_B[i]$. Si un encodage est un préfixe strict de l'autre, le plus court précède le plus long.
  - *Conséquence* : Un entier $255$ encodé `0x18ff` précède l'entier $256$ encodé `0x190100`, qui précède l'entier négatif $-1$ encodé `0x20` (car `0x18` < `0x19` < `0x20`, cas `CBOR-ENC-050`).
  - *Clés entières positives du profil v1* : Les clés entières $[1, 12]$ s'encodent `0x01` à `0x0c`. Leur ordre numérique coïncide naturellement avec leur ordre bytewise CBOR.
- Tout flux présentant une inversion d'ordre est rejeté avec `ERR_CBOR_MAP_UNSORTED` (cas `CBOR-REJ-011`, `CBOR-REJ-012`).

### 4. Unicité stricte des clés
- Aucune carte ne peut comporter de clé dupliquée.
- Le décodeur strict vérifie l'absence de collision après chaque insertion et rejette immédiatement avec `ERR_CBOR_DUPLICATE_KEY` (cas `CBOR-REJ-014`). L'encodeur refuse également toute entrée présentant des clés en doublon (cas `CBOR-REJ-032`).

### 5. Types de données et restrictions de profil
Dans le cadre de l'enveloppe de stockage AeterniCore et des profils mémoriels :
- **Nombres flottants interdits** : Aucun nombre flottant IEEE 754 (demi-précision `0xf9`, simple précision `0xfa`, double précision `0xfb`) n'est toléré. Rejet immédiat avec `ERR_CBOR_UNSUPPORTED_TYPE` (cas `CBOR-REJ-023`, `CBOR-REJ-024`, `CBOR-REJ-033`).
- **Valeurs spéciales interdites** : `undefined` (`0xf7`), valeurs simples non assignées de 0 à 19 (`0xe0` à `0xf3`, cas `CBOR-REJ-038` à `CBOR-REJ-040`), et toute valeur simple 1 octet non assignée (`0xf820`..`0xf8ff`, cas `CBOR-REJ-027`) sont bien formées mais rejetées avec `ERR_CBOR_UNSUPPORTED_TYPE`.
- **Octet d'arrêt isolé interdit** : L'octet de fin `0xff` hors d'une structure de longueur indéfinie est mal formé et lève `ERR_CBOR_MALFORMED` (cas `CBOR-REJ-041`).
- **Valeurs simples autorisées** : Exclusivement `false` (`0xf4`), `true` (`0xf5`), et `null` (`0xf6`).
- **Étiquettes sémantiques (Tags) autorisées** :
  - **Tag `1`** (RFC 8949 §3.4.2) : Horodatage epoch en secondes entières non négatives (types majeurs 0 ou valeur positive). Si le contenu n'est pas un entier ou est négatif, le décodeur lève `ERR_CBOR_TAG_CONTENT` (cas `CBOR-REJ-037`).
  - **Tag `100`** (RFC 8943) : Date civile grégorienne en nombre entier de jours écoulés depuis le 1er janvier 1970 UTC (types majeurs 0 ou 1, valeurs positives, nulles ou négatives admises).
  - Tout autre tag (y compris tag 2 bignum) est proscrit dans la charge utile mémorielle et déclenche `ERR_CBOR_UNSUPPORTED_TAG` (cas `CBOR-REJ-030`).
  - Si le tag 100 est appliqué à une donnée non entière (ex. texte ou carte CBOR déguisée), le décodeur lève `ERR_CBOR_TAG_CONTENT` (cas `CBOR-REJ-029`, `CBOR-REJ-036`).

### 6. Intégrité Unicode et Normalisation NFC
- Toutes les chaînes textuelles (type majeur 3) doivent être composées d'octets UTF-8 valides. Tout octet non conforme, surlong (*overlong*), ou surrogate UTF-16 isolé lève `ERR_CBOR_INVALID_UTF8` (cas `CBOR-REJ-019` à `CBOR-REJ-021`).
- **Pas de normalisation silencieuse** : Les textes doivent être **préalablement normalisés en forme NFC (Unicode Normalization Form C)**. L'encodeur vérifie `str.normalize('NFC') === str` et refuse tout texte non-NFC (`ERR_CBOR_TEXT_NOT_NFC`, cas `CBOR-REJ-031`). Le décodeur strict refuse également les textes décomposés NFD (`ERR_CBOR_TEXT_NOT_NFC`, cas `CBOR-REJ-022`).

### 7. Canonisation JCS (RFC 8785) pour les exports JSON
- Les attestations et déclarations transmises sous format JSON-LD sont canonisées via la RFC 8785 :
  - Tri des propriétés d'objets selon les code units UTF-16 (ex. `"A"` < `"a"`, `""` en tête, `"😀"` U+D83D U+DE00 avant `"～"` U+FF5E, cas `JCS-ENC-001` à `JCS-ENC-007`).
  - Nombres formatés selon la règle ECMAScript 7.1.12.1 `Number::toString()` (ex. `1.0` $\rightarrow$ `1`, `-0` $\rightarrow$ `0`, `1e21` $\rightarrow$ `1e+21`, `1e20` $\rightarrow$ `100000000000000000000`, cas `JCS-ENC-011` à `JCS-ENC-022`).
  - Échappement restreint aux seuls caractères obligatoires `"` (`\"`), `\` (`\\`), et contrôles `\u0000`..`\u001f` en minuscules hexadécimales (cas `JCS-ENC-023` à `JCS-ENC-026`).

### 8. Règle Normative AVN-R & Représentation Interne (Cycle 0010, Ordre 0065)

#### 8.1. Règle AVN-R des Clés Réservées
Dans la notation des vecteurs AVN (AeterniTrak Vector Notation), le JSON ne sait pas exprimer nativement la distinction entre certains types CBOR :
- Les clés `$int`, `$bytes`, `$map`, `$tag`, `$value` et `$float` sont réservées à la syntaxe de notation AVN.
- **Règle impérative** : Un objet JSON simple (notation `{ ... }`) ne porte **JAMAIS** de clé textuelle débutant par le caractère `'$'`.
- Une carte CBOR (type majeur 5) dont au moins une clé textuelle commence par `'$'` doit obligatoirement être représentée sous la forme explicite :
  ```json
  {"$map": [[k1, v1], [k2, v2], ...]}
  ```
- *Justification technique* : Sans cette règle, une carte CBOR dont les clés textuelles sont `"$tag"` et `"$value"` (`{"$tag": 100, "$value": 20730}`) était indistincte de l'élément étiqueté `100(20730)`. De même, une carte à clé textuelle `"$bytes"` était confondue avec une chaîne binaire, et une carte à clé textuelle `"$map"` avec une carte à clés entières.

#### 8.2. Représentation Interne Typée & Séparation Sémantique
- L'AVN est une notation de test et d'échange de vecteurs, consommée par les adaptateurs de conformité du harnais QA.
- Au sein de l'architecture AeterniCore (`core/profile/` et `core/cose/`), la validation logique s'opère sur la **structure sémantique réelle** (types majeurs CBOR natifs) et non sur des artefacts syntaxiques de la notation :
  1. **Contrôle strict des tags** : Les tags 1 et 100 sont vérifiés sur leur type majeur réel (entiers stricts). Une carte CBOR passée sous un tag 1 ou 100 échoue dès le décodage CBOR (`ERR_CBOR_TAG_CONTENT`), avant toute logique de profil ou de crypto.
  2. **Proscription des tests fragiles sur la notation** : Aucun test du type `"$map" in obj` ou `"$tag" in obj` ne doit être exécuté dans les validateurs sur des structures pouvant découler d'une carte à clés texte légitime.
  3. **Étanchéité des types** : Une carte CBOR à clés entières est reconnue par sa nature intrinsèque de carte et le typage entier de ses clés, garantissant l'immunité complète face aux collisions de clés textuelles `$tag`, `$map`, `$int` ou `$bytes`.

---

## A2. Profil Mémoriel V1 en CDDL (RFC 8610) à Clés Entières

Sur support silicium (NFC / carte à puce sécurisée), chaque octet économisé renforce la robustesse de transmission RF et libère de l'espace pour la redondance cryptographique. Les clés textuelles sont formellement proscrites : **toutes les clés de la charge utile sont des entiers stricts**.

### 1. Architecture Quadripartite des Blocs AeterniTrak

| Bloc | Désignation | Support & Localisation | Statut Cryptographique |
|---|---|---|---|
| **Bloc 1** | **Profil Mémoriel & Identité** | Silicium NFC (EEPROM $\le$ 2 Ko) | **Scellé & Immuable** sous enveloppe `COSE_Sign1` |
| **Bloc 2** | **Portrait Visuel** | WebP haute fidélité ($\le 20\,480$ octets) | **Immuable**, empreinte SHA-256 scellée dans le Bloc 1 |
| **Bloc 3** | **Mémo Vocal** | Audio ($\le 46\,080$ octets, codec selon `DEC-AET-01`) | **Immuable**, empreinte SHA-256 scellée dans le Bloc 1 |
| **Bloc 4** | **Hommages & Registre Mémoriel** | Puce étendue ou ledger décentralisé | **Évolutif (Append-Only)** — **HORS enveloppe Bloc 1** |

> **Règle de Sécurité Fondamentale** : Le Bloc 4 (recueil de condoléances, hommages de la communauté, messages post-mortem) est **strictement exclu de l'enveloppe signée du Bloc 1**. Toute modification ou ajout dans le Bloc 4 n'invalide en rien le scellement cryptographique du profil d'état-civil du défunt inscrit dans le Bloc 1.

### 2. Spécification Formelle CDDL (RFC 8610)

```cddl
; ==============================================================================
; AeterniTrak Memorial Profile Specification - Version 1.0 (AeterniCore)
; Conforme RFC 8610, RFC 8949, RFC 8943, RFC 9052, RFC 9596, DEC-AET-01, DEC-AET-04
; Amendements M1-M10 intégrés
; ==============================================================================

; --- Structure Racine du Profil Mémoriel (Charge Utile CBOR) ---
MemorialProfileV1 = {
  1 => schema_version,
  2 => subject_kind,
  3 => names,
  ? 4 => birth_date,        ; Optionnel pour animal (subject_kind = 2)
  ? 5 => death_date,
  ? 6 => rite_code,         ; Optionnel, registre fermé docs/functional/rite-registry.md
  7 => country,             ; Pays de résidence du défunt (ISO 3166-1 alpha-2)
  ? 8 => portrait_ref,
  ? 9 => voice_memo_ref,
  10 => issuer_id,
  11 => issued_at,
  ? 12 => epitaph,
  ? 13 => species_taxid,    ; Optionnel pour animal (entier NCBI Taxonomy)
}

; 1: Version du schéma (uint fixé à 1 en v1 - rejet strict si différent)
schema_version = 1

; 2: Nature du sujet (1 = human, 2 = animal)
subject_kind = 1 / 2

; 3: Structure des noms
names = {
  1 => usage_name,
  ? 2 => birth_name,
  ? 3 => given_names,
}

; Règle normative : .size compte des octets UTF-8, pas des caractères Unicode
usage_name  = tstr .size (1..120) ; Nom d'usage ou patronyme principal (NFC)
birth_name  = tstr .size (1..120) ; Nom de naissance / jeune fille (NFC)
given_names = [0*8 (tstr .size (1..80))] ; Au plus 8 prénoms ordonnés (NFC)

; 4 & 5: Dates civiles grégoriennes (RFC 8943 - Tag 100)
; Jours écoulés depuis 1970-01-01 (négatif pour dates antérieures)
; Optionnel pour subject_kind = 2 (animal de compagnie)
birth_date = #6.100(int)
death_date = #6.100(int)

; 6: Code de rite / orientation philosophique (uint optionnel)
; Renvoie au registre fermé normatif `docs/functional/rite-registry.md` (Bushi 13 et 08)
rite_code = uint

; 7: Pays de résidence du défunt (ISO 3166-1 alpha-2 majuscules strictes)
country = tstr .size 2 .regexp "^[A-Z]{2}$"

; 8 & 9: Références cryptographiques des Blocs Immuables 2 et 3
portrait_ref   = AssetReferencePortrait
voice_memo_ref = AssetReferenceVoice

AssetReferencePortrait = {
  1 => asset_sha256,
  2 => uint .le 20480,      ; Longueur maximale 20 Ko (20 480 octets) pour le portrait (Bloc 2)
}

AssetReferenceVoice = {
  1 => asset_sha256,
  2 => uint .le 46080,      ; Longueur maximale 45 Ko (46 080 octets) pour l'audio (Bloc 3)
}

asset_sha256 = bstr .size 32 ; Condensat SHA-256 (FIPS 180-4)

; 10: Identifiant qualifié de l'opérateur ou concessionnaire émetteur
issuer_id = tstr .size (4..64) ; ex: "BE-WAL-AET-2026-0042"

; 11: Date d'émission de l'acte mémoriel (Tag 100)
issued_at = #6.100(int)

; 12: Épitaphe ou texte mémoriel solennel (UTF-8 NFC strict)
epitaph = tstr .size (1..1600)

; 13: Identifiant taxonomique NCBI pour animal (subject_kind = 2)
species_taxid = uint
```

### 3. Règles Normatives de Profil et de Compatibilité

1. **Encadrement Strict du Budget CBOR (Amendement M2)** :
   - La taille de la charge utile CBOR sérialisée (`payload`) ne doit en aucun cas dépasser **$1\,900$ octets**.
   - Tout profil généré ou reçu dont l'encodage déterministe excède $1\,900$ octets est formellement rejeté avec le code `ERR_PROFILE_TOO_LARGE`.
   - Les contraintes `.size (min..max)` du CDDL expriment strictement des **tailles en octets UTF-8** et non en points de code ou caractères.
   - La liste `given_names` est bornée à un maximum de **8 prénoms**.

2. **Politique Fermée des Clés et Compatibilité Ascendante (Amendement M8)** :
   - Tout lecteur ou validateur v1 **rejette obligatoirement** une carte dont `schema_version != 1`.
   - Tout lecteur ou validateur v1 **rejette obligatoirement** toute carte contenant une clé non définie dans la spécification v1 (hors plage d'entiers $[1, 13]$). Aucune ignorance silencieuse n'est admise dans une enveloppe signée.

3. **Ordre de Contrôle Normatif du Profil Mémoriel V1 (README.md §4.7)** :
   Le validateur évalue la conformité selon un ordre séquentiel strict où le premier échec détermine le code d'erreur levé :
   1. Plus de 1 900 octets : `ERR_PROFILE_TOO_LARGE`, avant tout décodage ;
   2. Décodage strict CBOR : l'erreur remonte avec son code `ERR_CBOR_*` natif (aucun doublon `ERR_PROFILE_*` pour une faute CBOR) ;
   3. La racine n'est pas une carte : `ERR_PROFILE_NOT_A_MAP` ;
   4. Une clé de la racine n'est pas un entier : `ERR_PROFILE_INVALID_KEY_TYPE` ;
   5. Clé 1 absente : `ERR_PROFILE_MISSING_FIELD` ; différente de l'entier 1 : `ERR_PROFILE_UNSUPPORTED_VERSION` ;
   6. Clé hors de $[1, 13]$ : `ERR_PROFILE_UNKNOWN_FIELD` ;
   7. Clé obligatoire absente (2, 3, 7, 10, 11) : `ERR_PROFILE_MISSING_FIELD` ;
   8. Champs dans l'ordre croissant des clés :
      - Clé 2 (`subject_kind`) : entier 1 ou 2, sinon `ERR_PROFILE_INVALID_SUBJECT_KIND`.
      - Clé 3 (`names`) : carte, clés entières, pas de clé hors de 1..3, clé 1 obligatoire (`usage_name` 1..120 octets UTF-8), clé 2 optionnelle (`birth_name` 1..120 octets UTF-8), clé 3 optionnelle (`given_names` tableau de 0 à 8 prénoms de 1..80 octets UTF-8). En cas d'anomalie : `ERR_PROFILE_INVALID_NAME`, `ERR_PROFILE_TOO_MANY_NAMES`, `ERR_PROFILE_INVALID_KEY_TYPE`, `ERR_PROFILE_UNKNOWN_FIELD`, ou `ERR_PROFILE_MISSING_FIELD`.
      - Clé 4 (`birth_date`) : si présente, date civile Tag 100 entier (`#6.100(int)`), sinon `ERR_PROFILE_INVALID_DATE_TYPE` ; obligatoire pour sujet humain (clé 2 = 1), sinon `ERR_PROFILE_MISSING_BIRTH_DATE`.
      - Clé 5 (`death_date`) : si présente, date civile Tag 100 entier (`#6.100(int)`), sinon `ERR_PROFILE_INVALID_DATE_TYPE`.
      - Clé 6 (`rite_code`) : si présent, entier non négatif (uint), sinon `ERR_PROFILE_INVALID_RITE`.
      - Clé 7 (`country`) : code pays ISO 3166-1 alpha-2 en majuscules strictes (`^[A-Z]{2}$`), sinon `ERR_PROFILE_INVALID_COUNTRY`.
      - Clé 8 (`portrait_ref`) : si présent, carte {1: asset_sha256 (32 octets bstr), 2: len (uint <= 20480)}, sinon `ERR_PROFILE_INVALID_ASSET_REF`, `ERR_PROFILE_INVALID_HASH_LENGTH`, ou `ERR_PROFILE_PORTRAIT_TOO_LARGE`.
      - Clé 9 (`voice_memo_ref`) : si présent, carte {1: asset_sha256 (32 octets bstr), 2: len (uint <= 46080)}, sinon `ERR_PROFILE_INVALID_ASSET_REF`, `ERR_PROFILE_INVALID_HASH_LENGTH`, ou `ERR_PROFILE_VOICE_TOO_LARGE`.
      - Clé 10 (`issuer_id`) : chaîne de 4 à 64 octets UTF-8, sinon `ERR_PROFILE_INVALID_ISSUER_ID`.
      - Clé 11 (`issued_at`) : date d'émission Tag 100 entier (`#6.100(int)`), sinon `ERR_PROFILE_INVALID_DATE_TYPE`.
      - Clé 12 (`epitaph`) : si présente, chaîne de 1 à 1 600 octets UTF-8 NFC, sinon `ERR_PROFILE_INVALID_EPITAPH`.
      - Clé 13 (`species_taxid`) : interdit pour un sujet humain (`ERR_PROFILE_INVALID_SPECIES`) ; pour un animal, entier strictement positif (uint > 0), sinon `ERR_PROFILE_INVALID_SPECIES`.

   Dans les cartes imbriquées (`names`, références d'actifs), les mêmes codes `ERR_PROFILE_INVALID_KEY_TYPE`, `ERR_PROFILE_UNKNOWN_FIELD` et `ERR_PROFILE_MISSING_FIELD` s'appliquent. Toutes les contraintes de taille se comptent en octets UTF-8.

4. **Registre Complet des Erreurs de Profil (`ERR_PROFILE_*`)** :
   | Code d'Erreur | Condition de Déclenchement |
   |---|---|
   | `ERR_PROFILE_TOO_LARGE` | Charge utile CBOR dépassant 1 900 octets (contrôlé avant décodage) |
   | `ERR_PROFILE_NOT_A_MAP` | Élément racine n'est pas une carte CBOR |
   | `ERR_PROFILE_INVALID_KEY_TYPE` | Clé non entière dans la carte racine ou une carte imbriquée |
   | `ERR_PROFILE_MISSING_FIELD` | Clé obligatoire absente (racine: 1, 2, 3, 7, 10, 11 ; `names`: 1 ; asset ref: 1, 2) |
   | `ERR_PROFILE_UNSUPPORTED_VERSION` | Version de schéma (clé 1) absente ou différente de l'entier 1 |
   | `ERR_PROFILE_UNKNOWN_FIELD` | Clé inconnue hors plage autorisée (racine: hors 1..13 ; `names`: hors 1..3 ; asset ref: hors 1..2) |
   | `ERR_PROFILE_INVALID_SUBJECT_KIND` | Nature du sujet (clé 2) différente de 1 (humain) ou 2 (animal) |
   | `ERR_PROFILE_INVALID_NAME` | Structure ou contenu de `names` invalide, ou taille d'un nom hors bornes en octets |
   | `ERR_PROFILE_TOO_MANY_NAMES` | Liste des prénoms (`given_names`, clé 3.3) comportant plus de 8 éléments |
   | `ERR_PROFILE_INVALID_DATE_TYPE` | Date (clé 4, 5 ou 11) non étiquetée Tag 100 ou contenu non entier |
   | `ERR_PROFILE_MISSING_BIRTH_DATE` | Date de naissance (clé 4) absente pour un sujet humain (`subject_kind = 1`) |
   | `ERR_PROFILE_INVALID_RITE` | Code de rite (clé 6) non entier ou négatif |
   | `ERR_PROFILE_INVALID_COUNTRY` | Code pays (clé 7) non conforme à ISO 3166-1 alpha-2 majuscules (`^[A-Z]{2}$`) |
   | `ERR_PROFILE_INVALID_ASSET_REF` | Référence d'actif (clé 8 ou 9) mal formée, type d'empreinte ou de taille invalide |
   | `ERR_PROFILE_INVALID_HASH_LENGTH` | Empreinte SHA-256 de référence d'actif différente de 32 octets |
   | `ERR_PROFILE_PORTRAIT_TOO_LARGE` | Longueur du portrait (clé 8.2) supérieure à 20 480 octets (Amendement M6) |
   | `ERR_PROFILE_VOICE_TOO_LARGE` | Longueur du mémo vocal (clé 9.2) supérieure à 46 080 octets (Amendement M6) |
   | `ERR_PROFILE_INVALID_ISSUER_ID` | Identifiant émetteur (clé 10) non textuel ou taille hors 4..64 octets UTF-8 |
   | `ERR_PROFILE_INVALID_EPITAPH` | Épitaphe (clé 12) non textuelle, vide (0 octet) ou supérieure à 1 600 octets UTF-8 |
   | `ERR_PROFILE_INVALID_SPECIES` | `species_taxid` (clé 13) présent pour un humain, ou non entier > 0 pour un animal |

---

## A3. Budget Silicium & Dimensionnement Matériel

Le Bloc 1 est destiné à être gravé et transmis par des transpondeurs NFC de type ISO/IEC 14443 Type A (NFC Forum Type 4 Tag / cartes JavaCard ACOSJ).
- **Limite physique de l'enveloppe signée (Bloc 1)** : $\le 2\,048$ octets.
- **Budget alloué à la charge utile CBOR pure** : $\le 1\,900$ octets.
- **Budget réservé à l'overhead cryptographique COSE_Sign1** : $\le 148$ octets.

### 1. Décomposition de l'Overhead COSE_Sign1 (Tag 18)

L'enveloppe `COSE_Sign1` (RFC 9052 §4.2) se compose d'un tableau CBOR étiqueté à 4 éléments :

$$\text{COSE\_Sign1} = \text{Tag}(18, [\text{protected}, \text{unprotected}, \text{payload}, \text{signature}])$$

| Composant | Description | Représentation Binaire | Taille |
|---|---|---|---|
| **Tag CBOR 18** | Identifiant majeur COSE_Sign1 | `0xd2` (major 6, info 18) | 1 octet |
| **En-tête de tableau (4 éléments)** | Tableau défini | `0x84` (major 4, info 4) | 1 octet |
| **En-tête protégé (`protected`)** | `bstr` enveloppant `{1: alg, 16: typ}` avec séparation de domaine `application/aeternitrak-profile+cbor` (M4) | `0x582ba201...1078256170...` | 45 octets |
| **En-tête non protégé (`unprotected`)** | Carte avec identifiant de clé `kid` (exactement 16 octets, M3) ou vide | `0xa10450<kid_16_bytes>` (19 octets) ou `0xa0` (1 octet) | 1 à 19 octets |
| **En-tête de charge utile (`payload`)** | `bstr` préfixant la charge utile ($N \le 1\,900$ octets) | `0x59` suivi de $N$ sur 2 octets en Big-Endian | 3 octets |
| **Signature numérique (`signature`)** | `bstr` de 64 octets (Ed25519 brut ou ECDSA P-256 $r\|s$, M10) | `0x5840` (2 octets) + 64 octets de signature | 66 octets |
| **TOTAL OVERHEAD COSE_Sign1** | | | **117 à 135 octets** |

Avec une charge utile CBOR maximale fixée à $1\,900$ octets (Amendement M2) :
$$\text{Taille Enveloppe Totale} \le 1\,900 + 135 = 2\,035 \text{ octets} \le 2\,048 \text{ octets}$$
La marge résiduelle de sécurité sur le silicium est d'au moins **13 octets** dans le scénario le plus défavorable, garantissant le respect de la Règle inviolable 3.

### 2. Décompte Octet par Octet du Profil Maximal (Amendements M1, M6)

Le tableau suivant certifie la décomposition binaire d'un profil mémoriel dense poussé à ses limites de conception (avec patronymes aristocratiques complets, 6 prénoms, empreintes de 32 octets, et une épitaphe solennelle de $1\,558$ octets en français NFC avec diacritiques) :

| Clé / Entrée | Rôle Normatif | Valeur / Structure | Encodage Clé | Taille Champ |
|---|---|---|---|---|
| En-tête racine | Carte à 12 paires | Type majeur 5, 12 paires | — | 1 octet (`0xac`) |
| **Clé 1** | Version de schéma | `1` | `0x01` (1 o) | 2 octets (`01 01`) |
| **Clé 2** | Nature du sujet | `1` (Humain) | `0x02` (1 o) | 2 octets (`02 01`) |
| **Clé 3** | Noms complets | Carte à 3 clés : Usage (51 o), Naissance (44 o), 6 prénoms (63 o) | `0x03` (1 o) | 164 octets |
| **Clé 4** | Date de naissance | Tag 100, `-18263` (1er janvier 1920) / `-18262` (2 janvier 1920, M1) | `0x04` (1 o) | 6 octets (`04 d8 64 39 47 56` ou `55`) |
| **Clé 5** | Date de décès | Tag 100, `20730` (4 octobre 2026) | `0x05` (1 o) | 6 octets (`05 d8 64 19 50 fa`) |
| **Clé 6** | Code de rite | `3` (Panthéon mémoriel) | `0x06` (1 o) | 2 octets (`06 03`) |
| **Clé 7** | Code pays | `"FR"` (ISO 3166-1) | `0x07` (1 o) | 4 octets (`07 62 46 52`) |
| **Clé 8** | Réf. Portrait Bloc 2 | Carte : SHA-256 (32 o) + Longueur ($\le 20\,480$ o, ex: `20480`, M6) | `0x08` (1 o) | 41 octets (`08 a2 01 58 20... 02 19 50 00`) |
| **Clé 9** | Réf. Mémo Vocal Bloc 3 | Carte : SHA-256 (32 o) + Longueur ($\le 46\,080$ o, ex: `46080`, M6) | `0x09` (1 o) | 41 octets (`09 a2 01 58 20... 02 19 b4 00`) |
| **Clé 10** | Identifiant émetteur | `"FR-PAR-AET-MOM-2026-0000000000000099"` (36 car.) | `0x0a` (1 o) | 39 octets |
| **Clé 11** | Date d'émission | Tag 100, `20730` (4 octobre 2026) | `0x0b` (1 o) | 6 octets (`0b d8 64 19 50 fa`) |
| **Clé 12** | Épitaphe / Hommage | Texte français solennel NFC ($1\,558$ octets UTF-8) | `0x0c` (1 o) | 1 562 octets (`0c 79 06 16 ...`) |
| **TOTAL CBOR** | **Charge utile Bloc 1** | Calibré avec contraintes M6 | | **1 876 octets** |

Enveloppe signée avec `kid` de 16 octets et en-tête protégé avec `typ` (135 octets d'overhead) : $1\,876 + 135 = \mathbf{2\,011\text{ octets}} \le 2\,048\text{ octets}$ (conforme au budget silicium de 2 Ko).

---

## A4. Enveloppe de Signature COSE_Sign1 (RFC 9052 & RFC 9596)

### 1. Spécification de l'Enveloppe

L'enveloppe utilise le tag CBOR standard `18` (RFC 9052 §4.2) et encapsule directement la charge utile (*attached payload*).

```cddl
COSE_Sign1_Memorial = #6.18([
  protected: bstr .cbor ProtectedHeaders,
  unprotected: UnprotectedHeaders,
  payload: bstr .cbor MemorialProfileV1,
  signature: bstr .size 64
])

ProtectedHeaders = {
  1 => alg,   ; Clé 1 = Algorithm Identifier (-8 EdDSA, -7 ES256)
  16 => typ,  ; Clé 16 = Content Type (RFC 9596 / RFC 9052 - Amendement M4)
}

alg = -8 / -7 ; -8 = EdDSA (Ed25519), -7 = ES256 (ECDSA P-256)
typ = "application/aeternitrak-profile+cbor"

UnprotectedHeaders = {
  ? 4 => kid, ; Clé 4 = Key Identifier (Amendement M3)
}

kid = bstr .size 16 ; Exactement 16 octets (16 premiers octets du SHA-256 de la clé publique émetteur)
```

### 2. Séparation de Domaine Cryptographique (Amendement M4)

Une même autorité ou opérateur peut détenir des clés aptes à signer à la fois des profils mémoriels et des certificats de lot de filière (« Porte de Fer », Ordre 0019/0020).
- Afin de prévenir toute substitution de contexte ou rejeu inter-domaines, l'en-tête **protégé** intègre impérativement l'étiquette **`typ` (étiquette 16, RFC 9596)**.
- Pour le profil mémoriel, `typ` est fixé à `"application/aeternitrak-profile+cbor"`. (La Porte de Fer utilise `"application/aeternitrak-batch-claim+cbor"`).
- **Règle de validation** : Tout lecteur ou vérificateur d'enveloppe AeterniTrak **doit obligatoirement vérifier la présence et la valeur exacte de ce paramètre `typ`** dans l'en-tête protégé avant toute interprétation ou décodage de la charge utile `payload`.

### 3. Modèle de Confiance Hors-Ligne & Gestion des Clés (Amendement M5)

- La validation cryptographique d'une carte ne repose jamais sur une clé publique transmise sans contrôle. L'application lectrice intègre en local une **liste d'émetteurs de confiance embarquée (offline-first)**.
- L'identifiant de clé `kid` (16 octets) correspond aux **16 premiers octets du SHA-256 de la clé publique** de l'émetteur.
- Si le `kid` de l'enveloppe ne correspond à aucun émetteur répertorié dans la base locale d'émetteurs approuvés, la signature est rejetée sans appel.
- Les mécanismes d'approvisionnement, de rotation et de révocation des clés relèvent de la responsabilité de Bushi 02 suite à l'arbitrage `DEC-AET-04`.

### 4. Agilité d'Algorithme et Particularité ES256 (Amendement M10 / `DEC-AET-04`)

Conformément à la décision d'architecture `DEC-AET-04` (Option C : ES256 pour les enclaves et puces, Ed25519 pour le logiciel, vérification des deux partout) :
- **Algorithme `-8` (EdDSA / Ed25519, RFC 8032)** : Utilisé pour les actes émis par les serveurs, le Studio et les validateurs logiciels. Les tests couvrent la génération déterministe de signature et la vérification.
- **Algorithme `-7` (ES256 / ECDSA sur secp256r1 avec SHA-256, RFC 9053)** : Utilisé pour les actes scellés par les enclaves matérielles mobiles (Apple Secure Enclave, Android StrongBox / KeyStore) et puces JavaCard ACOSJ. La signature est transmise au format binaire brut $r \| s$ de **64 octets exactement** (32 octets pour $r$, 32 octets pour $s$ en Big-Endian, sans encapsulation ASN.1 DER).
- **Règle de testabilité (M10)** : En raison du non-déterminisme intrinsèque des générateurs d'aléa matériels sous ECDSA, les suites de vecteurs de test pour ES256 sont opérées en **vérification seule** ; Ed25519 est validé en signature et en vérification.

### 5. Structure de Signature `Sig_structure` (RFC 9052 §4.4)

Le calcul et la vérification de la signature opèrent sur la sérialisation CBOR déterministe de la structure canonique `Sig_structure` :

```cddl
Sig_structure = [
  context: "Signature1",
  body_protected: bstr,       ; Exacts octets sérialisés de l'en-tête protégé
  external_aad: bstr .size 0, ; Chaîne d'octets vide h'' pour le Bloc 1
  payload: bstr               ; Octets bruts de la charge utile CBOR MemorialProfileV1
]
```

Pour ES256, le condensat signé est $M = \text{SHA-256}(\text{CBOR}(\text{Sig\_structure}))$. Pour Ed25519 (PureEd25519), la structure $\text{CBOR}(\text{Sig\_structure})$ est directement transmise à la primitive de signature.

---

## A5. Tables d'Octets des Trois Profils de Référence (AVN)

Les trois profils suivants sont documentés selon l'**AeterniTrak Vector Notation (AVN)** définie dans `qa/vectors/README.md` §3. Leurs encodages et empreintes SHA-256 ont été validés par calcul croisé et constituent les matrices des futurs vecteurs `draft`.

### 1. Profil Minimal (132 octets)
Profil compact destiné aux puces mémoire d'entrée de gamme ou aux transferts NFC ultra-rapides.
- **Champs présents** : Version 1, Sujet Humain, Nom d'usage "Guy", Naissance 1945-05-08 (-9004 jours), Décès 2026-10-04 (20730 jours), Rite laïque (1), Pays "BE", Empreintes et tailles des Blocs 2 et 3, Émetteur "BE-BRU-001", Date d'émission (20730 jours).

#### Notation AVN (JSON d'entrée calibré M6)
```json
{
  "$map": [
    [1, 1],
    [2, 1],
    [3, { "$map": [[1, "Guy"]] }],
    [4, { "$tag": 100, "$value": -9004 }],
    [5, { "$tag": 100, "$value": 20730 }],
    [6, 1],
    [7, "BE"],
    [8, {
      "$map": [
        [1, { "$bytes": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" }],
        [2, 18450]
      ]
    }],
    [9, {
      "$map": [
        [1, { "$bytes": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb" }],
        [2, 32400]
      ]
    }],
    [10, "BE-BRU-001"],
    [11, { "$tag": 100, "$value": 20730 }]
  ]
}
```

---

### 2. Profil Courant / Standard (Amendement M6)
Profil représentatif de la production courante AeterniTrak pour les concessions forestières mémorielles.
- **Champs présents** : Version 1, Sujet Humain, Noms (Usage "Dupont", Naissance "Dupont", Prénoms ["Guy", "Jean", "Arthur"]), Naissance 1950-01-15 (-7291 jours), Décès 2026-09-12 (20708 jours), Rite forestier (2), Pays "BE", Empreintes et tailles conformes des Blocs 2 et 3, Émetteur "BE-WAL-AET-2026-0042", Date d'émission (20730 jours), Épitaphe "Auprès de l'arbre vivant, la mémoire s'enracine pour toujours.".

#### Notation AVN (JSON d'entrée calibré M6)
```json
{
  "$map": [
    [1, 1],
    [2, 1],
    [3, {
      "$map": [
        [1, "Dupont"],
        [2, "Dupont"],
        [3, ["Guy", "Jean", "Arthur"]]
      ]
    }],
    [4, { "$tag": 100, "$value": -7291 }],
    [5, { "$tag": 100, "$value": 20708 }],
    [6, 2],
    [7, "BE"],
    [8, {
      "$map": [
        [1, { "$bytes": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae" }],
        [2, 19200]
      ]
    }],
    [9, {
      "$map": [
        [1, { "$bytes": "fcde2b2edba56bf408686f0477e2597b93ec45435329ae7e6fb0d20a0add9f84" }],
        [2, 45210]
      ]
    }],
    [10, "BE-WAL-AET-2026-0042"],
    [11, { "$tag": 100, "$value": 20730 }],
    [12, "Auprès de l'arbre vivant, la mémoire s'enracine pour toujours."]
  ]
}
```

---

### 3. Profil Maximal (Silicon Stress Test — Amendements M1, M6)
Profil de test de saturation siliconique, calibré pour prouver qu'un monument mémoriel littéraire et exhaustif reste strictement contenu sous la barre des $1\,900$ octets de charge utile et des $2\,048$ octets d'enveloppe signée.
- **Noms** : Patronyme long avec diacritiques ("De La Fontaine de Saint-Germain-des-Prés-lès-Eaux"), nom de naissance ("De La Tour d'Auvergne de Bouillon-Châtillon"), 6 prénoms complets.
- **Dates** : 1920-01-01 (-18263 jours, ou 1920-01-02 à -18262 jours) à 2026-10-04 (20730 jours).
- **Épitaphe** : Texte littéraire NFC de $1\,558$ octets UTF-8.

#### Notation AVN (JSON d'entrée calibré M1, M6)
```json
{
  "$map": [
    [1, 1],
    [2, 1],
    [3, {
      "$map": [
        [1, "De La Fontaine de Saint-Germain-des-Prés-lès-Eaux"],
        [2, "De La Tour d'Auvergne de Bouillon-Châtillon"],
        [3, ["Alexandre", "Barthélémy", "Charles", "Désiré", "Emmanuel", "Ferdinand"]]
      ]
    }],
    [4, { "$tag": 100, "$value": -18263 }],
    [5, { "$tag": 100, "$value": 20730 }],
    [6, 3],
    [7, "FR"],
    [8, {
      "$map": [
        [1, { "$bytes": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" }],
        [2, 20480]
      ]
    }],
    [9, {
      "$map": [
        [1, { "$bytes": "cb8379ac2098d92f6f1404c506377771560936ac6abb0bf76080784a00c0b35e" }],
        [2, 46080]
      ]
    }],
    [10, "FR-PAR-AET-MOM-2026-0000000000000099"],
    [11, { "$tag": 100, "$value": 20730 }],
    [12, "Sous les frondaisons centenaires du domaine mémoriel d'AeterniTrak, chaque pulsation du vent rappelle la fidélité, le dévouement et l'amour inaltérable légués à ceux qui continuent la marche terrestre. Puisse cette trace immuable, gravée au sein du silicium et scellée sous la garde des arbres protecteurs, traverser les cycles des saisons et le flux des générations sans jamais faiblir. L'existence trouve ici sa juste métamorphose : retour harmonieux à la poussière vivante, célébration de la beauté d'un parcours accompli, et transmission d'une mémoire claire, épurée de toute ombre. Ici reposent la bienveillance d'un regard, la noblesse des engagements pris et la paix souveraine d'un repos éternel mérité. Sous les frondaisons centenaires du domaine mémoriel d'AeterniTrak, chaque pulsation du vent rappelle la fidélité, le dévouement et l'amour inaltérable légués à ceux qui continuent la marche terrestre. Puisse cette trace immuable, gravée au sein du silicium et scellée sous la garde des arbres protecteurs, traverser les cycles des saisons et le flux des générations sans jamais faiblir. L'existence trouve ici sa juste métamorphose : retour harmonieux à la poussière vivante, célébration de la beauté d'un parcours accompli, et transmission d'une mémoire claire, épurée de toute ombre. Ici reposent la bienveillance d'un regard, la noblesse des engagements pris et la paix souveraine d'un repos éternel mérité. En cet asile forestier de sérénité et de grâce, la mémoire vit pour les siècles."]
  ]
}
```

> **Note Normative d'Audit & Dépôt des Vecteurs de Profil (Ordre 0012)** :  
> Conformément aux directives de l'Ordre 0012, les amendements M1 à M10 ont été intégrés à la spécification technique sans introduction de code de profil applicatif.  
> Suite à ces amendements, le Bushi 16 (QA) déposera les trois profils de référence recalculés dans la suite `draft` `qa/vectors/core/profile-v1.vectors.json` pour revue et approbation souveraine par Claude AI avant tout développement de modules de haut niveau.

---

## A6. API du Noyau TypeScript / WebAssembly

Le noyau AeterniCore est conditionné sous forme de module universel TypeScript (ESM pur, sans dépendance externe `dependencies: {}`, conforme à la Règle 5 de conformité) pouvant être exécuté nativement sous Node.js 22 LTS, dans un Service Worker de navigateur ou compilé via AssemblyScript / Rust vers WebAssembly.

### 1. Signatures des Fonctions Exportées

```typescript
/**
 * Encode un élément JavaScript / AVN en flux binaire CBOR déterministe.
 *
 * @param item - Élément à sérialiser (respectant le profil AeterniCore v1).
 * @returns Flux d'octets Uint8Array canonique.
 * @throws {CborError} Si l'élément contient un type interdit (flottant, undefined),
 *                     une clé dupliquée, ou un texte non-NFC.
 */
export function encode(item: unknown): Uint8Array;

/**
 * Décode un flux d'octets CBOR sous mode de validation strict.
 *
 * @param bytes - Buffer d'octets CBOR à valider et décoder.
 * @returns Structure de données décomposée en notation native/AVN.
 * @throws {CborError} Dès qu'une non-conformité déterministe est détectée
 *                     (longueur indéfinie, encodage non minimal, tri incorrect,
 *                     octets résiduels, UTF-8 invalide ou texte non-NFC).
 */
export function decodeStrict(bytes: Uint8Array): unknown;

/**
 * Canonise une structure JSON selon la spécification RFC 8785 (JCS).
 *
 * @param value - Objet, tableau ou valeur primitive JSON.
 * @returns Flux d'octets UTF-8 canonisé représentant le JSON scellé.
 * @throws {JcsError} En cas de valeur non sérialisable (cycles, NaN, Infinity).
 */
export function canonicalizeJson(value: unknown): Uint8Array;

/**
 * Valide une charge utile CBOR de profil mémoriel V1 selon les règles normatives AeterniCore.
 *
 * @param bytes - Buffer d'octets CBOR de la charge utile (budget maximal 1 900 octets).
 * @returns Résultat de validation { valid: true, len: number }.
 * @throws {ProfileError|CborError} Dès qu'une non-conformité de profil ou CBOR est détectée.
 */
export function validateProfile(bytes: Uint8Array): { valid: true; len: number };
```

### 2. Registre Normatif des Erreurs Typées

Les erreurs émises par `core/cbor/` et `core/jcs/` dérivent de `AeterniCoreError` et exposent obligatoirement une propriété `code: CborErrorCode` dont les valeurs correspondent **rigoureusement au registre officiel** défini dans `qa/vectors/README.md` §4.1 :

```typescript
export type CborErrorCode =
  | "ERR_CBOR_NOT_SHORTEST"      // Entier ou longueur non encodé sous forme minimale
  | "ERR_CBOR_INDEFINITE_LENGTH"  // Tentative d'encodage/décodage de longueur indéfinie
  | "ERR_CBOR_MAP_UNSORTED"       // Clés de carte non ordonnées selon le tri bytewise
  | "ERR_CBOR_DUPLICATE_KEY"      // Collision de clé au sein d'une même carte
  | "ERR_CBOR_TRAILING_BYTES"     // Octets orphelins résiduels après l'élément racine
  | "ERR_CBOR_TRUNCATED"          // Flux interrompu avant la fin attendue de la structure
  | "ERR_CBOR_MALFORMED"          // Structure binaire mal formée selon RFC 8949 §3
  | "ERR_CBOR_INVALID_UTF8"       // Séquence d'octets UTF-8 illégale ou surlongue
  | "ERR_CBOR_TEXT_NOT_NFC"       // Texte Unicode non normalisé en forme NFC
  | "ERR_CBOR_UNSUPPORTED_TYPE"   // Flottants, undefined, ou valeurs simples réservées
  | "ERR_CBOR_UNSUPPORTED_TAG"    // Tag non autorisé par le profil (hors tag 1 et 100)
  | "ERR_CBOR_TAG_CONTENT";       // Contenu inadapté pour le tag appliqué (ex: tag 100 non entier)

export class CborError extends Error {
  readonly code: CborErrorCode;
  readonly offset?: number;

  constructor(code: CborErrorCode, message: string, offset?: number) {
    super(`[${code}] ${message}${offset !== undefined ? ` at offset ${offset}` : ""}`);
    this.name = "CborError";
    this.code = code;
    this.offset = offset;
  }
}

export type ProfileErrorCode =
  | "ERR_PROFILE_TOO_LARGE"
  | "ERR_PROFILE_NOT_A_MAP"
  | "ERR_PROFILE_INVALID_KEY_TYPE"
  | "ERR_PROFILE_MISSING_FIELD"
  | "ERR_PROFILE_UNSUPPORTED_VERSION"
  | "ERR_PROFILE_UNKNOWN_FIELD"
  | "ERR_PROFILE_INVALID_SUBJECT_KIND"
  | "ERR_PROFILE_INVALID_NAME"
  | "ERR_PROFILE_TOO_MANY_NAMES"
  | "ERR_PROFILE_INVALID_DATE_TYPE"
  | "ERR_PROFILE_MISSING_BIRTH_DATE"
  | "ERR_PROFILE_INVALID_RITE"
  | "ERR_PROFILE_INVALID_COUNTRY"
  | "ERR_PROFILE_INVALID_ASSET_REF"
  | "ERR_PROFILE_INVALID_HASH_LENGTH"
  | "ERR_PROFILE_PORTRAIT_TOO_LARGE"
  | "ERR_PROFILE_VOICE_TOO_LARGE"
  | "ERR_PROFILE_INVALID_ISSUER_ID"
  | "ERR_PROFILE_INVALID_EPITAPH"
  | "ERR_PROFILE_INVALID_SPECIES";

export class ProfileError extends Error {
  readonly code: ProfileErrorCode;

  constructor(code: ProfileErrorCode, message: string) {
    super(`[${code}] ${message}`);
    this.name = "ProfileError";
    this.code = code;
  }
}
```

### 3. Exigences d'Implémentation & Portabilité
- **Zero-Dependency** : Aucun module externe de sérialisation (`cbor`, `cbor-x`, `canonical-json`, etc.) n'est autorisé en production. Tout le code source réside dans `core/cbor/` et `core/jcs/`.
- **APIs Web Standardisées** : Utilisation exclusive de `Uint8Array`, `DataView`, `TextEncoder`, `TextDecoder`, et `crypto.subtle` (Web Cryptography API).
- **Compatibilité Matérielle** : Garantie d'exécution identique sans divergence arithmétique sur Node.js 22 LTS, Chromium V8 (Pixel 9 / Android WebView), et JavaScriptCore (iOS / macOS Safari).
