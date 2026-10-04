# Spécification Technique & Formelle — Sécurité Cryptographique & Modèle de Confiance COSE_Sign1

> **Document ID** : `AET-SPEC-CRYPTO-001`  
> **Version** : 1.0.0  
> **Statut** : Soumis pour révision  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `ag/bushi-02-crypto-spec`  
> **Auteur** : Bushi 02 (Security & Cryptography Lead)  
> **Revue & Arbitrage** : Claude AI (Master Verifier)  
> **Autorité Souveraine** : Kudoro (`DECISIONS-KUDORO.md`, décision `DEC-AET-04` Option C)  
> **Contrats Partagés** : Bushi 01 (AeterniCore Déterminisme CBOR), Bushi 12 (Anti-Prion & The Iron Gate), Bushi 16 (QA Testvectors & Harnais)  
> **Phase du Chantier** : Phase A — Spécification Formelle Pure (Zéro code d'implémentation, zéro clé privée)

---

## 0. Recherches Documentaires Normatives Obligatoires

Conformément à la fiche de poste de Bushi 02 et aux exigences de l'Ordre 0032, les normes internationales, RFC de l'IETF et publications gouvernementales suivantes ont été étudiées et intégrées de manière contraignante :

1. **RFC 9052 — CBOR Object Signing and Encryption (COSE): Structures and Process**
   - *URL* : `https://www.rfc-editor.org/rfc/rfc9052.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Structure de l'enveloppe signée `COSE_Sign1` (§4.2), Tag CBOR `#6.18`, construction de la structure canonique à signer `Sig_structure` (§4.4) avec contexte `"Signature1"` et données associées externes `external_aad` fixées à une chaîne d'octets vide (`h''`).
2. **RFC 9053 — CBOR Object Signing and Encryption (COSE): Initial Algorithms**
   - *URL* : `https://www.rfc-editor.org/rfc/rfc9053.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Enregistrement IANA des identifiants d'algorithmes : `alg: -7` pour ECDSA avec SHA-256 sur courbe P-256 (`ES256`), et `alg: -8` pour EdDSA avec Ed25519 (`Ed25519`).
3. **RFC 8032 — Edwards-Curve Digital Signature Algorithm (EdDSA)**
   - *URL* : `https://www.rfc-editor.org/rfc/rfc8032.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Spécification d'Ed25519 pur (§5.1), génération de signature déterministe par double hachage SHA-512 sans aléa par signature, équation de vérification $8 S B = 8 R + 8 k A$, et rejet obligatoire des scalaires non canoniques $S \ge L$.
4. **RFC 9596 — CBOR Object Signing and Encryption (COSE) "typ" (type) Header Parameter**
   - *URL* : `https://www.rfc-editor.org/rfc/rfc9596.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Utilisation normalisée de l'étiquette protégée `16` (`typ`) pour séparer cryptographiquement les domaines d'application et empêcher formellement toute attaque par substitution de type de charge utile ou rejeu cross-domain.
5. **RFC 8949 — Concise Binary Object Representation (CBOR)**
   - *URL* : `https://www.rfc-editor.org/rfc/rfc8949.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Règles déterministes strictes (§4.2.1) : longueurs d'entiers les plus courtes, tri bytewise-lexicographique des clés de cartes, interdiction des longueurs indéfinies et des clés dupliquées.
6. **FIPS 186-5 — Digital Signature Standard (DSS)**
   - *URL* : `https://csrc.nist.gov/pubs/fips/186-5/final`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Définition formelle de l'algorithme ECDSA sur la courbe elliptique standard NIST P-256 (`prime256v1` / `secp256r1`), spécification des plages valides pour les scalaires $(r, s) \in [1, n-1]$.
7. **BSI TR-03111 — Technical Guideline: Elliptic Curve Cryptography (Version 2.10)**
   - *URL* : `https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03111/TR-03111_V-2-1.html`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Exigence de normalisation `s` bas (§4.1.3) pour l'élimination définitive de la malléabilité des signatures ECDSA ($s \le \lfloor n/2 \rfloor$), et encodage IEEE P1363 brut $r \parallel s$ sur 64 octets à taille fixe.
8. **SEC 1: Elliptic Curve Cryptography (Version 2.0)**
   - *URL* : `https://www.secg.org/sec1-v2.pdf`
   - *Date de consultation* : 4 octobre 2026
   - *Apports retenus* : Procédure formelle de validation des clés publiques sur la courbe (§3.2.2.1) : point non nul, coordonnées dans $\mathbb{F}_p$, satisfaction de l'équation de Weierstrass $y^2 \equiv x^3 - 3x + b \pmod p$, et appartenance au sous-groupe d'ordre premier $n$.

### 0.1 Périmètre V1 : Écartement Explicite & Motivé

Les technologies suivantes sont **formellement écartées du périmètre d'AeterniTrak V1.0** :

1. **zk-SNARK (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge)** :
   - *Motif d'exclusion* : La taille des circuits arithmétiques, l'empreinte mémoire et la puissance de calcul requises pour générer ou vérifier des preuves à divulgation nulle de connaissance excèdent largement le budget silicium de 92 Ko de la puce ACOSJ et les capacités d'un lecteur NFC mobile ou de station de pompes funèbres. L'écosystème de normalisation industrielle n'est pas stabilisé pour la traçabilité vétérinaire.
2. **SCP03 (GlobalPlatform Secure Channel Protocol 03)** :
   - *Motif d'exclusion* : SCP03 impose un canal symétrique chiffré point-à-point avec négociation préalable de clés secrètes partagées entre le lecteur et la carte. Cette exigence est incompatible avec le paradigme **Offline-First et Universel** d'AeterniTrak, où tout terminal mobile grand public ou d'inspection assermentée doit pouvoir lire et vérifier la carte sans détenir de clé secrète partagée.
3. **AES-GCM des données privées (Chiffrement de la charge utile sur carte)** :
   - *Motif d'exclusion* : Les données d'hommage funéraire (profil civil mémoriel) et les attestations sanitaires (filière sarcomusation) sont des assertions d'intérêt public dont **l'intégrité et l'authenticité séculaires sont recherchées, et non le secret d'État**. L'introduction d'un chiffrement AES-GCM poserait un écueil insoluble de séquestre et de transmission de clés privées symétriques sur 50 ou 100 ans. La V1 consacre l'intégrité publique signée.

---

## 1. Structure Formelle de l'Enveloppe COSE_Sign1

### 1.1 Définition CDDL Normative (RFC 9052 & RFC 9596)

L'enveloppe cryptographique est un message unique `COSE_Sign1` balisé par l'étiquette CBOR `#6.18` (Tag 18, `0xd2`), avec charge utile attachée (*attached payload*).

```cddl
; Enveloppe principale étiquetée COSE_Sign1
COSE_Sign1_Tagged = #6.18(COSE_Sign1)

COSE_Sign1 = [
  protected:   bstr .cbor ProtectedHeaders,   ; En-tête protégé sérialisé
  unprotected: UnprotectedHeaders,             ; En-tête non protégé (carte)
  payload:     bstr,                           ; Charge utile brute attachée
  signature:   bstr .size 64                   ; Signature cryptographique brute (64 octets)
]

; En-tête protégé : déterministe, non modifiable, couvert par la signature
ProtectedHeaders = {
  1 => alg,    ; Algorithme cryptographique autorisé (étiquette 1)
  16 => typ    ; Séparation de domaine applicatif (étiquette 16, RFC 9596)
}

alg = -8 / -7  ; -8 = Ed25519 (RFC 8032), -7 = ES256 (RFC 9053)

typ = "application/aeternitrak-profile+cbor" /
      "application/aeternitrak-batch-claim+cbor"

; En-tête non protégé : métadonnées d'acheminement et identification de clé
UnprotectedHeaders = {
  ? 4 => kid   ; Identifiant de la clé de signature (étiquette 4)
}

kid = bstr .size 16 ; Exactement 16 octets (SHA-256 tronqué de la clé publique)
```

### 1.2 Structure Canonique à Signer : `Sig_structure` (RFC 9052 §4.4)

La signature cryptographique n'est pas calculée directement sur la charge utile brute, mais sur la structure de contexte canonique normalisée `Sig_structure` définie par la RFC 9052 §4.4.

La structure `Sig_structure` est un tableau CBOR de 4 éléments encodé selon le profil déterministe strict d'AeterniCore :

```cddl
Sig_structure = [
  context:        "Signature1",               ; Contexte textuel fixe UTF-8
  body_protected: bstr .cbor ProtectedHeaders,; Octets bruts de l'en-tête protégé
  external_aad:   bstr .size 0,                ; Données associées externes : TOUJOURS vide (h'')
  payload:        bstr                         ; Octets bruts de la charge utile attachée
]
```

- **`context`** : Chaîne UTF-8 `"Signature1"` (encodée en CBOR par `0x6a5369676e617475726531`).
- **`body_protected`** : Champ `protected` exact extrait de l'enveloppe (chaîne d'octets `bstr` contenant la carte CBOR sérialisée `{1: alg, 16: typ}`).
- **`external_aad`** : Chaîne d'octets vide de longueur 0, encodée en CBOR par `0x40` (`h''`). AeterniTrak V1 n'utilise aucune AAD externe afin de préserver l'autonomie totale hors-ligne de l'enveloppe.
- **`payload`** : Champ `payload` exact extrait de l'enveloppe (chaîne d'octets `bstr`).

