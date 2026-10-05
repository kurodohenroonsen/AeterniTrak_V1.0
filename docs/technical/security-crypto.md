# Spécification Technique & Formelle — Sécurité Cryptographique & Modèle de Confiance COSE_Sign1

> **Document ID** : `AET-SPEC-CRYPTO-001`  
> **Version** : 1.2.0  
> **Statut** : Soumis pour révision  
> **Date de référence** : 2026-10-04  
> **Branche Git** : `ag/bushi-02-key-validity`  
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
     $$\left\lfloor \frac{n}{2} \right\rfloor = \text{0x7FFFFFFF800000007FFFFFFFFFFFFFFFDE737D56D38BCF4279DCE5617E3192A8}$$
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

L'ordre de vérification suivant est **strictement normatif** (conforme à `qa/vectors/README.md` §4.8 et §4.11). Aucune étape ne peut être inversée, sautée ou reportée. En particulier, **la charge utile ne doit sous aucun prétexte être inspectée ou désérialisée avant que l'authenticité et l'intégrité cryptographiques n'aient été formellement établies (Étape 12 acquittée)**. Le contrôle temporel (Étape 13) n'intervient qu'après vérification de signature et uniquement pour les clés de confiance dotées d'une fenêtre de validité.

```
[Flux binaire reçu]
        │
        ▼
   [Étape 1] Contrôle Tag 18 (0xd2) ─────────────────────────► Échec : ERR_COSE_INVALID_ENVELOPE
        │
        ▼
   [Étape 2] Décodage strict CBOR du reste ──────────────────► Échec : propagation native ERR_CBOR_*
        │
        ▼
   [Étape 3] Forme de l'enveloppe [bstr, carte, bstr, bstr64] ► Échec : ERR_COSE_INVALID_ENVELOPE
        │
        ▼
   [Étape 4] En-tête protégé : décodable, carte, déterministe ► Échec : ERR_COSE_INVALID_ENVELOPE
        │
        ▼
   [Étape 5] Contrôle de l'algorithme (alg ∈ {-8, -7}) ─────► Échec : ERR_COSE_UNSUPPORTED_ALGORITHM
        │
        ▼
   [Étape 6] Concordance du domaine applicatif (typ) ───────► Échec : ERR_COSE_TYPE_MISMATCH
        │
        ▼
   [Étape 7] Présence et format du kid (16 octets) ──────────► Échec : ERR_COSE_MISSING_KID
        │
        ▼
   [Étape 8] Cohérence globale du Trust Store (K5, K2) ──────► Échec : ERR_COSE_INVALID_TRUST_STORE
        │
        ▼
   [Étape 9] Résolution kid & contrôle de révocation ────────► Échec : ERR_COSE_UNKNOWN_KID / REVOKED_KEY
        │
        ▼
   [Étape 10] Concordance alg déclaré vs Trust Store ────────► Échec : ERR_COSE_ALGORITHM_MISMATCH
        │
        ▼
   [Étape 11] Concordance typ déclaré vs Trust Store (K3) ───► Échec : ERR_COSE_KEY_USAGE_MISMATCH
        │
        ▼
   [Étape 12] Validation signature (Ed25519 ou ES256 low-s) ─► Échec : ERR_COSE_INVALID_SIGNATURE / MALLEABLE / INVALID_PUBLIC_KEY
        │
        ▼
   [Étape 13] Validité temporelle post-signature (K2) ───────► Échec : ERR_COSE_EXPIRED_KEY / ISSUANCE_DATE_MISSING / ERR_CBOR_*
        │
        ▼
   [Déverrouillage Payload certifié]
```

---

### 3.1 Détail Testable des Étapes Normatives

Chaque règle est spécifiée de manière formellement testable sous le triptyque : **Entrée, Condition de Rejet, Code d'Erreur & Résultat**.