La séquence d'octets à signer ou à vérifier, désignée par **TBS** (*To-Be-Signed*), est obtenue par l'encodage CBOR déterministe strict de `Sig_structure` :

$$\text{TBS} = \text{CBOR\_Deterministic\_Encode}(\text{Sig\_structure})$$

Pour Ed25519 : la signature porte directement sur $\text{TBS}$.  
Pour ES256 : la signature porte sur le condensat $\text{SHA-256}(\text{TBS})$.

---

### 1.3 Les 4 Combinaisons Normatives de l'En-Tête Protégé

L'en-tête protégé contient obligatoirement les clés `1` (`alg`) et `16` (`typ`).  
Conformément à la RFC 8949 §4.2.1, les clés entières sont triées selon leur encodage CBOR bytewise-lexicographique :  
- La clé `1` s'encode sur un octet : `0x01`.  
- La clé `16` s'encode sur un octet : `0x10`.  
- Puisque `0x01 < 0x10`, la paire `(1, alg)` précède obligatoirement la paire `(16, typ)`.

Voici la spécification exacte octet par octet des 4 combinaisons possibles :

#### Combinaison 1 : Ed25519 (`alg: -8`) × Profil Mémoriel (`typ: application/aeternitrak-profile+cbor`)
- **Carte logique** : `{1: -8, 16: "application/aeternitrak-profile+cbor"}`
- **Taille de la carte brute** : 42 octets
- **Octets hexadécimaux de la carte déterministe brute** :
  ```hex
  a201271078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72
  ```
  *Décomposition* :
  - `a2` : carte de 2 paires
  - `01` : clé entière 1 (`alg`)
  - `27` : entier négatif -8 (`-1 - 7`)
  - `10` : clé entière 16 (`typ`)
  - `78 24` : chaîne textuelle UTF-8 de 36 octets (`0x24 = 36`)
  - `61...626f72` : texte `"application/aeternitrak-profile+cbor"`
- **Taille encapsulée dans l'enveloppe (`bstr`)** : 44 octets
- **Octets hexadécimaux de l'élément `protected` encapsulé** :
  ```hex
  582aa201271078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72
  ```
  *(Préfixe `58 2a` : major type 2 `bstr` de longueur 42 octets).*

#### Combinaison 2 : ES256 (`alg: -7`) × Profil Mémoriel (`typ: application/aeternitrak-profile+cbor`)
- **Carte logique** : `{1: -7, 16: "application/aeternitrak-profile+cbor"}`
- **Taille de la carte brute** : 42 octets
- **Octets hexadécimaux de la carte déterministe brute** :
  ```hex
  a201261078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72
  ```
  *Décomposition* :
  - `a2 01` : carte 2 paires, clé 1
  - `26` : entier négatif -7 (`-1 - 6`)
  - `10 78 24` : clé 16, texte de 36 octets
  - `61...626f72` : texte `"application/aeternitrak-profile+cbor"`
- **Taille encapsulée dans l'enveloppe (`bstr`)** : 44 octets
- **Octets hexadécimaux de l'élément `protected` encapsulé** :
  ```hex
  582aa201261078246170706c69636174696f6e2f61657465726e697472616b2d70726f66696c652b63626f72
  ```

#### Combinaison 3 : Ed25519 (`alg: -8`) × Revendication de Lot (`typ: application/aeternitrak-batch-claim+cbor`)
- **Carte logique** : `{1: -8, 16: "application/aeternitrak-batch-claim+cbor"}`
- **Taille de la carte brute** : 46 octets
- **Octets hexadécimaux de la carte déterministe brute** :
  ```hex
  a201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72
  ```
  *Décomposition* :
  - `a2 01 27` : carte 2 paires, clé 1 = -8
  - `10` : clé 16
  - `78 28` : chaîne textuelle UTF-8 de 40 octets (`0x28 = 40`)
  - `61...626f72` : texte `"application/aeternitrak-batch-claim+cbor"`
- **Taille encapsulée dans l'enveloppe (`bstr`)** : 48 octets
- **Octets hexadécimaux de l'élément `protected` encapsulé** :
  ```hex
  582ea201271078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72
  ```
  *(Préfixe `58 2e` : major type 2 `bstr` de longueur 46 octets).*

#### Combinaison 4 : ES256 (`alg: -7`) × Revendication de Lot (`typ: application/aeternitrak-batch-claim+cbor`)
- **Carte logique** : `{1: -7, 16: "application/aeternitrak-batch-claim+cbor"}`
- **Taille de la carte brute** : 46 octets
- **Octets hexadécimaux de la carte déterministe brute** :
  ```hex
  a201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72
  ```
  *Décomposition* :
  - `a2 01 26` : carte 2 paires, clé 1 = -7
  - `10 78 28` : clé 16, texte de 40 octets
  - `61...626f72` : texte `"application/aeternitrak-batch-claim+cbor"`
- **Taille encapsulée dans l'enveloppe (`bstr`)** : 48 octets
- **Octets hexadécimaux de l'élément `protected` encapsulé** :
  ```hex
  582ea201261078286170706c69636174696f6e2f61657465726e697472616b2d62617463682d636c61696d2b63626f72
  ```

---

## 2. Spécification Formelle des Algorithmes Cryptographiques (DEC-AET-04)

Conformément à l'arbitrage souverain `DEC-AET-04` (Option C : Agilité COSE hybride), AeterniTrak supporte **deux et seulement deux** algorithmes asymétriques au sein de la V1. Tout autre algorithme est interdit et immédiatement rejeté.

| Algorithme | Identifiant COSE | Standard | Format Clé Publique | Format Signature | Ancrage Cible |
|---|---|---|---|---|---|
| **Ed25519** | `alg: -8` | RFC 8032 | 32 octets compressés | 64 octets ($R \parallel S$) | Signatures logicielles, P2P, evaluateur Porte de Fer |
| **ES256** | `alg: -7` | RFC 9053 / FIPS 186-5 | 64 octets ($X \parallel Y$) | 64 octets ($r \parallel s$ normalisé *low-s*) | Enclaves matérielles (Secure Enclave, StrongBox, ACOSJ 92k) |

---

### 2.1 Spécification d'Ed25519 (`alg: -8`, RFC 8032)

1. **Courbe et Corps** : Courbe d'Edwards tordue définie sur le corps fini $\mathbb{F}_{2^{255}-19}$ d'équation $-x^2 + y^2 = 1 - \frac{121665}{121666} x^2 y^2$.
2. **Ordre du groupe** : L'ordre du point de base $B$ est le nombre premier :
   $$L = 2^{252} + 27742317777372353535851937790883648493$$
3. **Format de Signature** : 64 octets exactement, concaténation de la représentation compressée du point $R$ (32 octets) et du scalaire $S$ (32 octets, *little-endian*).
4. **Vérification Mathématique Stricte (RFC 8032 §5.1.7)** :
   - Rejet immédiat si la signature ne comporte pas exactement 64 octets.
   - Rejet si la clé publique ne comporte pas exactement 32 octets.
   - Décompression du point $A$ (clé publique) : le décodage doit réussir et le point doit être sur la courbe.
   - **Contrôle de canonicité de $S$** : L'entier $S$ doit satisfaire strictement $0 \le S < L$. Si $S \ge L$, la signature **doit être rejetée**.
   - Calcul de $k = \text{SHA-512}(R \parallel A \parallel \text{TBS}) \pmod L$.
   - Décompression du point $R$.
   - Vérification de l'équation de groupe : $8 S B = 8 R + 8 k A$.

---

### 2.2 Spécification d'ES256 (`alg: -7`, NIST P-256 / FIPS 186-5)

1. **Courbe et Paramètres de Domaine** : Courbe de Weierstrass de standard NIST P-256 (`secp256r1`) sur le corps $\mathbb{F}_p$ avec :
   - Premier $p = 2^{256} - 2^{224} + 2^{192} + 2^{96} - 1$
   - Équation : $y^2 \equiv x^3 - 3x + b \pmod p$
   - Ordre du point de base $n$ :
     $$n = \text{0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551}$$
   - Demi-ordre de la courbe :
     $$\left\lfloor \frac{n}{2} \right\rfloor = \text{0x7FFFFFFF800000007FFFFFFFFFFFFFFFDE737D56D38BCE4279DC65617E3192A8}$$