#### Étape 1 : Contrôle du Tag 18 (Règle K4)
- **Entrée** : `raw_bytes` (tableau d'octets du message complet).
- **Condition de Rejet** : Le flux d'entrée est vide (`raw_bytes.length === 0`) ou son premier octet est différent de `0xd2` (Tag CBOR 18).
- **Code d'Erreur** : `ERR_COSE_INVALID_ENVELOPE`.
- **Résultat** : Abandon immédiat. Le Tag 18 n'est admis qu'à cette première position ; le décodeur AeterniCore n'est pas modifié.

#### Étape 2 : Décodage Binaire Strict CBOR du Reste du Flux (Règles K4, K5)
- **Entrée** : Sous-tableau d'octets `raw_bytes.subarray(1)`.
- **Condition de Rejet** : Le reste du flux est soumis au décodeur strict AeterniCore (`decodeStrict`). En cas d'anomalie CBOR (entier non minimal, longueur indéfinie, octets résiduels, carte non triée, clés dupliquées, texte non normalisé, tag non autorisé, etc.), l'erreur native sous-jacente remonte telle quelle (`ERR_CBOR_*`, ex. `ERR_CBOR_TRAILING_BYTES`, `ERR_CBOR_NOT_SHORTEST`, `ERR_CBOR_TRUNCATED`).
- **Code d'Erreur** : Propagation directe de `ERR_CBOR_*`.
- **Résultat** : Abandon immédiat de la lecture.

#### Étape 3 : Forme de l'Enveloppe et de l'En-tête Non Protégé (Règles K5, Typage Strict des Clés)
- **Entrée** : Tableau déballé issu du décodage CBOR.
- **Règle Fondamentale sur les Clés d'En-tête** : **Une clé d'en-tête (protégé ou non protégé) est STRICTEMENT un entier non signé (Major 0)**. Toute clé textuelle (ex. `"4"`, `"1"`, `"16"`) ou de tout autre type (booléen, tableau, etc.) est formellement interdite. L'acceptation de chaînes de caractères permettrait deux encodages CBOR distincts d'une même enveloppe, violant le déterminisme et introduisant une malléabilité structurelle inadmissible (`COSE-VER-041`, `COSE-VER-042`).
- **Condition de Rejet** :
  1. L'élément déballé n'est pas un tableau de 4 éléments exactement : `[bstr, carte, bstr, bstr de 64 octets]`.
  2. L'élément 0 (`protected`) n'est pas une chaîne d'octets (`bstr`).
  3. L'élément 1 (`unprotected`) n'est pas une carte CBOR ou porte une clé autre que l'entier strict `4` (`kid`).
  4. L'élément 2 (`payload`) n'est pas une chaîne d'octets (`bstr`).
  5. L'élément 3 (`signature`) n'est pas une chaîne d'octets de 64 octets exactement.
- **Code d'Erreur** : `ERR_COSE_INVALID_ENVELOPE`.
- **Résultat** : Rejet immédiat.

#### Étape 4 : Décodage Strict et Déterminisme de l'En-tête Protégé
- **Entrée** : Octets de l'élément 0 (`protected`).
- **Condition de Rejet** :
  1. L'en-tête protégé n'est pas strictement décodable en carte CBOR.
  2. La carte est vide ou porte une clé autre que les entiers stricts `1` (`alg`) et `16` (`typ`).
  3. Non-respect du déterminisme canonique : les clés entières doivent être encodées dans l'ordre lexicographique strict (`0x01` puis `0x10`). Le ré-encodage déterministe de la carte doit correspondre octet par octet aux octets protégés reçus.
- **Code d'Erreur** : `ERR_COSE_INVALID_ENVELOPE`.
- **Résultat** : Rejet immédiat.

#### Étape 5 : Validation de l'Algorithme Cryptographique Déclaré (`alg`)
- **Entrée** : Valeur associée à la clé `1` dans l'en-tête protégé.
- **Condition de Rejet** :
  1. La clé `1` (`alg`) est absente.
  2. La valeur de `alg` n'est pas un entier relatif.
  3. La valeur de `alg` n'appartient pas à la liste blanche stricte `{-8, -7}`.
- **Code d'Erreur** : `ERR_COSE_UNSUPPORTED_ALGORITHM`.
- **Résultat** : Rejet de l'enveloppe.

#### Étape 6 : Validation du Paramètre de Séparation de Domaine (`typ`)
- **Entrée** : Valeur associée à la clé `16` dans l'en-tête protégé, et type attendu `expected_typ`.
- **Condition de Rejet** :
  1. La clé `16` (`typ`) est absente.
  2. La valeur de `typ` n'est pas une chaîne de caractères UTF-8.
  3. La valeur de `typ` est différente de `expected_typ` (ex. une revendication de lot présentée à un lecteur de profil mémoriel).
- **Code d'Erreur** : `ERR_COSE_TYPE_MISMATCH`.
- **Résultat** : Rejet immédiat.

#### Étape 7 : Présence et Format du `kid`
- **Entrée** : Valeur associée à la clé `4` dans la carte d'en-tête non protégé (`unprotected`).
- **Condition de Rejet** :
  1. La clé `4` (`kid`) est absente.
  2. La valeur associée à `kid` n'est pas une chaîne d'octets (`bstr`) d'exactement 16 octets.
- **Code d'Erreur** : `ERR_COSE_MISSING_KID`.
- **Résultat** : Rejet immédiat.

#### Étape 8 : Cohérence Globale du Magasin de Confiance (Règles K5 et K2)
- **Entrée** : Registre d'émetteurs de confiance (`TrustStore`).
- **Condition de Rejet** : Toute anomalie sur une quelconque entrée du magasin vicie l'ensemble du registre et provoque un rejet immédiat. Pour chaque entrée :
  1. **Empreinte de clé** : Le `kid` doit correspondre strictement aux 16 premiers octets du SHA-256 de la clé publique brute (`kid === SHA-256(raw_public_key)[0..15]`).
  2. **Algorithme et taille** : Si `alg === -8`, la clé publique doit compter exactement 32 octets. Si `alg === -7`, la clé publique doit compter exactement 64 octets. Tout autre algorithme est interdit.
  3. **Unicité** : Aucun doublon de `kid` dans le registre.
  4. **Statut obligatoire (Règle K2)** : Le champ `status` doit être strictement `"ACTIVE"`, `"RETIRED"` ou `"REVOKED"`. Tout autre statut (ex: `"EXPIRED"`) est rejeté.
  5. **Fenêtre de validité (Règle K2)** : Les champs `valid_from` et `valid_until` sont facultatifs, mais ils doivent être **soit tous les deux présents, soit tous les deux absents**. La présence d'une seule des deux bornes est invalide.
  6. **Typage et bornes de la fenêtre** : Si présents, `valid_from` et `valid_until` doivent être des entiers non négatifs (type `number` entier $\ge 0$, sans $-0$), et respecter `valid_from <= valid_until`. Des bornes égales nulles `[0, 0]` sont admises.
  7. **Statut RETIRED fenêtré** : Une entrée au statut `"RETIRED"` doit obligatoirement porter une fenêtre de validité (`valid_from` et `valid_until`).
- **Code d'Erreur** : `ERR_COSE_INVALID_TRUST_STORE`.
- **Résultat** : Rejet immédiat si une seule entrée est incohérente, quelle que soit la clé du message inspecté.

#### Étape 9 : Résolution du `kid` et Contrôle de Révocation
- **Entrée** : `kid` extrait de l'enveloppe et magasin de confiance vérifié.
- **Condition de Rejet** :
  1. Le `kid` est absent du TrustStore : rejet avec `ERR_COSE_UNKNOWN_KID`.
  2. L'entrée de confiance résolue est marquée au statut `"REVOKED"` : rejet immédiat avec `ERR_COSE_REVOKED_KEY`, quelle que soit sa fenêtre de validité ou la date du message.
- **Code d'Erreur** : `ERR_COSE_UNKNOWN_KID` ou `ERR_COSE_REVOKED_KEY`.
- **Résultat** : La clé publique est certifiée appartenir au magasin de confiance et ne pas être révoquée.

#### Étape 10 : Concordance de l'Algorithme Déclaré vs Trust Store
- **Entrée** : `alg` de l'en-tête protégé et `alg` de l'entrée de confiance résolue.
- **Condition de Rejet** : `protected.alg !== trusted_entry.alg`.
- **Code d'Erreur** : `ERR_COSE_ALGORITHM_MISMATCH`.
- **Résultat** : Rejet immédiat (protection anti-rétrogradation).

#### Étape 11 : Concordance du Type Déclaré vs Trust Store (Règle K3)
- **Entrée** : `typ` de l'en-tête protégé et `typ` de l'entrée de confiance résolue.
- **Condition de Rejet** : `protected.typ !== trusted_entry.typ` (ex. une clé de conformité de lot prétendant signer un profil mémoriel).
- **Code d'Erreur** : `ERR_COSE_KEY_USAGE_MISMATCH`.
- **Résultat** : Rejet immédiat (cloisonnement strict des usages de clés).

#### Étape 12 : Vérification Cryptographique de la Signature
- **Entrée** : Clé publique résolue, signature (64 octets), structure `Sig_structure` calculée sur `["Signature1", protected_bytes, h'', payload]`.
- **Condition de Rejet** :
  1. Si `alg === -7` (ES256) :
     - Clé publique non située sur la courbe P-256 ($X, Y \in [0, p-1]$, satisfaction de $y^2 \equiv x^3 - 3x + b \pmod p$, point non nul) : rejet avec `ERR_COSE_INVALID_PUBLIC_KEY`.
     - Composantes de signature $r, s \notin [1, n-1]$ : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
     - **Violation de la règle low-s** ($s > \lfloor n/2 \rfloor$) : rejet avec `ERR_COSE_MALLEABLE_SIGNATURE`.
     - L'opération cryptographique ECDSA échoue : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
  2. Si `alg === -8` (Ed25519) :
     - Le point de clé publique ou de signature est invalide, le scalaire $S \ge L$ (non canonique), ou la vérification WebCrypto échoue : rejet avec `ERR_COSE_INVALID_SIGNATURE`.
- **Code d'Erreur** : `ERR_COSE_INVALID_SIGNATURE`, `ERR_COSE_MALLEABLE_SIGNATURE`, `ERR_COSE_INVALID_PUBLIC_KEY`.
- **Résultat** : L'authenticité mathématique et l'intégrité de la charge utile sont acquittées. En cas d'échec, le payload n'est jamais déverrouillé.

#### Étape 13 : Contrôle de Validité Temporelle Post-Signature (Règle K2) & Déverrouillage Payload
- **Entrée** : Charge utile attachée `payload`, type attendu `expected_typ`, et entrée de confiance `trusted_entry`.
- **Condition d'Exécution & Règles Normatives** :
  1. **Exécution Post-Signature Stricte** : La validité temporelle n'est évaluée qu'après confirmation intégrale de la signature cryptographique à l'étape 12. Aucune date d'émission n'est lue dans une charge utile non signée.
  2. **Entrée sans Fenêtre** : Si l'entrée de clé de confiance ne porte aucune fenêtre temporelle (`valid_from` et `valid_until` absents), la charge utile n'est PAS décodée à cette étape. Le payload est directement déverrouillé et restitué (maintien à 100% du comportement nominal des 104 vecteurs initiaux, cas `COSE-KEY-026`).
  3. **Décodage Strict de la Charge Utile** : Si l'entrée porte une fenêtre temporelle `[valid_from, valid_until]`, la charge utile est décodée via `decodeStrict`. Si le flux est tronqué ou invalide, l'erreur native `ERR_CBOR_*` remonte telle quelle (`COSE-KEY-024`, `COSE-KEY-025`).
  4. **Extraction de la Date d'Émission** :
     - Si `expected_typ === "application/aeternitrak-profile+cbor"` : la date d'émission $D$ doit être portée par la clé entière `11` sous l'étiquette sémantique Tag CBOR 100 (nombre de jours depuis le 1er janvier 1970).
     - Si `expected_typ === "application/aeternitrak-batch-claim+cbor"` : la date d'émission $S$ doit être portée par la clé entière `3` sous l'étiquette sémantique Tag CBOR 1 (horodatage UNIX en secondes, entier non négatif).
     - Si la charge utile n'est pas une carte CBOR, si la clé est absente, si l'étiquette sémantique est incorrecte (ex: tag 1 sur profil ou tag 100 sur certificat), s'il s'agit d'un entier nu, ou si la clé est textuelle : rejet avec `ERR_COSE_ISSUANCE_DATE_MISSING`.
  5. **Comparaison Temporelle aux Bornes (Incluses)** :
     - Pour un profil mémoriel (daté au jour $D$) : comparaison au jour :
       $$\lfloor valid\_from / 86400 \rfloor \le D \le \lfloor valid\_until / 86400 \rfloor$$
     - Pour un certificat de lot (daté à la seconde $S$) : comparaison à la seconde :
       $$valid\_from \le S \le valid\_until$$
     - Si la date d'émission se situe hors de l'intervalle (antérieure comme postérieure) : rejet avec `ERR_COSE_EXPIRED_KEY`.
  6. **Interdiction Formelle de l'Horloge Locale (Zero-Clock)** : L'horloge du lecteur n'intervient jamais. Aucun appel à `Date.now()` ou `new Date()` n'est toléré dans le module de vérification.
- **Limite de Sécurité Fondamentale (Antidatage)** :
  > [!WARNING]
  > **Limite Intrinsèque — Vulnérabilité à l'Antidatage** :  
  > La date d'émission est déclarée unilatéralement par le signataire au sein de la charge utile. Si une clé privée de signature est volée ou compromise, l'attaquant peut forger et signer un document frauduleux en y inscrivant une date d'émission artificielle comprise dans la fenêtre de validité passée de la clé. La fenêtre temporelle ne protège pas contre cette falsification ; **seule la révocation formelle (`status: "REVOKED"`) neutralise une clé compromise**.
- **Code d'Erreur** : `ERR_COSE_EXPIRED_KEY`, `ERR_COSE_ISSUANCE_DATE_MISSING`, ou propagation de `ERR_CBOR_*`.
- **Résultat** : Restitution sécurisée de la charge utile certifiée (`VerifyResult`).

---

### 3.2 Registre Normatif des Codes d'Erreur Typés

| Code d'Erreur | Étape | Signification Formelle |
|---|---|---|
| `ERR_COSE_INVALID_ENVELOPE` | 1, 3, 4 | Structure non conforme (tag 18 manquant, tableau ≠ 4 éléments, types invalides, en-tête non protégé avec clé autre que 4, en-tête protégé non déterministe ou avec clés autres que 1 et 16). |
| `ERR_CBOR_*` | 2, 13 | Décodage CBOR invalide (erreur native AeterniCore sur l'enveloppe ou sur la charge utile fenêtrée, ex. `ERR_CBOR_TRUNCATED`). |
| `ERR_COSE_UNSUPPORTED_ALGORITHM` | 5 | Algorithme non autorisé ou absent de la liste blanche `{-8, -7}`. |
| `ERR_COSE_TYPE_MISMATCH` | 6 | Paramètre `typ` (étiquette 16) manquant, malformé ou non concordant avec le type attendu. |
| `ERR_COSE_MISSING_KID` | 7 | Clé 4 (`kid`) absente de l'en-tête non protégé ou taille ≠ 16 octets. |
| `ERR_COSE_INVALID_TRUST_STORE` | 8 | Magasin de confiance incohérent (`kid` ≠ empreinte SHA-256 de la clé, algorithme invalide, taille de clé incorrecte, doublon, statut inconnu, fenêtre incohérente ou absente pour RETIRED). |
| `ERR_COSE_UNKNOWN_KID` | 9 | Identifiant `kid` inconnu dans la liste de confiance locale. |
| `ERR_COSE_REVOKED_KEY` | 9 | Clé révoquée dans le Trust Store (rejet inconditionnel de tous ses documents). |
| `ERR_COSE_ALGORITHM_MISMATCH` | 10 | L'algorithme déclaré ne correspond pas à celui assigné dans le Trust Store. |
| `ERR_COSE_KEY_USAGE_MISMATCH` | 11 | Le type de document ne correspond pas à l'usage autorisé pour cette clé dans le Trust Store. |
| `ERR_COSE_INVALID_PUBLIC_KEY` | 12 | Clé publique invalide ou non située sur la courbe P-256. |
| `ERR_COSE_MALLEABLE_SIGNATURE` | 12 | Signature ES256 malléable rejetée ($s > \lfloor n/2 \rfloor$, violation BSI TR-03111). |
| `ERR_COSE_INVALID_SIGNATURE` | 12 | Signature mathématiquement corrompue, falsifiée ou scalaire Ed25519 non canonique. |
| `ERR_COSE_ISSUANCE_DATE_MISSING` | 13 | Date d'émission absente, étiquette CBOR incorrecte, entier nu ou charge utile non-carte lors d'une vérification sous entrée de confiance fenêtrée. |
| `ERR_COSE_EXPIRED_KEY` | 13 | Date d'émission déclarée dans la charge utile hors de la fenêtre `[valid_from, valid_until]` de l'entrée de confiance. |
| `ERR_COSE_UNVERIFIED_PAYLOAD_ACCESS` | 13 | Tentative d'accès au payload sans vérification cryptographique complète préalable. |

---

### 3.3 Lecture sous Réserve — Décision DEC-AET-07 Option B (`coseOpen`)

Conformément à l'arbitrage souverain de Kudoro (`DECISIONS-KUDORO.md`, décision `DEC-AET-07` Option B) et aux règles formelles de `qa/vectors/README.md` §4.9 :

L'opération `coseVerify` demeure la référence normative fondamentale : elle exécute l'intégralité des 13 étapes de vérification et ne restitue le payload qu'en cas d'authentification cryptographique parfaite (`valid: true`).

L'opération `coseOpen(envelope, expectedTyp, trustStore)` constitue l'interface applicative standard de consultation et de rendu des cartes et profils :

1. **`VERIFIED` (Authenticité Certifiée)** :
   - **Condition** : `coseVerify` franchit avec succès les 13 étapes de contrôle avec une clé de confiance active ou retirée dont la date est dans la fenêtre.
   - **Retour** : `{ status: "VERIFIED", valid: true, payload, payload_hex, kid }`.
   - **Usage Applicatif** : Affichage certifié de plein droit.

2. **`UNVERIFIED` (Lecture sous Réserve — Émetteur Inconnu)** :
   - **Condition** : **Seule et uniquement** l'erreur `ERR_COSE_UNKNOWN_KID` autorise ce régime. Cela garantit que les étapes 1 à 7 ont réussi avec succès : enveloppe bien formée, tag 18 présent, en-têtes typés strictement avec clés entières, algorithme autorisé, type de contenu attendu (`typ === expected_typ`), et identifiant `kid` de 16 octets présent.
   - **Retour** : `{ status: "UNVERIFIED", valid: false, payload, payload_hex, reason: "ERR_COSE_UNKNOWN_KID" }`.
   - **Usage Applicatif** : L'application est autorisée à afficher le mémorial sous réserve, mais **DOIT impérativement afficher un bandeau d'avertissement visible** (*« Authenticité non vérifiée — Émetteur inconnu »*).
   - **Interdiction Formelle** : Une carte sous statut `UNVERIFIED` ne possède **aucune valeur de preuve juridique ou technique**. Elle ne peut en aucun cas franchir la Porte de Fer (Bushi 12) ni servir de justificatif réglementaire ou sanitaire.

3. **`BLOCKED` (Blocage Inconditionnel)** :
   - **Condition** : Toute autre anomalie lors de la vérification :
     - Clé révoquée (`ERR_COSE_REVOKED_KEY`).
     - Clé expirée (`ERR_COSE_EXPIRED_KEY`).
     - Date d'émission absente ou tag CBOR non conforme (`ERR_COSE_ISSUANCE_DATE_MISSING`).
     - Signature invalide ou corrompue (`ERR_COSE_INVALID_SIGNATURE`).
     - Signature ECDSA malléable avec $s > \lfloor n/2 \rfloor$ (`ERR_COSE_MALLEABLE_SIGNATURE`).
     - Clé publique hors courbe (`ERR_COSE_INVALID_PUBLIC_KEY`).
     - Discordance d'usage de clé (`ERR_COSE_KEY_USAGE_MISMATCH`).
     - Discordance de type de document (`ERR_COSE_TYPE_MISMATCH`).
     - Algorithme non supporté (`ERR_COSE_UNSUPPORTED_ALGORITHM`).
     - Enveloppe malformée, clés non entières ou octets résiduels (`ERR_COSE_INVALID_ENVELOPE`, `ERR_CBOR_*`).
     - Identifiant de clé absent ou corrompu (`ERR_COSE_MISSING_KID`).
     - Magasin de confiance incohérent (`ERR_COSE_INVALID_TRUST_STORE`).
   - **Retour** : `{ status: "BLOCKED", valid: false, error }`.
   - **Protection Anti-Fuite** : **Aucune charge utile (`payload`) n'est délivrée**.

> [!IMPORTANT]
> **Séparation Stricte des Types** : Le type de retour de `coseOpen` sépare formellement les statuts `VERIFIED`, `UNVERIFIED` et `BLOCKED` via une union discriminée TypeScript pour interdire toute confusion accidentelle par le code appelant entre un payload certifié et un payload sous réserve.

> [!IMPORTANT]
> **Note de Coordination Inter-Bushi (Alignement Bushi 12 — The Iron Gate)** :  
> Le document `docs/technical/antiprion-feedban.md` §6.2 mentionne actuellement une enveloppe COSE_Sign1 « sans tag 18 ». Cette description est obsolète et contraire à la présente spécification (`AET-SPEC-CRYPTO-001`, Règle K4, Étape 1) ainsi qu'au RFC 9052 §4.2, qui imposent la présence impérative du Tag CBOR 18 (`0xd2`) comme premier octet de toute enveloppe. Le Bushi 12 devra aligner sa documentation lors de sa prochaine itération.

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
  ? valid_from: uint,                    ; Début de validité facultatif (timestamp UNIX secondes, les deux ou aucun)
  ? valid_until: uint,                   ; Fin de validité facultatif (timestamp UNIX secondes, les deux ou aucun)
  status: "ACTIVE" / "RETIRED" / "REVOKED" ; État opérationnel de la clé (Règle K2)
}
```

---

### 4.4 Règle d'Étanchéité : « Une Clé, Un Algorithme, Un Rôle, Un Type »

Pour éliminer toute ambiguïté sémantique et parer toute attaque par réutilisation de clé (*cross-protocol key reuse*), AeterniTrak applique une règle d'étanchéité stricte :

1. **Une clé cryptographique est assignée à un algorithme unique** : Une même clé ne peut jamais être sollicitée ou déclarée sous un algorithme différent.
2. **Une clé cryptographique est assignée à un rôle métier unique** : Une station de pompes funèbres ne peut jamais émettre une attestation sanitaire de lot ; un laboratoire d'analyse ne peut jamais émettre un profil civil mémoriel.
3. **Une clé cryptographique est assignée à un type de contenu unique (`typ`)** : L'étiquette `16` protégée scelle définitivement le contexte d'interprétation.

---

### 4.5 Rotation et Révocation Hors-Ligne (Zero-Network & Règle K2)

AeterniTrak opère dans des environnements dépourvus de connectivité réseau (chambres funéraires en sous-sol, forêts cinéraires reculées, abattoirs isolés, postes d'équarrissage industriels). Aucune requête en ligne (OCSP, CRL sur serveur HTTP) n'est requise.

1. **Mises à Jour Monotones Signées** : Les révocations de clés compromises et l'enregistrement de nouveaux émetteurs sont distribués via les mises à jour standard de l'application (App Store, Google Play, paquets d'audit signés).
2. **Trois Statuts Opérationnels d'Émetteurs (Règle K2)** :
   - `ACTIVE` : Clé pleinement opérationnelle autorisée à signer de nouvelles charges utiles. Si l'entrée porte une fenêtre temporelle `[valid_from, valid_until]`, les documents signés ne sont valides que si leur date d'émission se situe dans cet intervalle. Si l'entrée ne porte aucune fenêtre temporelle, aucune restriction temporelle ne s'applique.
   - `RETIRED` : Clé retirée du service actif (ne signant plus de nouvelles cartes). Elle porte obligatoirement une fenêtre temporelle `[valid_from, valid_until]`. Ses cartes émises durant sa période active demeurent certifiées valides à perpétuité si leur date d'émission est comprise dans la fenêtre.
   - `REVOKED` : Clé compromise ou signalée volée. Tout document portant la signature de ce `kid` est rejeté inconditionnellement avec `ERR_COSE_REVOKED_KEY`, quelle que soit sa date d'émission déclarée.
3. **Contrôle Temporel Décorrélé de la Lecture (Zero-Clock & Limite d'Antidatage)** :
   Une carte mémorielle se lit pendant des décennies et le terminal de lecture ne dispose d'aucune horloge de confiance en mode déconnecté. La fenêtre de validité `[valid_from, valid_until]` ne se compare JAMAIS à l'horloge locale du lecteur (`now`), mais exclusivement à la date d'émission scellée dans la charge utile vérifiée (clé 11 du profil au jour, clé 3 du lot à la seconde), après validation de la signature cryptographique (Étape 13). Toute date d'émission hors fenêtre déclenche `ERR_COSE_EXPIRED_KEY`.
   
   *Limite fondamentale d'antidatage* : La date d'émission est une assertion déclarée par le signataire au sein de la charge utile. Une clé volée peut donc être utilisée par un attaquant pour antidater une charge utile dans la fenêtre passée de la clé ; la fenêtre temporelle ne protège pas contre ce risque, seule la révocation formelle (`status: "REVOKED"`) neutralise une clé compromise.

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

| Famille | Rôle Opérationnel | Algorithme Assigné | Support d'Exécution & Emplacement | Paramètre `typ` Obligatoire | Statut V1 |
|---|---|---|---|---|---|
| **Famille 1 : Clé d'Hommage Mémoriel** | Signature des profils civils d'hommage humain et animaux de compagnie (Bloc 1 du Sanctuaire). | **ES256 (`alg: -7`)** | Enclave matérielle sécurisée : Apple Secure Enclave, Android StrongBox sur tablette de station funéraire PaxFunèbre, ou carte opérateur JavaCard ACOSJ 92k. | `"application/aeternitrak-profile+cbor"` | **Actif V1.0** |
| **Famille 2 : Clé de Conformité de Lot** | Signature des attestations de conformité sanitaire et feed-ban de la filière de sarcomusation (Portes G0 à G9 de The Iron Gate). | **Ed25519 (`alg: -8`)** | Serveur durci de laboratoire d'analyse vétérinaire agréé ou micro-service de validation certifié. | `"application/aeternitrak-batch-claim+cbor"` | **Actif V1.0** |
| **Famille 3 : Clé d'Audit Régulateur** | Contre-signature d'inspection officielle, constats de prélèvement, scellés vétérinaires et visas douaniers d'exportation. | **ES256 (`alg: -7`)** | *Hypothèse architecturale cible* : Terminal d'inspection durci des agents de l'État (AFSCA / DNF) avec puce Secure Element ou carte d'agent assermenté ACOSJ 92k. | `"application/aeternitrak-audit-claim+cbor"` | *Hors v1 (Extension future)* |
| **Famille 4 : Clé de Politique Dérogatoire** | Signature de la politique d'autorisation administrative d'amendement forestier cinéraire privé pour dépouilles de compagnie Catégorie 1 LFA-négatives (`DEC-AET-05`). | **Ed25519 (`alg: -8`)** *(ou ES256)* | *Hypothèse architecturale cible* : HSM souverain d'administration centrale (DGO3 / AFSCA) ou autorité réglementaire. | `"application/aeternitrak-policy+cbor"` | *Hors v1 (Extension future)* |

*(Règle K6 — Les Familles 3 et 4 sont formellement réservées pour extensions futures hors V1. Les mentions d'équipements de tiers tels que les HSM de l'AFSCA ou de la DGO3 constituent des hypothèses architecturales de déploiement et non des faits ou engagements contractuels avérés).*

### 5.2 Rationale des Choix Algorithmiques

- **Pourquoi ES256 pour les familles 1 et 3 ?**  
  Les stations funéraires PaxStation (App 2) et les agents d'inspection opèrent sur des équipements dotés d'enclaves matérielles (iPad avec Apple Secure Enclave, terminaux Android durcis avec Android StrongBox selon `DEC-AET-10`). Ces puces de sécurité matérielle intègrent nativement des accélérateurs cryptographiques pour la courbe NIST P-256. L'usage d'ES256 garantit que la clé privée ne peut physiquement pas être extraite du silicium de la station d'encodage.
- **Pourquoi Ed25519 pour la famille 2 (Porte de Fer) ?**  
  La filière de sarcomusation requiert le traitement de dizaines de milliers de lots industriels et de requêtes P2P décentralisées. Ed25519 offre une vitesse d'exécution supérieure, une dérivation déterministe mathématique exempte de génération d'aléa par signature (éliminant tout risque de fuite de clé par biais du générateur aléatoire), et une immunité totale contre la malléabilité.

---

## 6. Stockage Matériel Sécurisé & Résilience Silicium

### 6.1 Architecture des Enclaves Matérielles de Scellement (`DEC-AET-10`)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 ENCLAVES MATÉRIELLES DE SCELLEMENT (STATION PAXSTATION)       │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│    Apple Secure Enclave      │     Android StrongBox        │ Stockage      │
│        (iOS / macOS)         │       (Android 9+)           │  ACOSJ 92 Ko  │
├──────────────────────────────┼──────────────────────────────┼───────────────┤
│ Coprocesseur SEP isolé       │ Puce Secure Element dédiée   │ Coffre EEPROM │
│ Clé générée in-silico        │ Drapeau isStrongBoxBacked    │ Immuable      │
│ EC P-256 256 bits            │ RAM & CPU isolés physiquement│ Scellement    │
│ Déverrouillage biométrique   │ Authentification biométrique │ Fusible DE 01 │
└──────────────────────────────┴──────────────────────────────┴───────────────┘
```

1. **Apple Secure Enclave (Station iPadOS / macOS)** :
   - Les puces de la série A et M intègrent un coprocesseur cryptographique sécurisé (Secure Enclave Processor - SEP) doté de sa propre mémoire chiffrée et de son propre système d'exploitation sécurisé.
   - Les clés privées sont générées directement dans l'enclave (`kSecAttrKeyTypeECSECPrimeRandom`, taille 256 bits).
   - Les clés privées ne franchissent jamais la frontière de l'enclave sous forme en clair.
   - L'opération de signature s'effectue au sein du SEP de la station de gravure, sous condition d'authentification biométrique (Face ID / Touch ID) de l'opérateur PaxFunèbre.
2. **Android StrongBox Keymaster / KeyMint (Station Android)** :
   - StrongBox s'appuie sur un matériel dédié (Secure Element séparé, tel que la puce Titan M de Google), disposant d'un microprocesseur et d'un stockage physique indépendants du processeur applicatif principal.
   - Configuration obligatoire : `setIsStrongBoxBacked(true)` combiné avec `KeyProperties.KEY_ALGORITHM_EC` et courbe P-256.
   - La clé privée est non exportable (`PURPOSE_SIGN`).
3. **Carte à Puce JavaCard ACOSJ 92 Ko (Coffre de Stockage Immuable, `DEC-AET-01`, `DEC-AET-10`)** :
   - Microcontrôleur cryptographique avec 92 Ko de mémoire EEPROM non volatile.
   - La carte ne génère pas de clé privée active : elle stocke l'enveloppe `COSE_Sign1` scellée par la station PaxStation dans son fichier élémentaire `EF-5`.
   - Protection matérielle absolue via commande de soufflage du fusible in-silico `80 DE 01 00`, interdisant toute altération ultérieure.

---

### 6.2 Résilience et Procédure en Cas de Perte ou de Vol

1. **Protection Physique Inviolable** :  
   Les clés privées stockées en enclave ou sur ACOSJ sont protégées contre les attaques physiques par canaux auxiliaires (DPA, SPA), l'analyse électromagnétique et l'injection de fautes. Même avec un accès physique prolongé à un terminal volé, un attaquant ne peut pas extraire la clé privée en clair.
2. **Procédure de Signalement & Révocation (Règle K2)** :
   - Dès la constatation de la perte ou du vol d'un appareil opérateur ou d'une carte d'agent, l'administrateur PaxFunèbre ou AFSCA signale le `kid` correspondant.
   - Le statut de ce `kid` bascule à `"REVOKED"` dans la prochaine version du registre de confiance (*Trust Store*).
   - La liste d'émetteurs mise à jour est immédiatement déployée sur l'ensemble de la flotte de terminaux.
   - **Règle absolue de sécurité (Règle K2)** : Tout document ou profil signé par une clé révoquée est **inconditionnellement et immédiatement rejeté** (`ERR_COSE_REVOKED_KEY`), quelle que soit la date d'émission déclarée dans sa charge utile. En effet, un attaquant ayant dérobé ou compromis une clé privée pourrait facilement antidater les documents forgés ; aucune antériorité alléguée n'est donc admise en cas de révocation.

---

## 7. Matrice de Conformité & Critères d'Acceptation (Amendements v1.2.0 & Phase B)

Conformément à l'Ordre 0037, au Redirect 0042 et à l'Ordre 0057 de Claude AI :

- **Spécification v1.2.0 & Règle K2 Alignées** : Intégration de la règle de validité temporelle des clés K2 en 13 étapes normatives (§3.1, §4.5), fenêtre `[valid_from, valid_until]` facultative dans le registre de confiance (CDDL §4.3), contrôle post-signature stricte (Étape 13) avec décodage CBOR strict et vérification de la date d'émission portée par la charge utile (tag 100 jours pour profil, tag 1 secondes pour certificat), et mention formelle de la limite d'antidatage par clé compromise neutralisée par révocation.
- **Amendements v1.1.0 & v1.1.1 Intégrés** : Application des 7 amendements normatifs K1 à K7, correction de la constante $\lfloor n/2 \rfloor$ de P-256 dans la spécification (§2.2), typage strict entier des clés d'en-tête (rejet immédiat de toute clé textuelle, §3.1), intégration contractuelle de la lecture sous réserve DEC-AET-07 Option B (`coseOpen`, §3.3), et notification d'alignement au Bushi 12 pour le Tag 18.
- **Portabilité WebCrypto Stricte (Zéro `node:crypto`)** : Implémentation réalisée sous `core/cose/` en TypeScript ESM sans aucune dépendance npm (`dependencies: {}`) et sans aucun import de modules Node (`node:crypto`), s'appuyant exclusivement sur `globalThis.crypto.subtle` (`digest`, `importKey`, `verify`, `sign`) pour assurer la portabilité totale sur WebView Android et navigateur.
- **Zéro Clé Privée dans `core/`** : Aucune clé privée ou graine secrète n'est présente dans le code source ; seuls les vecteurs de tests publics RFC 8032 et RFC 6979 de `qa/vectors/crypto/` font foi.
- **Intégrité des Vecteurs de Test** : `git diff --stat main -- qa/vectors` demeure strictement vide.
- **Déverrouillage Sécurisé Strict** : La charge utile n'est jamais exposée ni désérialisée en cas d'échec d'une quelconque étape de contrôle cryptographique ; seule l'opération `coseOpen` restitue le payload sous réserve (`status: "UNVERIFIED"`) pour le cas unique `ERR_COSE_UNKNOWN_KID`.