2. **Format de Signature** : Format IEEE P1363 (BSI TR-03111 §4.1.3), 64 octets exactement : concaténation de l'entier $r$ (32 octets, *big-endian*) et de l'entier $s$ (32 octets, *big-endian*). Les formats ASN.1 / DER sont formellement rejetés.
3. **Validation Impérative de la Clé Publique sur la Courbe (SEC 1 §3.2.2.1)** :
   Tout vérificateur ES256 doit impérativement valider la clé publique $Q = (X, Y)$ avant tout calcul :
   - $Q \ne \mathcal{O}$ (le point n'est pas le point à l'infini).
   - $X, Y \in [0, p-1]$.
   - Le point satisfait l'équation de courbe : $Y^2 \equiv X^3 - 3X + b \pmod p$.
   - L'ordre du point est $n$ ($n \cdot Q = \mathcal{O}$).
4. **Règle Absolue du `s` Bas (Low-s Requirement — BSI TR-03111 §4.1.3)** :
   - En cryptographie ECDSA, si une paire $(r, s)$ est une signature valide d'un message sous une clé publique donnée, alors $(r, n - s \pmod n)$ est également une signature mathématiquement valide. Cette propriété induit une **malléabilité** intrinsèque de la signature, permettant à un tiers de modifier les octets de l'enveloppe sans invalider la vérification cryptographique.
   - **Règle d'AeterniTrak** : Tout vérificateur ES256 **DOIT IMPÉRATIVEMENT REJETER** toute signature où :
     $$s > \left\lfloor \frac{n}{2} \right\rfloor$$
   - En cas de $s > \lfloor n/2 \rfloor$, la vérification échoue avec l'erreur `ERR_COSE_MALLEABLE_SIGNATURE`.
   - Lors de la signature sur puce ou enclave matérielle, si le coprocesseur produit une composante $s > \lfloor n/2 \rfloor$, la couche d'enveloppement doit impérativement normaliser la signature en substituant $s \leftarrow n - s$ avant toute sérialisation de l'enveloppe.

---

## 3. Ordre Normatif de Vérification & Registre des Erreurs `ERR_COSE_*`

L'ordre de vérification suivant est **strictement normatif**. Aucune étape ne peut être inversée, sautée ou reportée. En particulier, **la charge utile ne doit sous aucun prétexte être inspectée ou désérialisée avant que l'authenticité et l'intégrité cryptographiques n'aient été formellement établies**.

```
[Flux binaire reçu]
        │
        ▼
   [Étape 1] Décodage CBOR déterministe strict ─────────────► Échec : ERR_COSE_CBOR_DECODE
        │
        ▼
   [Étape 2] Structure enveloppe COSE_Sign1 (#6.18) ────────► Échec : ERR_COSE_INVALID_ENVELOPE
        │
        ▼
   [Étape 3] Contrôle de l'algorithme (alg ∈ {-8, -7}) ─────► Échec : ERR_COSE_UNSUPPORTED_ALGORITHM
        │
        ▼
   [Étape 4] Concordance du domaine applicatif (typ) ───────► Échec : ERR_COSE_TYPE_MISMATCH
        │
        ▼
   [Étape 5] Recherche kid dans la liste de confiance ──────► Échec : ERR_COSE_UNTRUSTED_KEY
        │                                                              (ou MISSING / UNKNOWN / EXPIRED / REVOKED)
        ▼
   [Étape 6] Concordance alg déclaré vs Trust Store ────────► Échec : ERR_COSE_ALGORITHM_MISMATCH
        │
        ▼
   [Étape 7] Validation signature (Ed25519 ou ES256 low-s) ─► Échec : ERR_COSE_INVALID_SIGNATURE
        │                                                              (ou MALLEABLE / INVALID_PUBLIC_KEY)
        ▼
   [Étape 8] Déverrouillage sécurisé du Payload
```

---

### 3.1 Détail Testable des 8 Étapes Normatives

Chaque règle est spécifiée de manière formellement testable sous le triptyque : **Entrée, Condition de Rejet, Code d'Erreur & Résultat**.

#### Étape 1 : Décodage Binaire Strict CBOR
- **Entrée** : `raw_bytes` (tableau d'octets du message complet).
- **Condition de Rejet** : Tout flux non conforme au profil déterministe strict RFC 8949 / AeterniCore : entier non minimal, longueur indéfinie, octets résiduels en fin de flux (*trailing bytes*), carte non triée selon l'ordre lexicographique, clés dupliquées, texte non normalisé NFC, ou présence de flottants.
- **Code d'Erreur** : `ERR_COSE_CBOR_DECODE` (ou propagation de l'erreur native sous-jacente `ERR_CBOR_*`).
- **Résultat** : Abandon immédiat de la lecture.

#### Étape 2 : Forme et Typage de l'Enveloppe COSE_Sign1
- **Entrée** : Élément CBOR décodé `cbor_item`.
- **Condition de Rejet** :
  1. L'élément n'est pas balisé par le Tag CBOR `18` (`cbor_item.$tag !== 18`).
  2. Le contenu déballé n'est pas un tableau de 4 éléments exactement.
  3. L'élément 0 (`protected`) n'est pas une chaîne d'octets (`bstr`).
  4. L'élément 1 (`unprotected`) n'est pas une carte CBOR.
  5. L'élément 2 (`payload`) n'est pas une chaîne d'octets (`bstr`).
  6. L'élément 3 (`signature`) n'est pas une chaîne d'octets de 64 octets exactement.
- **Code d'Erreur** : `ERR_COSE_INVALID_ENVELOPE`.
- **Résultat** : Rejet immédiat, aucun décodage de l'en-tête protégé n'est tenté.

#### Étape 3 : Validation de l'Algorithme Cryptographique Déclaré
- **Entrée** : Champ `protected` extrait (décodé en carte CBOR `{1: alg, 16: typ}`).
- **Condition de Rejet** :
  1. L'en-tête protégé ne contient pas la clé `1` (`alg`).
  2. La valeur associée à `alg` n'est pas un entier relatif.
  3. La valeur de `alg` n'appartient pas à la liste blanche stricte $\{-8, -7\}$.
- **Code d'Erreur** : `ERR_COSE_UNSUPPORTED_ALGORITHM`.
- **Résultat** : Rejet de l'enveloppe.

#### Étape 4 : Validation du Paramètre de Séparation de Domaine `typ`
- **Entrée** : Carte d'en-tête protégé, et type attendu par l'application appelante `expected_typ`.
- **Condition de Rejet** :
  1. L'en-tête protégé ne contient pas la clé `16` (`typ`).
  2. La valeur associée à `typ` n'est pas une chaîne de caractères UTF-8.
  3. La valeur de `typ` est différente de `expected_typ` (ex. une revendication de lot présentée à un lecteur de profil mémoriel, ou un type tiers inconnu).
- **Code d'Erreur** : `ERR_COSE_TYPE_MISMATCH`.
- **Résultat** : Rejet immédiat. Toute confusion de domaine ou tentative de rejeu cross-domain est neutralisée.

#### Étape 5 : Résolution du `kid` dans la Liste de Confiance Locale (Trust Store)
- **Entrée** : Carte `unprotected`, registre d'émetteurs de confiance embarqué localement (`TrustStore`), timestamp de vérification `now`.
- **Condition de Rejet** :
  1. L'en-tête non protégé ne contient pas la clé `4` (`kid`) ou `kid` n'a pas une taille de 16 octets : rejet avec `ERR_COSE_MISSING_KID`.
  2. Le `kid` est absent de la liste locale des émetteurs certifiés : rejet avec `ERR_COSE_UNKNOWN_KID`.
  3. L'entrée de confiance associée est marquée révoquée (`status === "REVOKED"`) : rejet avec `ERR_COSE_REVOKED_KEY`.
  4. La date de vérification est hors de l'intervalle de validité de la clé (`now < valid_from` ou `now > valid_until`) : rejet avec `ERR_COSE_EXPIRED_KEY`.
- **Code d'Erreur Générique** : `ERR_COSE_UNTRUSTED_KEY`.
- **Résultat** : La clé publique ne provient JAMAIS de la carte physique, mais uniquement du stockage de confiance local.

#### Étape 6 : Concordance de l'Algorithme Déclaré avec la Liste de Confiance
- **Entrée** : `alg` issu de l'en-tête protégé, et champ `alg` assigné à ce `kid` dans le Trust Store.
- **Condition de Rejet** : L'algorithme déclaré dans l'enveloppe ne correspond pas à l'algorithme assigné à cette clé dans le registre de confiance (`protected.alg !== trusted_entry.alg`).
- **Code d'Erreur** : `ERR_COSE_ALGORITHM_MISMATCH`.
- **Résultat** : Rejet immédiat (empêche toute attaque par rétrogradation ou substitution d'algorithme).

#### Étape 7 : Vérification Cryptographique de la Signature
- **Entrée** : Clé publique de confiance résolue à l'étape 5, signature (64 octets), structure `Sig_structure` calculée sur `(protected, h'', payload)`.
- **Condition de Rejet** :
  1. Si `alg === -7` (ES256) :
     - La clé publique ne satisfait pas les équations de validation sur la courbe P-256 : rejet avec `ERR_COSE_INVALID_PUBLIC_KEY`.
     - Les composantes de signature $r, s \notin [1, n-1]$ : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
     - **Violation de la règle low-s** ($s > \lfloor n/2 \rfloor$) : rejet avec `ERR_COSE_MALLEABLE_SIGNATURE`.
     - L'opération mathématique de vérification ECDSA échoue : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
  2. Si `alg === -8` (Ed25519) :
     - Le point de clé publique ou le point $R$ ne sont pas valides sur la courbe Edwards25519 : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
     - Le scalaire $S \ge L$ (non canonique) : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
     - L'équation de vérification $8 S B = 8 R + 8 k A$ échoue : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
- **Code d'Erreur** : `ERR_COSE_INVALID_SIGNATURE` (ou `ERR_COSE_MALLEABLE_SIGNATURE` / `ERR_COSE_INVALID_PUBLIC_KEY`).
- **Résultat** : En cas d'échec, aucune charge utile n'est déverrouillée.

#### Étape 8 : Déverrouillage et Restitution de la Charge Utile
- **Entrée** : Enveloppe validée aux étapes 1 à 7.
- **Condition de Réalisation** : L'application n'accède au contenu brut de `payload` que si et seulement si l'étape 7 a retourné un statut de succès cryptographique absolu.
- **Sanction en cas d'accès direct anticipé** : Tout composant logiciel tentant d'interpréter le payload sans acquittement cryptographique préalable lève l'exception fatale `ERR_COSE_UNVERIFIED_PAYLOAD_ACCESS`.
- **Résultat** : Restitution de `payload` certifié intègre et authentique pour désérialisation métier par le récepteur (AeterniCore pour profil civil, The Iron Gate pour certificat de lot).

---

### 3.2 Registre Normatif des Codes d'Erreur Typés

| Code d'Erreur | Étape | Signification Formelle |
|---|---|---|
| `ERR_COSE_CBOR_DECODE` | 1 | Échec du décodage CBOR déterministe du flux reçu. |
| `ERR_COSE_INVALID_ENVELOPE` | 2 | Structure non conforme (tag ≠ 18, tableau ≠ 4 éléments, types invalides). |
| `ERR_COSE_UNSUPPORTED_ALGORITHM` | 3 | Algorithme non autorisé ou absent de la liste blanche `{-8, -7}`. |
| `ERR_COSE_TYPE_MISMATCH` | 4 | Paramètre `typ` (étiquette 16) manquant, malformé ou non concordant. |
| `ERR_COSE_MISSING_KID` | 5 | Clé 4 (`kid`) absente de l'en-tête non protégé ou taille ≠ 16 octets. |
| `ERR_COSE_UNKNOWN_KID` | 5 | Identifiant `kid` inconnu dans la liste de confiance locale. |
| `ERR_COSE_REVOKED_KEY` | 5 | Clé révoquée dans la liste de révocation locale. |
| `ERR_COSE_EXPIRED_KEY` | 5 | Clé expirée (date de validité échue au moment de l'émission). |
| `ERR_COSE_UNTRUSTED_KEY` | 5 | Échec générique de confiance de la clé d'émission. |
| `ERR_COSE_ALGORITHM_MISMATCH` | 6 | L'algorithme déclaré ne correspond pas à celui assigné dans le Trust Store. |
| `ERR_COSE_INVALID_PUBLIC_KEY` | 7 | Clé publique invalide ou non située sur la courbe P-256. |
| `ERR_COSE_MALLEABLE_SIGNATURE` | 7 | Signature ES256 malléable rejetée ($s > \lfloor n/2 \rfloor$, violation BSI TR-03111). |
| `ERR_COSE_INVALID_SIGNATURE` | 7 | Signature mathématiquement corrompue ou falsifiée. |
| `ERR_COSE_UNVERIFIED_PAYLOAD_ACCESS` | 8 | Tentative d'accès au payload sans vérification cryptographique complète. |

---

## 4. Modèle de Confiance Hors-Ligne (Offline-First Trust Model)

### 4.1 La Règle d'Or de Sécurité

> [!CAUTION]
> **Règle d'Or Absolue d'AeterniTrak** :  
> **La clé publique lue sur une carte physique ne fait JAMAIS autorité par elle-même.**  
> Une carte ou puce NFC ne peut en aucun cas s'auto-authentifier en transmettant sa propre clé publique non vérifiée.  
> La clé publique servant à la vérification provient **exclusivement** du magasin de confiance local (*Trust Store*) embarqué dans l'application lectrice.

---

### 4.2 Calcul Mathématique du `kid` (Key Identifier)

L'identifiant de clé `kid` est un condensat cryptographique de 16 octets (128 bits), garantissant une unicité statistique absolue et une résistance aux collisions :

$$\text{kid} = \text{SHA-256}(\text{raw\_public\_key})[0..15]$$

- **Pour Ed25519** : `raw_public_key` correspond aux 32 octets bruts de la clé publique compressée (point $A$, RFC 8032).
- **Pour ES256** : `raw_public_key` correspond aux 64 octets bruts de la concaténation big-endian des coordonnées affines $(X \parallel Y)$ du point sur la courbe P-256 (32 octets pour $X$, 32 octets pour $Y$).
- **En-tête non protégé** : Le `kid` est transporté dans l'en-tête non protégé sous la clé entière standard `4` :
  ```hex
  a10450<16 octets du kid>
  ```
  *(Préfixe `a1 04 50` : carte 1 paire, clé 4, chaîne d'octets `bstr` de 16 octets `0x50`).*

---

### 4.3 Format du Registre d'Émetteurs Embarqué (Trust Store)

L'application lectrice (iOS, Android, CLI d'audit) embarque dans ses ressources compilées un registre scellé des émetteurs autorisés.

```cddl
TrustStore = {
  version: uint,                         ; Numéro de version monotone croissant
  updated_at: uint,                      ; Date de publication (timestamp UNIX secondes)
  signers: [* TrustedIssuerEntry]        ; Liste des entrées de confiance
}

TrustedIssuerEntry = {
  kid: bstr .size 16,                    ; Identifiant calculé (16 octets)
  alg: -8 / -7,                          ; Algorithme unique assigné
  public_key: bstr,                      ; Octets bruts de la clé publique (32 ou 64 octets)
  role: "MEMORIAL_STATION" /             ; Rôle opérationnel strict
        "BATCH_CONFORMITY" / 
        "REGULATOR_AUDIT" / 
        "POLICY_SIGNER",
  typ: text,                             ; Paramètre typ associé obligatoire
  issuer_id: text,                       ; Identifiant officiel (ex: FR-PAR-AET-MOM-2026-0000000000000099)
  valid_from: uint,                      ; Début de validité (timestamp UNIX secondes)
  valid_until: uint,                     ; Fin de validité (timestamp UNIX secondes)
  status: "ACTIVE" / "REVOKED"           ; État opérationnel de la clé
}
```

---

### 4.4 Règle d'Étanchéité : « Une Clé, Un Algorithme, Un Rôle, Un Type »

Pour éliminer toute ambiguïté sémantique et parer toute attaque par réutilisation de clé (*cross-protocol key reuse*), AeterniTrak applique une règle d'étanchéité stricte :

1. **Une clé cryptographique est assignée à un algorithme unique** : Une même clé ne peut jamais être sollicitée ou déclarée sous un algorithme différent.
2. **Une clé cryptographique est assignée à un rôle métier unique** : Une station de pompes funèbres ne peut jamais émettre une attestation sanitaire de lot ; un laboratoire d'analyse ne peut jamais émettre un profil civil mémoriel.
3. **Une clé cryptographique est assignée à un type de contenu unique (`typ`)** : L'étiquette `16` protégée scelle définitivement le contexte d'interprétation.

---

### 4.5 Rotation et Révocation Hors-Ligne (Zero-Network)

AeterniTrak opère dans des environnements dépourvus de connectivité réseau (chambres funéraires en sous-sol, forêts cinéraires reculées, abattoirs isolés, postes d'équarrissage industriels). Aucune requête en ligne (OCSP, CRL sur serveur HTTP) n'est requise.

1. **Mises à Jour Monotones Signées** : Les révocations de clés compromises et l'enregistrement de nouveaux émetteurs sont distribués via les mises à jour standard de l'application (App Store, Google Play, paquets d'audit signés).
2. **Champ `status: "REVOKED"`** : Tout `kid` révoqué voit son statut mis à jour dans le Trust Store. Toute tentative de vérification d'une carte portant ce `kid` échoue immédiatement avec l'erreur `ERR_COSE_REVOKED_KEY`.
3. **Fenêtre de Validité (`valid_from` / `valid_until`)** : Chaque clé possède une durée de vie maximale certifiée (3 ans par défaut pour les stations funéraires). Une signature émise en dehors de cette plage est rejetée avec `ERR_COSE_EXPIRED_KEY`.

---

### 4.6 Comportement et Interface Utilisateur (UX / UI Hors-Ligne)

Lorsque la vérification échoue, l'application lectrice affiche un retour clair et non ambigu à l'utilisateur :

- **Clé Inconnue (`ERR_COSE_UNKNOWN_KID`)** :  
  *Affichage* : Bannière orange d'avertissement.  
  *Message* : *"Carte non reconnue — Émetteur inconnu. Cette carte mémorielle a été émise par une autorité non répertoriée dans votre application. Les données ne peuvent être certifiées authentiques. Si cette carte est récente, veuillez mettre à jour votre application AeterniTrak."*
- **Clé Expirée (`ERR_COSE_EXPIRED_KEY`)** :  
  *Affichage* : Bannière orange d'alerte temporelle.  
  *Message* : *"Clé d'émission expirée. La station d'émission de cette carte utilisait une clé hors de sa période de validité. Veuillez contacter votre conseiller funéraire PaxFunèbre."*
- **Clé Révoquée (`ERR_COSE_REVOKED_KEY`)** :  
  *Affichage* : Bannière rouge vif d'interdiction.  
  *Message* : *"ALERTE SÉCURITÉ : Clé révoquée. Cette carte a été signée par une clé compromise ou signalée révoquée. L'accès aux données est bloqué par précaution."*
- **Signature Invalide / Falsification (`ERR_COSE_INVALID_SIGNATURE` ou `ERR_COSE_MALLEABLE_SIGNATURE`)** :  
  *Affichage* : Bannière rouge vif d'intégrité compromise.  
  *Message* : *"ALERTE SÉCURITÉ : Falsification détectée. L'empreinte cryptographique de la carte est corrompue ou a subi une tentative d'altération physique. Les données de la puce sont invalidées."*

---

## 5. Séparation des 4 Familles de Clés & Découpage Métier

AeterniTrak segmente l'architecture cryptographique en quatre familles de clés hermétiques :

```
                  ┌────────────────────────────────────────────────────────┐
                  │          ARCHITECTURE CRYPTOGRAPHIQUE AETERNITRAK      │
                  └────────────────────────────────────────────────────────┘
                                 │                            │
             ┌───────────────────┴──────────┐   ┌─────────────┴─────────────────┐
             │       FAMILLES MATÉRIELLES   │   │      FAMILLES LOGICIELLES     │
             │          (ES256 / -7)        │   │          (Ed25519 / -8)       │
             └──────────────────────────────┘   └───────────────────────────────┘
                     │              │                   │               │
                     ▼              ▼                   ▼               ▼
               [Famille 1]    [Famille 3]         [Famille 2]     [Famille 4]
                Hommage &     Inspection &        Conformité      Politique
                Mémorial      Audit Légal          Sanitaire      Dérogatoire
               PaxFunèbre     AFSCA / DNF         The Iron Gate   DEC-AET-05
```

### 5.1 Matrice Détaillée des 4 Familles de Clés

| Famille | Rôle Opérationnel | Algorithme Assigné | Support d'Exécution & Emplacement | Paramètre `typ` Obligatoire |
|---|---|---|---|---|
| **Famille 1 : Clé d'Hommage Mémoriel** | Signature des profils civils d'hommage humain et animaux de compagnie (Bloc 1 du Sanctuaire). | **ES256 (`alg: -7`)** | Enclave matérielle sécurisée : Apple Secure Enclave, Android StrongBox sur tablette de station funéraire PaxFunèbre, ou carte opérateur JavaCard ACOSJ 92k. | `"application/aeternitrak-profile+cbor"` |
| **Famille 2 : Clé de Conformité de Lot** | Signature des attestations de conformité sanitaire et feed-ban de la filière de sarcomusation (Portes G0 à G9 de The Iron Gate). | **Ed25519 (`alg: -8`)** | Serveur durci de laboratoire d'analyse vétérinaire agréé ou micro-service de validation certifié. | `"application/aeternitrak-batch-claim+cbor"` |
| **Famille 3 : Clé d'Audit Régulateur** | Contre-signature d'inspection officielle, constats de prélèvement, scellés vétérinaires et visas douaniers d'exportation. | **ES256 (`alg: -7`)** | Terminal d'inspection durci des agents de l'État (AFSCA / DNF) avec puce Secure Element ou carte d'agent assermenté ACOSJ 92k. | `"application/aeternitrak-audit-claim+cbor"` |
| **Famille 4 : Clé de Politique Dérogatoire** | Signature de la politique d'autorisation administrative d'amendement forestier cinéraire privé pour dépouilles de compagnie Catégorie 1 LFA-négatives (`DEC-AET-05`). | **Ed25519 (`alg: -8`)** *(ou ES256)* | HSM souverain d'administration centrale (DGO3 / AFSCA) ou autorité réglementaire. | `"application/aeternitrak-policy+cbor"` |

### 5.2 Rationale des Choix Algorithmiques

- **Pourquoi ES256 pour les familles 1 et 3 ?**  
  Les stations funéraires PaxFunèbre et les agents d'inspection opèrent sur des équipements mobiles (iPad, terminaux Android durcis, cartes à puce JavaCard). Les puces de sécurité matérielle (Apple Secure Enclave, Android StrongBox, ACOSJ 92k) intègrent nativement des accélérateurs cryptographiques certifiés FIPS 140-2/3 et Common Criteria EAL5+ pour la courbe NIST P-256. L'usage d'ES256 garantit que la clé privée ne peut physiquement pas être extraite du silicium.
- **Pourquoi Ed25519 pour la famille 2 (Porte de Fer) ?**  
  La filière de sarcomusation requiert le traitement de dizaines de milliers de lots industriels et de requêtes P2P décentralisées. Ed25519 offre une vitesse d'exécution supérieure, une dérivation déterministe mathématique exempte de génération d'aléa par signature (éliminant tout risque de fuite de clé par biais du générateur aléatoire), et une immunité totale contre la malléabilité.

---

## 6. Stockage Matériel Sécurisé & Résilience Silicium

### 6.1 Architecture des Enclaves Matérielles Supportées

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 ENCLAVES MATÉRIELLES CERTIFIÉES (NON EXPORTABLES)            │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│    Apple Secure Enclave      │     Android StrongBox        │ JavaCard      │
│        (iOS / macOS)         │       (Android 9+)           │  ACOSJ 92k    │
├──────────────────────────────┼──────────────────────────────┼───────────────┤
│ Coprocesseur SEP isolé       │ Puce Secure Element dédiée   │ Puce CC EAL5+ │
│ Clé générée in-silico        │ Drapeau isStrongBoxBacked    │ Générée on-   │
│ EC P-256 256 bits            │ RAM & CPU isolés physiquement│ chip via APDU │
│ Déverrouillage FaceID/PIN    │ Authentification biométrique │ Code PIN agent│
└──────────────────────────────┴──────────────────────────────┴───────────────┘
```

1. **Apple Secure Enclave (iOS / iPadOS / macOS)** :
   - Les puces de la série A et M intègrent un coprocesseur cryptographique sécurisé (Secure Enclave Processor - SEP) doté de sa propre mémoire chiffrée et de son propre système d'exploitation sécurisé.
   - Les clés privées sont générées directement dans l'enclave (`kSecAttrKeyTypeECSECPrimeRandom`, taille 256 bits).
   - Les clés privées ne franchissent jamais la frontière de l'enclave sous forme en clair.
   - L'opération de signature s'effectue au sein du SEP, sous condition d'authentification biométrique (Face ID / Touch ID) de l'opérateur PaxFunèbre.
2. **Android StrongBox Keymaster / KeyMint (Android 9+)** :
   - StrongBox s'appuie sur un matériel dédié (Secure Element séparé, tel que la puce Titan M de Google), disposant d'un microprocesseur et d'un stockage physique indépendants du processeur applicatif principal.
   - Configuration obligatoire : `setIsStrongBoxBacked(true)` combiné avec `KeyProperties.KEY_ALGORITHM_EC` et courbe P-256.
   - La clé privée est non exportable (`PURPOSE_SIGN`).
3. **Carte à Puce JavaCard ACOSJ 92k** :
   - Microcontrôleur cryptographique certifié Common Criteria EAL5+ avec 92 Ko de mémoire EEPROM non volatile.
   - Applet JavaCard propriétaire dédiée AeterniTrak.
   - Génération de clé *on-chip* via `KeyPair.genKeyPair()`, supportant nativement `ALG_ECDSA_SHA_256`.
   - Signature déclenchée par commande APDU après validation du code PIN opérateur (APDU `VERIFY`).

---

### 6.2 Résilience et Procédure en Cas de Perte ou de Vol

1. **Protection Physique Inviolable** :  
   Les clés privées stockées en enclave ou sur ACOSJ sont protégées contre les attaques physiques par canaux auxiliaires (DPA, SPA), l'analyse électromagnétique et l'injection de fautes. Même avec un accès physique prolongé à un terminal volé, un attaquant ne peut pas extraire la clé privée en clair.
2. **Procédure de Signalement & Révocation** :
   - Dès la constatation de la perte ou du vol d'un appareil opérateur ou d'une carte d'agent, l'administrateur PaxFunèbre ou AFSCA signale le `kid` correspondant.
   - Le statut de ce `kid` bascule à `"REVOKED"` dans la prochaine version du registre de confiance.
   - La liste d'émetteurs mise à jour est immédiatement déployée sur l'ensemble de la flotte de terminaux.
   - Tout document ou profil prétendument émis après la date de révocation est définitivement rejeté (`ERR_COSE_REVOKED_KEY`).

---

## 7. Matrice de Conformité & Critères d'Acceptation pour Claude AI (Phase A)

Conformément à l'Ordre 0032 et au protocole `PROTOCOL.md` :

- **Phase A Strictement Respectée** : Aucun code d'implémentation (dans `crypto/`, `core/cose/` ou ailleurs) n'est introduit dans le dépôt lors de cette étape.
- **Zéro Clé Privée** : Aucune clé privée, même factice ou de test, n'a été ajoutée. Les clés publiques et signatures de référence seront fournies par Claude AI lors de la création de la suite de vecteurs `qa/vectors/crypto/`.
- **Intégrité des Vecteurs Existants** : `git diff --stat main -- qa/vectors` demeure strictement vide.
- **Règles Testables Univoques** : L'ensemble des 8 étapes de validation est explicité avec code d'erreur standardisé `ERR_COSE_*`, conditions de rejet précises et représentations hexadécimales exactes.

La présente spécification formelle est soumise à Claude AI (Master Verifier) pour examen et approbation.
